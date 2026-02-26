import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()

SITE_URL = "https://prometeontyregroup-my.sharepoint.com/personal/mazen_ahmed_st_prometeon_com"

# 1. READ EMAILS
emails_raw = os.getenv("TARGET_EMAILS")
if not emails_raw:
    print("ERROR: Could not find 'TARGET_EMAILS' in .env file!")
    exit()

TARGET_EMAILS = [e.strip() for e in emails_raw.split(",") if e.strip()]

# Lists to IGNORE
EXCLUDED_LISTS = [
    "Documents", "Form Templates", "Style Library", 
    "Site Assets", "Site Pages", "Maintenance Mode",
    "Social", "MicroFeed", "TaxonomyHiddenList",
    "Documenti", "Pagine del sito", "Social networking"
]

def get_sharepoint_cookies(site_url):
    print(">>> LAUNCHING EDGE...")
    driver_path = "msedgedriver.exe"
    if not os.path.exists(driver_path): return None

    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Edge(service=service)
    except: return None
    
    driver.get(site_url)
    print(">>> LOG IN and press ENTER here when ready.")
    input("Press Enter to continue...") 
    
    selenium_cookies = driver.get_cookies()
    driver.quit()
    
    session = requests.Session()
    for cookie in selenium_cookies:
        session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])
    return session

def get_request_digest(session, site_url):
    url = f"{site_url}/_api/contextinfo"
    headers = {"Accept": "application/json;odata=verbose"}
    response = session.post(url, headers=headers)
    return response.json()['d']['GetContextWebInformation']['FormDigestValue'] if response.status_code == 200 else None

def resolve_user_id(session, email, headers):
    """Finds the ID to remove."""
    print(f"   > Finding ID for: {email}...", end=" ")
    user_url = f"{SITE_URL}/_api/web/siteusers/getByEmail('{email}')"
    r = session.get(user_url, headers=headers)
    
    if r.status_code == 200:
        uid = r.json()['d']['Id']
        print(f"[FOUND: {uid}]")
        return uid
    print("[NOT FOUND - Skipping]")
    return None

def main():
    # 1. Login
    session = get_sharepoint_cookies(SITE_URL)
    if not session: return
    
    digest = get_request_digest(session, SITE_URL)
    headers = {
        "Accept": "application/json;odata=verbose",
        "Content-Type": "application/json;odata=verbose",
        "X-RequestDigest": digest
    }

    # 2. RESOLVE USER IDs TO REMOVE
    print(f"\n>>> Step 1: Identifying Users to Remove...")
    ids_to_remove = []
    for email in TARGET_EMAILS:
        uid = resolve_user_id(session, email, headers)
        if uid: ids_to_remove.append(uid)
            
    if not ids_to_remove:
        print("No users found to remove. Exiting.")
        return

    # 3. LOOP LISTS AND REMOVE
    print("\n>>> Step 2: Removing Permissions...")
    r_lists = session.get(f"{SITE_URL}/_api/web/lists", headers=headers)
    all_lists = r_lists.json()['d']['results']

    i = 1
    for lst in all_lists:
        title = lst['Title']
        if lst['Hidden'] or title in EXCLUDED_LISTS: continue

        print(f"{i}. {title}...", end=" ")
        i += 1

        removed_count = 0
        for uid in ids_to_remove:
            # API: RemoveRoleAssignment (Deletes user from permission list)
            remove_url = f"{SITE_URL}/_api/web/lists/getbytitle('{title}')/roleassignments/removeroleassignment(principalid={uid})"
            r_remove = session.post(remove_url, headers=headers)
            
            if r_remove.status_code == 200:
                removed_count += 1
        
        print(f"[Removed {removed_count} users]")

    print("\n>>> All done!")
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()