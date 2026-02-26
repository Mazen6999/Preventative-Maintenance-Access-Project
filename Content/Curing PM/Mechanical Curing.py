import pandas as pd
import io

# The input CSV data for the template machine (A0)
csv_data = """Curing Press,Sub_Machine,Element_Machine,.,Task_Description,Task_Code,Estimated_mins,Crew,Period_freq,W1,W2,W3,W4,W5,W6,W7,W8,W9,W10,W11,W12,W13,W14,W15,W16,W17,W18,W19,W20,W21,W22,W23,W24,W25,W26,W27,W28,W29,W30,W31,W32,W33,W34,W35,W36,W37,W38,W39,W40,W41,W42,W43,W44,W45,W46,W47,W48,W49,W50,W51,W52
A0,(A) hydraulic general check,,1,Review the conditions of  the packing of bladder cylinder (top ring)مراجعة حشو جلبة التوب رنج,P1,120,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(A) hydraulic general check,,2,check the hydraulic hose & piping  conditions مراجعة حالة خراطيم سلندرات الهيدروليكا والمواسير,P2,60,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(A) hydraulic general check,,3,check the hydaulic cylinder packing conditions مراجعة حشو سلندرات الهيدروليكا,P3,240,2M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(A) hydraulic general check,,4,Review the conditions of the safety of topring and filters مراجعة حالة فلتر وسفتى خطوط الهيدروليكا,P4,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(B) Steam Box,,5,Review the conditions of the dome gasket مراجعة مجرى جوان الدوم جاسكت,P5,20,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(B) Steam Box,,6,Review the conditions of the cover gasket مراجعة حشو اغطية الدوم,P6,45,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(B) Steam Box,,7,change the packing of teeth load mechansim  مراجعة حشو ترس الرجلاش,P7,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(B) Steam Box,,8,Review the conditions of the packing between sector cylinder rod and upper dome مراجعة حشو بخار عمود سلندر السكتور مع الحلة العلوية,P8,360,2M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(B) Steam Box,,9,Review the conditions of the  mechamical safety of dome مراجعة بلف سفتى الدوم,P9,120,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-1) adjust the loader centering,10,Review the conditions of the safety nut with its power screw teeth and washer which carrying the chuck and its conditions مراجعة صامولة ماكنزم الخرشوفة وحالة عمود الباور سكرو,P22,60,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-1) adjust the loader centering,11,adjust all chuck rollers and guides for loader. ضبط ومراجعة ريش الخرشوفة,P11,90,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-1) adjust the loader centering,12,adjust the centering of chuck with bladder centering ضبط سنترة اللوادر مع ال عمود التوب رنج,P12,120,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-2) Re-tight the bolts of the following positions,13,machine base مراجعة رباط مسامير قاعدة الماكينة,P13,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-2) Re-tight the bolts of the following positions,14,lower ring mechanism مراجعة رباط مسامير ماكنزم اللوارنج,P13,30,2M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-2) Re-tight the bolts of the following positions,15,"side link mechanism,end caps blots مراجعة رباط مسامير السيايد لنك",P13,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-2) Re-tight the bolts of the following positions,16,"arms mechanism,dome munting blots مراجعة مسامير ماكنزم الذراعات وحلل الدوم",P13,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-2) Re-tight the bolts of the following positions,17,main Gear-box fixation bolts مراجعة رباط مسامير الجيربوكس الرئيسى للكباس,P13,30,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-3)  parallsim,18,check the parallsim( machine centering) مراجعو سنترة حلة الدوم العلوية مع سنترة الحلة السفلية وعمود التوب رنج,P14,120,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-4)gear box,19,check oil level,P15,20,1M,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-4)gear box,20,change oil,P16,120,1M,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-5) Gearsing,21,Check the lubrication injectos points مراجعة حالة نقط التشحيم,P17,120,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) mechanical  check points,(B-5) Gearsing,22,Review the conditions ofthe main bushing clearance مراجعة خلوصات جلب الكباس الرئيسية,P18,180,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) curing battery (sinclair valves ),,50,Review the conditions of the filters of the curing Battery مراجعة فلاتر دائرة الطبخ,P19,45,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) curing battery (sinclair valves ),,24,Review the conditions of the Vaccum & Drain valves packing مراجعة جشو بلوف الفاكيوم والدرين,P20,240,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) curing battery (sinclair valves ),,25,"Review the conditions of the hot water, infaltion & recovery valves packing مراجعة حشو بلوف الانفليشن والمياه الساخنه والريكفرى",P21,240,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) curing battery (sinclair valves ),,26,Review the conditions of the piping leakage and its conditions. مراجعة تسريبات المواسير,P22,180,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
A0,(C) curing battery (sinclair valves ),,27,"Review the conditions of the non-retune valves conditions of the curing battery ( dome circuit and hot water,…) مراجعةوتنظيف فلاتر دوائر الطبخ",P23,240,1M,32,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
"""

# Read the template data
df = pd.read_csv(io.StringIO(csv_data))

# 1. Define the full list of 87 machines
machines = []
machines.extend([f"A{i}" for i in range(9)])    # A0-A8
machines.extend([f"B{i}" for i in range(1, 9)]) # B1-B8
machines.extend([f"C{i}" for i in range(1, 9)]) # C1-C8
machines.extend([f"D{i}" for i in range(1, 9)]) # D1-D8
machines.extend([f"E{i}" for i in range(1, 10)]) # E1-E9
machines.extend([f"F{i}" for i in range(1, 10)]) # F1-F9
machines.extend([f"G{i}" for i in range(1, 10)]) # G1-G9
machines.extend([f"H{i}" for i in range(1, 10)]) # H1-H9
machines.extend([f"I{i}" for i in range(1, 10)]) # I1-I9
machines.extend([f"J{i}" for i in range(1, 10)]) # J1-J9

print(f"Total machines generated: {len(machines)}")

# 2. Create the master DataFrame
# Replicate the task list (rows) for every machine
all_rows = []
for m in machines:
    m_df = df.copy()
    m_df['Curing Press'] = m  # Update machine name
    all_rows.append(m_df)

final_df = pd.concat(all_rows, ignore_index=True)

# 3. Clean and Initialize Week Columns
# Ensure columns W1 to W52 exist and are empty initially
w_cols = [f'W{i}' for i in range(1, 53)]
for w in w_cols:
    final_df[w] = ""

# 4. Apply Scheduling Logic
# 2 machines per week, wrapping around after 87 machines.
# Logic: Week 1 -> Indices 0, 1. Week 2 -> Indices 2, 3...
for w in range(1, 53):
    # Calculate the indices of the two machines for this week
    idx1 = (2 * (w - 1)) % len(machines)
    idx2 = (2 * (w - 1) + 1) % len(machines)
    
    m1 = machines[idx1]
    m2 = machines[idx2]
    
    # Mark 'X' in the current week column for these two machines
    mask = final_df['Curing Press'].isin([m1, m2])
    final_df.loc[mask, f'W{w}'] = "X"

# 5. Save to CSV
output_filename = 'mech_curing_press_schedule.csv'
# utf-8-sig ensures Arabic characters are displayed correctly in Excel
final_df.to_csv(output_filename, index=False, encoding='utf-8-sig')

print(f"Schedule generated successfully: {output_filename}")