import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv() # Load the .env file

SITE_URL = "https://prometeontyregroup-my.sharepoint.com/personal/mazen_ahmed_st_prometeon_com"

# 1. READ EMAILS FROM .ENV
emails_raw = os.getenv("TARGET_EMAILS")
if not emails_raw:
    print("ERROR: Could not find 'TARGET_EMAILS' in .env file!")
    exit()

# Clean up the list (remove spaces, split by comma)
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
    if not os.path.exists(driver_path):
        print("Driver not found.")
        return None

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
    """Finds the ID for a single email. Returns ID or None."""
    print(f"   > Resolving ID for: {email}...", end=" ")
    
    # Try generic lookup
    user_url = f"{SITE_URL}/_api/web/siteusers/getByEmail('{email}')"
    r = session.get(user_url, headers=headers)
    
    if r.status_code == 200:
        uid = r.json()['d']['Id']
        print(f"[FOUND: {uid}]")
        return uid
    
    # Try EnsureUser (Force add to directory)
    ensure_url = f"{SITE_URL}/_api/web/ensureUser('{email}')"
    r = session.post(ensure_url, headers=headers)
    
    if r.status_code == 200:
        uid = r.json()['d']['Id']
        print(f"[ADDED: {uid}]")
        return uid
    
    print("[FAILED - User not found]")
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

    # 2. RESOLVE ALL USERS FIRST (Optimization)
    print(f"\n>>> Step 1: Resolving {len(TARGET_EMAILS)} Users...")
    valid_user_ids = []
    
    for email in TARGET_EMAILS:
        uid = resolve_user_id(session, email, headers)
        if uid:
            valid_user_ids.append(uid)
            
    if not valid_user_ids:
        print("No valid users found. Exiting.")
        return

    # 3. GET ROLE ID
    r_role = session.get(f"{SITE_URL}/_api/web/roledefinitions/getbyname('Contribute')", headers=headers)
    role_id = r_role.json()['d']['Id'] if r_role.status_code == 200 else 1073741827

    # 4. LOOP LISTS AND ADD EVERYONE
    print("\n>>> Step 2: Granting Permissions on Lists...")
    r_lists = session.get(f"{SITE_URL}/_api/web/lists", headers=headers)
    all_lists = r_lists.json()['d']['results']

    i = 1
    for lst in all_lists:
        title = lst['Title']
        if lst['Hidden'] or title in EXCLUDED_LISTS: continue

        print(f"{i}. {title}...", end=" ")
        i += 1

        # A. Break Inheritance (Once per list)
        session.post(f"{SITE_URL}/_api/web/lists/getbytitle('{title}')/breakroleinheritance(copyRoleAssignments=true, clearSubscopes=true)", headers=headers)

        # B. Add ALL users to this list
        success_count = 0
        for uid in valid_user_ids:
            add_url = f"{SITE_URL}/_api/web/lists/getbytitle('{title}')/roleassignments/addroleassignment(principalid={uid}, roledefid={role_id})"
            r_add = session.post(add_url, headers=headers)
            if r_add.status_code == 200:
                success_count += 1
        
        print(f"[Added {success_count}/{len(valid_user_ids)} users]")

    print("\n>>> All done!")
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()