import pandas as pd
import io

# 1. Template Data (Tasks for one machine)
csv_data = """Curing Press,Sub_Machine,.,Task_Description,Task_Code,Estimated_mins,Crew,Period_freq
A0,بريشر سويتش,1,تنظيف ال PS من الماء أو أى طبقة ملوثة على أطراف التوصيل,1.1,10,1E,24
A0,بريشر سويتش,2,اعادة تثبيت أطراف التوصيل,1.2,10,1E,24
A0,بريشر سويتش,3,تصفية خط ال PS,1.3,10,1M,24
A0,بريشر سويتش,4,ضبط ال PS على قيمة الضبط  (Set Point),1.4,10,1E,24
A0,كونتاكتور الموتور,5,التأكد من الحركة الميكانيكية لكونتاكتور التحكم و تنظيفه بسبراى و تغييره اذا لزم الأمر,2.1,30,1E,24
A0,كونتاكتور الموتور,6,اعادة تربيط و تثبيت أطراف التوصيل,2.2,10,1E,24
A0,ريلاى التحكم,7,التأكد من الحركة الميكانيكية لريلاى التحكم و تنظيفه بسبراى و تغييره اذا لزم الأمر,3.1,20,1E,24
A0,ريلاى التحكم,8,اعادة تربيط و تثبيت أطراف التوصيل,3.2,10,1E,24
A0,البانل الرئيسية,9,تنظيف البانل من الداخل باستخدام بلاور,4.1,10,1E,24
A0,البانل الرئيسية,10,التأكد من سلامة التوصيل لجميع مكونات القوى أو التحكم ( قاطع الدائرة – الريلاى – الروزيتة – الكونتاكتور ),4.2,20,1E,24
A0,فرامل الموتور,20,التأكد من سلامة ديسك الفرامل و تغييره اذا لزم الأمر,8.1,20,1E,24
A0,فرامل الموتور,21,ضبط الجاب الخاصة بالفرامل,8.2,10,1E,24
A0,الليمت سويتشات & الانكودر,22,التأكد من سلامة توصيل  الأسلاك الخاصة بالانكودر و اعادة تثبيت و توصيل الأسلاك الغير مثبتة جيدا,9.1,10,1E,24
A0,الليمت سويتشات & الانكودر,23,التأكد من سلامة كابلينج الانكودر و تغييره اذا لزم الأمر,9.2,10,2E,24
A0,الليمت سويتشات & الانكودر,24,اعادة تثبيت و توصيل الأسلاك,9.3,10,1e,24
A0,الليمت سويتشات & الانكودر,25,التأكد من سلامة الليمت سويتش و تغييره اذا لزم الأمر,9.4,60,1E,24
A0,الليمت سويتشات & الانكودر,26,ضبط وضع و مستوى الليمت سويتش,9.5,10,2E,24
A0,لمبات التوضيح,27,التأكد من سلامة لمبات التوضيح الموجودة بالبانل و تغيير التالف منهم,10.1,10,1E,24
A0,لمبات التوضيح,28,التأكد من سلامة لمبات التوضيح الموجودة أعلى و أسفل البانل و تغيير التالف منهم,10.2,10,1E,24
A0,السيلكتور سويتش,29,التأكد من سلامة التوصيل الخاص بالسيلكتور سويتش و تغيير التالف منه,12.1,10,1E,24
A0,السيلكتور سويتش,30,اعادة ثتبيت الأسلاك الغير مثبتة جيدا,12.3,10,1E,24
A0,البانل الرئيسية,11,  التأكد من سلامة الكابلات من و الى البانل,4.3,10,1E,24
A0,البانل الرئيسية,12,التأكد من سلامة قاطع الدائرة,4.4,10,1E,24
A0,بانل الPLC,13,توصيل و تثبيت المكونات الداخلية لل PLC,5.1,10,1E,24
A0,بانل الPLC,14,تنظيف المكونات الداخلية لل PLC من الأتربة باستخدام سبراى مناسب,5.2,10,1E,24
A0,وحدة التكييف,15,التأكد من أن وحدة التكييف تعمل بحالة جيدة,6.1,10,1E,24
A0,مؤشر الديجيتال,16,تنظيف الكارت الخاص بمؤشر الديجيتال باستخدام سبراى منماسب,7.1,20,1E,24
A0,مؤشر الديجيتال,17,اعادة تثبيت و توصيل الأسلاك,7.2,10,1M,24
A0,مؤشر الديجيتال,18,تصفية خط  محول الضغط (Transducer) الموصل الى مؤشر الديجيتال,7.3,5,1E,24
A0,مؤشر الديجيتال,19,ضبط قراءة مؤشر الديجيتال,7.4,10,1E,24
"""

# Read template
df_template = pd.read_csv(io.StringIO(csv_data))
task_cols = ['Sub_Machine', '.', 'Task_Description', 'Task_Code', 'Estimated_mins', 'Crew', 'Period_freq']
template_tasks = df_template[task_cols].copy()

# 2. Generate Machine List (A0-A8, B1-B8 ... J1-J9)
machines = []
machines.extend([f"A{i}" for i in range(0, 9)])
machines.extend([f"B{i}" for i in range(1, 9)])
machines.extend([f"C{i}" for i in range(1, 9)])
machines.extend([f"D{i}" for i in range(1, 9)])
machines.extend([f"E{i}" for i in range(1, 10)])
machines.extend([f"F{i}" for i in range(1, 10)])
machines.extend([f"G{i}" for i in range(1, 10)])
machines.extend([f"H{i}" for i in range(1, 10)])
machines.extend([f"I{i}" for i in range(1, 10)])
machines.extend([f"J{i}" for i in range(1, 10)])

# 3. Build Schedule Rows
final_rows = []
week_cols = [f"W{i}" for i in range(1, 53)]

for idx, machine in enumerate(machines):
    start_week = (idx // 2) + 1  # 2 machines per week
    
    for _, task_row in template_tasks.iterrows():
        new_row = {'Curing Press': machine}
        # Copy task details
        for col in task_cols:
            new_row[col] = task_row[col]
            
        # Set weeks (x)
        for w in week_cols:
            new_row[w] = ""
            
        # Add maintenance cycle (Start Week + every 24 weeks)
        period = 24
        current_week = start_week
        while current_week <= 52:
            new_row[f"W{current_week}"] = "x"
            current_week += period
            
        final_rows.append(new_row)

# 4. Save to CSV
all_cols = ['Curing Press'] + task_cols + week_cols
df_final = pd.DataFrame(final_rows, columns=all_cols)
df_final.to_csv('complete_maintenance_schedule.csv', index=False, encoding='utf-8-sig')

print("Done! File 'complete_maintenance_schedule.csv' created.")