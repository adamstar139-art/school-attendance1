import streamlit as st
import pandas as pd
from datetime import date
import io

### ---------------------------------------------------------
### 1. إعدادات الصفحة والتصميم الاحترافي (Custom CSS)
### ---------------------------------------------------------
st.set_page_config(
    page_title="نظام تحضير متوسطة الثغر النموذجية",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيقات الهوية البصرية والمحاذاة لمدارس الثغر
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* تصميم الترويسة الرئيسية */
    .header-box {
        background: linear-gradient(135deg, #0F2552 0%, #1E3A8A 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(15, 37, 82, 0.2);
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 4px solid #D97706;
    }
    .header-text {
        text-align: right;
    }
    .header-title {
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        color: #FFFFFF;
    }
    .header-subtitle {
        font-size: 16px;
        color: #E2E8F0;
        margin-top: 5px;
        font-weight: 600;
    }
    
    /* تنسيق بطاقة الطالب */
    .student-card {
        text-align: right;
        direction: rtl;
        padding: 4px 0;
    }
    .student-name {
        font-size: 15px;
        font-weight: 700;
        color: #1E293B;
    }
    .student-id {
        font-size: 12px;
        color: #64748B;
        font-weight: 600;
        display: block;
        margin-top: 2px;
    }

    /* تنسيق الهيكل الإداري في القائمة الجانبية */
    .sidebar-admin-box {
        background-color: #F8FAFC;
        border-right: 4px solid #0F2552;
        border-radius: 8px;
        padding: 12px 15px;
        margin-top: 20px;
        text-align: right;
        direction: rtl;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .sidebar-admin-title {
        color: #0F2552;
        font-weight: 800;
        font-size: 15px;
        margin-bottom: 8px;
    }
    .sidebar-admin-item {
        font-size: 13px;
        color: #334155;
        margin: 4px 0;
    }
</style>
""", unsafe_allow_html=True)

### ---------------------------------------------------------
### 2. الترويسة والشعار المعتمد لمدارس الثغر
### ---------------------------------------------------------
header_html = """
<div class="header-box">
    <div class="header-text">
        <div class="header-title">متوسطة الثغر النموذجية الأهلية - بنين</div>
        <div class="header-subtitle">نظام رصد ومتابعة الحضور والغياب اليومي (1447 - 1448هـ)</div>
    </div>
    <div>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 220" width="160" height="70">
            <path d="M250 20 L400 100 L250 180 L100 100 Z" fill="#D97706" />
            <text x="250" y="115" font-family="'Cairo', sans-serif" font-size="32" font-weight="bold" fill="#FFFFFF" text-anchor="middle">الثغر</text>
        </svg>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

### ---------------------------------------------------------
### 3. قوائم المعلمين وطلاب المدرسة الكلية (167 طالباً)
### ---------------------------------------------------------
TEACHERS_LIST = [
    "محمد سامي السعيد", "علي محمد معوض", "أحمد عبد الحميد سعيد", "محمد عبد المنعم أبو كيلة",
    "هيثم رضا عطية", "عماد الدين نصر كرم", "السيد الغريب بدوي", "محمد إبراهيم عبد الرحمن",
    "أسامة أحمد سالم", "عماد بكر عارف", "إبراهيم علي العتيبي", "عيسى خالد العويس", "زيد بن علي التميمي"
]

STUDENTS_DB = {
    "الأول المتوسط": {
        "أول أول (فصل 1)": [
            {"id": "2395664317", "name": "بلال عبدالرزاق عيسى العيسى"},
            {"id": "1170970741", "name": "جاسر بن عبدالله بن منصور العطار الحارثي"},
            {"id": "1170582165", "name": "حسام بن محمد بن علي ال رايان البارقي"},
            {"id": "1169004353", "name": "ريان عبدالله جابر الأسمري"},
            {"id": "2446713998", "name": "زيد زياد عبد اللطيف أبو قبع"},
            {"id": "2527104554", "name": "سامي سعد عباس حمد"},
            {"id": "1170111759", "name": "سعد ناصر سعد السيف"},
            {"id": "1153310501", "name": "عبدالله بن سليمان بن عبدالله الراجحي"},
            {"id": "1170836520", "name": "عبدالله سعد بن محمد العيشان"},
            {"id": "1171448515", "name": "علي احمد علي كريري"},
            {"id": "1170853053", "name": "علي سعد علي القحطاني"},
            {"id": "1172018036", "name": "عمر عبدالله سعد الجبرين"},
            {"id": "2552851368", "name": "مازن اسلام احمد ابراهيم موسى"},
            {"id": "013609321", "name": "محمد أحمد علي عقيل"},
            {"id": "2502333707", "name": "محمد اسلام محمد دراز"},
            {"id": "2394606749", "name": "محمد اشرف مسعود ابواخاطر"},
            {"id": "1169174164", "name": "محمد نايف فراج الدعجاني"},
            {"id": "2380890976", "name": "وائل -- بولعيش"}
        ],
        "أول ثاني (فصل 2)": [
            {"id": "1167628468", "name": "ابراهيم بن محمد بن علي الوهيبي"},
            {"id": "1170348286", "name": "الوليد ابن خالد بن فهد العتيبي"},
            {"id": "1172433185", "name": "باسل محمد فرج الدوسري"},
            {"id": "1173391556", "name": "بسام بن عبدالكريم بن عبدالله الحرقان الدوسري"},
            {"id": "1169185053", "name": "تركي عبدالله مسفر الدوسري"},
            {"id": "1170108078", "name": "تميم فهد عبدالعزيز العزاز"},
            {"id": "1168982427", "name": "راكان عبدالله يحي كريري"},
            {"id": "1172590968", "name": "ريان عبدالله منصور السبر"},
            {"id": "2392863888", "name": "ريان وليد - حلاق"},
            {"id": "1170420473", "name": "سيف عبدالكريم بريك العصيمي"},
            {"id": "1168942108", "name": "صالح حسن فتحى سندى"},
            {"id": "1173182138", "name": "عبدالرحمن ابراهيم عبدالله الحضيف"},
            {"id": "1172448548", "name": "عبدالله صالح حمد الصفيان"},
            {"id": "1170000945", "name": "فهد ابن احمد بن فهد العثمان"},
            {"id": "1167092616", "name": "فهد عويض ثعيل المطيري"},
            {"id": "1170413171", "name": "فهد نايف فهد الحسينان"},
            {"id": "1170294118", "name": "فيصل موينع عبدالله بن موينع"},
            {"id": "1171524604", "name": "فيصل ناصر سيف العريفي"},
            {"id": "1170374993", "name": "مشاري عثمان سعد ناصر السعد"},
            {"id": "1170884165", "name": "يزن محمد علي اليحيى"},
            {"id": "1170548737", "name": "يوسف محمد عبدالله الدوسري"}
        ]
    },
    "الثاني المتوسط": {
        "ثاني أول (فصل 1)": [
            {"id": "1163613795", "name": "ابراهيم ياسر ابراهيم الحلوى"},
            {"id": "1163760935", "name": "احمد سامي بن احمد العمران"},
            {"id": "1153756612", "name": "الوليد عبدالله بن ابراهيم المبدل"},
            {"id": "1164269209", "name": "ذياب بن محمد بن ذياب بن مريطع القحطاني"},
            {"id": "1163187972", "name": "راكان سالم بن مسفر القحطاني"},
            {"id": "1167623758", "name": "سلطان عبدالله حسن القحطاني"},
            {"id": "1164769430", "name": "عبدالرحمن حمد بن محمد العريفي"},
            {"id": "1167893740", "name": "عبدالرحمن ربيع جابر خبراني"},
            {"id": "1159740032", "name": "عبدالعزيز سعود بن فهد العتيبي"},
            {"id": "1164277830", "name": "عبداللطيف ابراهيم محمد الطمره"},
            {"id": "1162761306", "name": "فهد عيسى محمد العيسى"},
            {"id": "1160901128", "name": "فيصل بن عبدالله بن سعود بن عبدالعزيز الجمعه"},
            {"id": "1162168627", "name": "مبارك صالح مبارك هليل"},
            {"id": "1163212978", "name": "محمد بن عبدالله بن حمد بن ناصر بن عمران"},
            {"id": "1161858301", "name": "محمد عبدالمحسن ناصر الحزام"},
            {"id": "1175902442", "name": "محمد فايز عبدالرحمن بن يوسف"},
            {"id": "1165686179", "name": "مشاري سلطان سالم الشمراني"},
            {"id": "1166040053", "name": "معاذ عبدالله سعود العريفي"},
            {"id": "1167081981", "name": "ناصر حسين محمد ال جبران"},
            {"id": "1163191222", "name": "يزيد بن طارق بن علي الحديثي"}
        ],
        "ثاني ثاني (فصل 2)": [
            {"id": "1166753291", "name": "ابراهيم بن مبارك بن راشد بن عبدالرحمن السبعان آل موينع"},
            {"id": "1167148251", "name": "حامد بن محمد بن حامد شباط"},
            {"id": "1164599977", "name": "حسام حسن محمد الشهري"},
            {"id": "1169057351", "name": "خالد تركي عايض القحطاني"},
            {"id": "1164120600", "name": "خالد داود بن عابد الحارثي"},
            {"id": "1165839455", "name": "سطام عبدالعزيز عبدالله العريفي"},
            {"id": "1171617069", "name": "سعود خالد عبدالله الحمد"},
            {"id": "1163778960", "name": "سعود سلطان بن خليل العتيبي"},
            {"id": "1163458878", "name": "سعود مشعل بن ابراهيم الشثري"},
            {"id": "1166582989", "name": "طلال محمد منير المهدرس"},
            {"id": "1165143783", "name": "عبدالكريم مساعد عبدالعزيز الهزاع"},
            {"id": "1165495258", "name": "عبدالله سامي سعد الحوشاني"},
            {"id": "013609088", "name": "علي أحمد علي عقيل"},
            {"id": "1164825802", "name": "عمر بن سعد بن هلال الشبانات"},
            {"id": "3787591993", "name": "عمر خالد عبدالله المهيني"},
            {"id": "1163537838", "name": "فارس مشعل عبدالله بن موينع"},
            {"id": "1164997858", "name": "مازن خالد دخيل المطيري"},
            {"id": "2348937422", "name": "مازن رفعت محمد حاج النيل"},
            {"id": "1166803245", "name": "نايف بن بندر بن خلفان العلوي"},
            {"id": "1165668417", "name": "نواف عبدالعزيز مرزوق المرزوق"},
            {"id": "1164387977", "name": "هادي سلطان هادي القحطاني"},
            {"id": "1165002153", "name": "يزيد بن حسين بن متعب بن محمد كعكم"}
        ],
        "ثاني ثالث (فصل 3)": [
            {"id": "1166911709", "name": "ثامر عمر ابراهيم عثمان"},
            {"id": "008464815", "name": "جهاد فارس عبدالقادر حتاوي"},
            {"id": "1164830562", "name": "خالد محمد عبدالكريم الخفاجي"},
            {"id": "1188914319", "name": "سعد ابن مسفر بن سعد القحطاني"},
            {"id": "1165099498", "name": "سعود بن عبدالله بن سعود السحامي"},
            {"id": "1167770468", "name": "سعود ناصر سنيف العريفي"},
            {"id": "2344500760", "name": "سعيد محمد - باوزير"},
            {"id": "1164983874", "name": "طلال بن فهد بن عطيه بالحكم الزهراني"},
            {"id": "2362260263", "name": "عبدالرحمن احمد جاسم الحمدي"},
            {"id": "1167153434", "name": "عبدالعزيز ماجد راشد الزير"},
            {"id": "1164512566", "name": "عبدالعزيز وليد ناصر بن سعران"},
            {"id": "1167267341", "name": "عبدالله بن بندر بن فهد المفيجل"},
            {"id": "1164747436", "name": "عبدالمجيد بن محمد بن مسعود آل عايض القحطاني"},
            {"id": "2358022958", "name": "عز الدين احمد محمد سعد"},
            {"id": "1167515020", "name": "عزام خالد شلهوب بن شلهوب"},
            {"id": "1164747014", "name": "عزام فهد احمد صلوي"},
            {"id": "4533080448", "name": "عمر وليد ياسين درويش علي"},
            {"id": "1163397811", "name": "فارس ابن محمد بن سالم بن نويشي الوهبي الحربي"},
            {"id": "1172720045", "name": "محمد بن علي محسن العثيميني"},
            {"id": "1171868639", "name": "وائل بن عبدالله بن عامر علي ال عبيد الغامدي"},
            {"id": "1166629798", "name": "يزيد بن حمد بن مترك بن محمد ال مسعود القحطاني"},
            {"id": "1167371093", "name": "يوسف عايد عواد البلوي"}
        ]
    },
    "الثالث المتوسط": {
        "ثالث أول (فصل 1)": [
            {"id": "1158966166", "name": "أصيل ناصر بن محمد مذكور"},
            {"id": "1162308223", "name": "خالد محمد مسدف معافا"},
            {"id": "1159155223", "name": "راشد سعيد راشد عبدالسلام"},
            {"id": "1161109093", "name": "راكان بن عبدالله بن سالم اليافعي"},
            {"id": "1160805899", "name": "زياد احمد بن علي اللحيد"},
            {"id": "1160267124", "name": "سطام محمد سعود الدوسري"},
            {"id": "1163270869", "name": "سلطان احمد صالح الفتوح"},
            {"id": "1160585624", "name": "عبدالعزيز عبدالله شراز المالكي"},
            {"id": "1160050678", "name": "عبدالعزيز عبدالله عايض الأسمري"},
            {"id": "1161021314", "name": "عبدالله عبيد عبدالله العتيبي"},
            {"id": "1160857700", "name": "عبدالله فهد جلوي سالم الشرعي"},
            {"id": "1161503857", "name": "علي ابراهيم علي الأسمري"},
            {"id": "2502333723", "name": "عماد الدين اسلام محمد دراز"},
            {"id": "1162454266", "name": "عمر فهد محمد السقامي"},
            {"id": "1161418593", "name": "فهد عبدالرحمن فهد العتيبي"},
            {"id": "1163074592", "name": "فيصل بن عبدالمحسن بن عايض العصيمي العتيبي"},
            {"id": "1165152107", "name": "فيصل محمد صالح الفتوح"},
            {"id": "1158815876", "name": "محمد سلطان عبدالعزيز العيد"},
            {"id": "1166075653", "name": "محمد مقعد ساير العتيبي"},
            {"id": "1160693949", "name": "مشاري ابراهيم عبداللطيف المغربي"},
            {"id": "1160803878", "name": "مشاري علي موسى عقيلي"},
            {"id": "1161661846", "name": "مهند عبدالله فهد الزكري"},
            {"id": "1159404795", "name": "نواف وليد حمد الشعلان"},
            {"id": "1168385894", "name": "يوسف نايف مقعد العتيبي"}
        ],
        "ثالث ثاني (فصل 2)": [
            {"id": "1156933093", "name": "تركي عبدالعزيز عبدالله المرزوق"},
            {"id": "1160223317", "name": "تركي عثمان عبدالعزيز العثمان"},
            {"id": "1159683497", "name": "راشد احمد فهد ال سعيد"},
            {"id": "2310646332", "name": "راكان ابراهيم محمد دبوان"},
            {"id": "1161397599", "name": "ريان ناصر عبدالرحمن المرشود"},
            {"id": "1163112129", "name": "صالح بن ممدوح بن صالح بن خالد الجويعي"},
            {"id": "2508581135", "name": "عبد الرحمن محمد صلاح بدر الدين"},
            {"id": "1162188872", "name": "عبدالعزيز تركي عبدالعزيز اللهيم"},
            {"id": "1161340763", "name": "عبدالعزيز عبدالمحسن فهد بن بديع"},
            {"id": "1171845140", "name": "عبدالله متعب بن عبدالرحمن الجبرين"},
            {"id": "1159200318", "name": "عبدالمحسن طارق بن عبدالرحمن العروان"},
            {"id": "1161333677", "name": "فارس وليد بن عبدالله الحوطي"},
            {"id": "1162461857", "name": "محمد خالد محمد بن مشرف"},
            {"id": "1161288897", "name": "محمد سعد بن محمد العيشان"},
            {"id": "1156334813", "name": "محمد عبدالعزيز محمد الخالدي"},
            {"id": "1162044851", "name": "مهند ماجد علي كعبي"},
            {"id": "1158021137", "name": "ناصر محمد عبدالله الزريعي"},
            {"id": "1161363443", "name": "نواف سعد بن علي القاسم"},
            {"id": "1162274086", "name": "ياسر تركي اسماعيل مسلمي"}
        ],
        "ثالث ثالث (فصل 3)": [
            {"id": "1163525544", "name": "ثامر وليد بن عبدالعزيز الطليحي"},
            {"id": "1160712996", "name": "خالد بن عبدالرؤوف بن عبدالرحمن بن عبدالله الشنير"},
            {"id": "1162560054", "name": "خالد عبدالله خالد الخالدي"},
            {"id": "1174188647", "name": "خالد محمد بن عبدالله ال درعان"},
            {"id": "1174226389", "name": "راشد صالح بن عبدالعزيز الحلوان"},
            {"id": "1167756897", "name": "رواد محمد إبراهيم الخليل"},
            {"id": "1159394046", "name": "صالح بن محمد بن صالح الميموني المطيري"},
            {"id": "1161085236", "name": "ضاري صالح مهنا العازمي"},
            {"id": "1158551372", "name": "عبدالرحمن بدر عبدالرحمن الطريقي"},
            {"id": "1195815558", "name": "عبدالرحمن خالد محمد سعيد"},
            {"id": "1158561843", "name": "عبدالله تركي عبدالله الأحمد"},
            {"id": "1159977451", "name": "عبدالله عبدالرحمن عبدالله النجراني"},
            {"id": "1162387458", "name": "علي بن خالد بن علي العجيري"},
            {"id": "1158128270", "name": "علي عبدالله علي ال حمود"},
            {"id": "1158198604", "name": "فهد بن خالد بن فهد بن عبدالعزيز الزيد"},
            {"id": "1159551264", "name": "فيصل عبدالرحمن عزيز القحطاني"},
            {"id": "1162325722", "name": "ماجد فهد عبدالعزيز الكثيري"},
            {"id": "1171918236", "name": "مازن خالد عبدربه الزهراني"},
            {"id": "1186515613", "name": "متعب مطر جمعان الدوسري"},
            {"id": "1159852746", "name": "نواف فهد بن ناصر القحطاني"},
            {"id": "1163027392", "name": "يوسف عبدالله عوض العتيبي"}
        ]
    }
}

### ---------------------------------------------------------
### 4. دالة توليد صفحة HTML المجهزة للطباعة والحفظ PDF
### ---------------------------------------------------------
def generate_printable_html(df_subset, report_title):
    rows_html = ""
    for idx, row in enumerate(df_subset.to_dict('records'), 1):
        status_color = "#DC2626" if row['الحالة'] == "غائب" else "#D97706" if row['الحالة'] in ["خارج الفصل", "خالد الفصل"] else "#CA8A04" if row['الحالة'] == "متأخر" else "#16A34A"
        teacher = row.get('اسم المعلم', 'غير محدد')
        rows_html += f"""
        <tr>
            <td>{idx}</td>
            <td style="text-align: right;"><b>{row['اسم الطالب']}</b><br><small style="color: #64748B;">الهوية: {row['رقم الطالب']}</small></td>
            <td>{row['الصف']}</td>
            <td>{row['الفصل']}</td>
            <td>{row['الحصة']}</td>
            <td>{teacher}</td>
            <td style="color: {status_color}; font-weight: bold;">{row['الحالة']}</td>
        </tr>
        """
        
    html_code = f"""
    <!DOCTYPE html>
    <html dir="rtl" lang="ar">
    <head>
    <meta charset="utf-8">
    <title>{report_title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
        body {{ font-family: 'Cairo', sans-serif; text-align: right; padding: 20px; background-color: #FFFFFF; color: #1E293B; }}
        .header {{ text-align: center; border-bottom: 3px solid #0F2552; padding-bottom: 12px; margin-bottom: 20px; }}
        h2 {{ color: #0F2552; margin: 5px; font-weight: 800; font-size: 22px; }}
        h4 {{ color: #4B5563; margin: 5px; font-weight: 700; font-size: 16px; }}
        .info {{ background-color: #F1F5F9; padding: 12px; border-radius: 8px; margin-bottom: 20px; text-align: center; font-weight: 700; border: 1px solid #CBD5E1; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
        th, td {{ border: 1px solid #CBD5E1; padding: 10px; text-align: center; font-size: 13px; }}
        th {{ background-color: #0F2552; color: white; font-weight: 700; }}
        tr:nth-child(even) {{ background-color: #F8FAFC; }}
        .footer-credits {{ margin-top: 40px; border-top: 2px solid #E2E8F0; padding-top: 20px; text-align: center; font-size: 12px; color: #475569; }}
        @media print {{
            .no-print {{ display: none; }}
        }}
    </style>
    </head>
    <body>
    <div class="no-print" style="text-align: center; margin-bottom: 20px;">
        <button onclick="window.print()" style="background-color: #0F2552; color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            🖨️ طباعة التقرير / حفظ كـ PDF
        </button>
    </div>
    <div class="header">
        <h2>متوسطة الثغر النموذجية الأهلية - بنين</h2>
        <h4>{report_title}</h4>
    </div>
    <div class="info">
        التاريخ: {date.today()} | إجمالي العدد المرصود: {len(df_subset)} طالب
    </div>
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>اسم الطالب ورقم الهوية</th>
                <th>الصف</th>
                <th>الفصل</th>
                <th>الحصة</th>
                <th>اسم المعلم</th>
                <th>الحالة</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>

    <div class="footer-credits">
        <table style="border: none; width: 100%;">
            <tr style="background: none;">
                <td style="border: none; font-weight: bold;">مدير المدرسة: إبراهيم بن موسى التميمي</td>
                <td style="border: none; font-weight: bold;">وكيل الشؤون التعليمية: محمد مبروك السيد</td>
                <td style="border: none; font-weight: bold;">وكيل شؤون الطلاب: صالح بن عبدالله الدعجاني</td>
                <td style="border: none; font-weight: bold;">تصميم الأستاذ: محمد سامي السعيد</td>
            </tr>
        </table>
    </div>
    </body>
    </html>
    """
    return html_code

### ---------------------------------------------------------
### 5. تهيئة ذاكرة البيانات
### ---------------------------------------------------------
if 'attendance_data' not in st.session_state:
    st.session_state['attendance_data'] = []

### ---------------------------------------------------------
### 6. القائمة الجانبية المحدثة
### ---------------------------------------------------------
st.sidebar.title("📌 نظام المتابعة")
role = st.sidebar.radio("اختر لوحة التحكم:", ["👨‍🏫 حساب المعلم (رصد الحضور)", "👔 حساب الوكيل والمدير (المتابعة والتصدير)"])

### ---------------------------------------------------------
### 7. واجهة المعلم (رصد الحضور)
### ---------------------------------------------------------
if role == "👨‍🏫 حساب المعلم (رصد الحضور)":
    st.subheader("📋 رصد حضور وغياب الطلاب")
    
    col_t, col_g, col_s, col_p, col_d = st.columns(5)
    with col_t:
        teacher_name = st.selectbox("اسم المعلم:", TEACHERS_LIST)
    with col_g:
        grade = st.selectbox("الصف الدراسي:", list(STUDENTS_DB.keys()))
    with col_s:
        section = st.selectbox("الفصل:", list(STUDENTS_DB[grade].keys()))
    with col_p:
        period = st.selectbox("الحصة:", [f"الحصة {i}" for i in range(1, 8)])
    with col_d:
        att_date = st.date_input("التاريخ:", date.today())

    students_list = STUDENTS_DB[grade][section]

    st.info(f"👨‍🏫 **المعلم:** {teacher_name} | 🏫 **الفصل:** {grade} - {section} | ⏰ **الحصة:** {period} | 📅 **التاريخ:** {att_date}")
    st.write("---")

    attendance_records = {}

    for idx, student in enumerate(students_list, 1):
        c_num, c_name, c_status = st.columns([0.5, 3.5, 3])
        c_num.write(f"**{idx}**")
        
        # محاذاة اسم الطالب لليمين ورقم الهوية أسفله
        c_name.markdown(
            f"""
            <div class="student-card">
                <span class="student-name">{student['name']}</span>
                <span class="student-id">رقم الطالب/الهوية: {student['id']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        status = c_status.radio(
            "حالة الحضور:",
            ["حاضر", "غائب", "خارج الفصل", "متأخر"],
            key=f"{teacher_name}_{grade}_{section}_{period}_{student['id']}",
            horizontal=True
        )
        attendance_records[student['id']] = {
            "name": student['name'],
            "status": status
        }

    st.write("---")
    if st.button("💾 حفظ وإرسال كشف الحضور", type="primary", use_container_width=True):
        for st_id, info in attendance_records.items():
            st.session_state['attendance_data'].append({
                "التاريخ": str(att_date),
                "اسم المعلم": teacher_name,
                "الصف": grade,
                "الفصل": section,
                "الحصة": period,
                "رقم الطالب": st_id,
                "اسم الطالب": info['name'],
                "الحالة": info['status']
            })
        st.success(f"تم حفظ حضور فصل ({section}) بنجاح بواسطة المعلم {teacher_name}!")

### ---------------------------------------------------------
### 8. واجهة الوكيل والمدير (مع نظام كلمة المرور adam112233)
### ---------------------------------------------------------
else:
    st.subheader("👔 لوحة الوكيل والمدير (المتابعة الإدارية والتصدير)")
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state['admin_authenticated'] = False
        
    if not st.session_state['admin_authenticated']:
        st.warning("🔒 هذه اللوحة مخصصة لإدارة المدرسة فقط. يرجى إدخال كلمة المرور للمتابعة:")
        pwd_input = st.text_input("كلمة المرور:", type="password")
        if st.button("تسجيل الدخول"):
            if pwd_input == "adam112233":
                st.session_state['admin_authenticated'] = True
                st.success("تم الدخول بنجاح!")
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة! يرجى التأكد وإعادة المحاولة.")
    else:
        if st.button("🚪 تسجيل الخروج من لوحة الإدارة"):
            st.session_state['admin_authenticated'] = False
            st.rerun()
            
        df = pd.DataFrame(st.session_state['attendance_data'])
        
        if not df.empty:
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("إجمالي السجلات المرصودة", len(df))
            m2.metric("🟢 الحاضرون", len(df[df['الحالة'] == 'حاضر']))
            m3.metric("🔴 الغياب", len(df[df['الحالة'] == 'غائب']))
            m4.metric("🟡 المتأخرون", len(df[df['الحالة'] == 'متأخر']))
            m5.metric("🟠 خارج الفصل", len(df[df['الحالة'] == 'خارج الفصل']))
            
            st.write("---")
            
            st.subheader("📥 تصدير التقرير النهائي (Excel / CSV)")
            
            excel_buffer = io.BytesIO()
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='السجل العام اليومي', index=False)
                df[df['الحالة'] == 'غائب'].to_excel(writer, sheet_name='كشف الغياب', index=False)
                df[df['الحالة'] == 'خارج الفصل'].to_excel(writer, sheet_name='خارج الفصل', index=False)
                df[df['الحالة'] == 'متأخر'].to_excel(writer, sheet_name='كشف المتأخرين', index=False)
                
            excel_data = excel_buffer.getvalue()
            
            col_down1, col_down2 = st.columns(2)
            col_down1.download_button(
                label="📊 تحميل التقرير اليومي الشامل (Excel)",
                data=excel_data,
                file_name=f"تقرير_حضور_متوسطة_الثغر_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
            col_down2.download_button(
                label="📄 تحميل التقرير كملف CSV (للحفظ والطباعة)",
                data=df.to_csv(index=False).encode('utf-8-sig'),
                file_name=f"تقرير_حضور_متوسطة_الثغر_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True
            )

            st.write("---")
            
            tab_absent, tab_out, tab_late, tab_all = st.tabs([
                "🔴 كشف الطلاب الغائبين (بالأسماء)", 
                "🟠 كشف الطلاب خارج الفصل (بالأسماء)", 
                "🟡 كشف المتأخرين عن الحصة", 
                "📋 السجل العام الشامل"
            ])
            
            with tab_absent:
                df_absent = df[df['الحالة'] == 'غائب']
                st.markdown(f"### 🔴 قائمة أسماء الطلاب الغائبين اليوم (`العدد: {len(df_absent)} طالب`)")
                if not df_absent.empty:
                    st.dataframe(df_absent[['اسم الطالب', 'رقم الطالب', 'الصف', 'الفصل', 'الحصة', 'اسم المعلم', 'التاريخ']], use_container_width=True)
                    
                    html_absent = generate_printable_html(df_absent, "كشف أسماء الطلاب الغائبين")
                    st.download_button(
                        label="🖨️ فتح صفحة طباعة كشف الغائبين (PDF)",
                        data=html_absent.encode('utf-8'),
                        file_name=f"كشف_الطلاب_الغائبين_{date.today()}.html",
                        mime="text/html",
                        key="btn_print_absent"
                    )
                else:
                    st.success("🎉 لا يوجد طلاب غائبون مسجلون اليوم!")

            with tab_out:
                df_out = df[df['الحالة'] == 'خارج الفصل']
                st.markdown(f"### 🟠 قائمة أسماء الطلاب المسجلين خارج الفصل (`العدد: {len(df_out)} طالب`)")
                if not df_out.empty:
                    st.dataframe(df_out[['اسم الطالب', 'رقم الطالب', 'الصف', 'الفصل', 'الحصة', 'اسم المعلم', 'التاريخ']], use_container_width=True)
                    
                    html_out = generate_printable_html(df_out, "كشف أسماء الطلاب المتواجدين خارج الفصل")
                    st.download_button(
                        label="🖨️ فتح صفحة طباعة كشف خارج الفصل (PDF)",
                        data=html_out.encode('utf-8'),
                        file_name=f"كشف_الطلاب_خارج_الفصل_{date.today()}.html",
                        mime="text/html",
                        key="btn_print_out"
                    )
                else:
                    st.success("✅ لا يوجد طلاب مسجلون خارج الفصل حالياً!")

            with tab_late:
                df_late = df[df['الحالة'] == 'متأخر']
                st.markdown(f"### 🟡 قائمة أسماء الطلاب المتأخرين عن الحصة (`العدد: {len(df_late)} طالب`)")
                if not df_late.empty:
                    st.dataframe(df_late[['اسم الطالب', 'رقم الطالب', 'الصف', 'الفصل', 'الحصة', 'اسم المعلم', 'التاريخ']], use_container_width=True)
                    
                    html_late = generate_printable_html(df_late, "كشف أسماء الطلاب المتأخرين عن الحصة")
                    st.download_button(
                        label="🖨️ فتح صفحة طباعة كشف المتأخرين (PDF)",
                        data=html_late.encode('utf-8'),
                        file_name=f"كشف_الطلاب_المتأخرين_{date.today()}.html",
                        mime="text/html",
                        key="btn_print_late"
                    )
                else:
                    st.success("✨ لا يوجد طلاب متأخرون مرصودون اليوم!")

            with tab_all:
                st.markdown("### 📋 السجل اليومي العام للرصد")
                st.dataframe(df, use_container_width=True)
                
                html_full = generate_printable_html(df, "التقرير اليومي الشامل لحضور وغياب الطلاب")
                st.download_button(
                    label="🖨️ فتح صفحة طباعة السجل العام (PDF)",
                    data=html_full.encode('utf-8'),
                    file_name=f"التقرير_اليومي_الشامل_{date.today()}.html",
                    mime="text/html",
                    key="btn_print_full"
                )
                
        else:
            st.info("لا توجد بيانات حضور مرصودة اليوم حتى الآن. سيتم عرض الإحصائيات وأزرار التصدير والطباعة فور بدء المعلمين في رصد الحضور.")

### ---------------------------------------------------------
### 9. الهيكل الإداري المحاذى لليمين في الشريط الجانبي
### ---------------------------------------------------------
st.sidebar.markdown("""
<div class="sidebar-admin-box">
    <div class="sidebar-admin-title">🏫 الهيكل الإداري للمدرسة</div>
    <div class="sidebar-admin-item"><b>مدير المدرسة:</b> إبراهيم بن موسى التميمي</div>
    <div class="sidebar-admin-item"><b>وكيل الشؤون التعليمية:</b> محمد مبروك السيد</div>
    <div class="sidebar-admin-item"><b>وكيل شؤون الطلاب:</b> صالح بن عبدالله الدعجاني</div>
    <hr style="margin: 8px 0; border: 0; border-top: 1px solid #E2E8F0;">
    <div class="sidebar-admin-item" style="color: #64748B; font-size: 11px;">تصميم الأستاذ: محمد سامي السعيد</div>
</div>
""", unsafe_allow_html=True)
