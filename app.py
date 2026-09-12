import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="حضور متوسطة الثغر", layout="wide")

st.markdown("<h2 style='text-align: center;'>🏫 متوسطة الثغر النموذجية الأهلية - بنين</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>نظام تسجيل الحضور والغياب (1447-1448هـ)</h4>", unsafe_allow_html=True)
st.write("---")

# حفظ البيانات مؤقتاً في الجلسة
if 'attendance_data' not in st.session_state:
    st.session_state['attendance_data'] = []

# القائمة الجانبية للتنقل
role = st.sidebar.radio("اختر لوحة التحكم:", ["👨‍🏫 حساب المعلم", "👔 حساب الوكيل والمدير"])

if role == "👨‍🏫 حساب المعلم":
    st.subheader("📋 رصد حضور الطلاب")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        grade = st.selectbox("الصف الدراسي:", ["الأول المتوسط", "الثاني المتوسط", "الثالث المتوسط"])
    with col2:
        section = st.selectbox("الفصل:", ["فصل 1", "فصل 2", "فصل 3"])
    with col3:
        period = st.selectbox("الحصة:", [f"الحصة {i}" for i in range(1, 8)])
    with col4:
        att_date = st.date_input("التاريخ:", date.today())

    st.write(f"**رصد الحصة:** {period} | **الفصل:** {grade} - {section}")
    
    # قائمة طلاب تجريبية (يمكن استبدالها بقاعدة البيانات كاملة)
    sample_students = ["بلال عبدالرزاق العيسى", "جاسر بن عبدالله الحارثي", "حسام بن محمد البارقي", "ريان عبدالله الأسمري"]
    
    attendance_status = {}
    for student in sample_students:
        status = st.radio(
            f"الطالب: **{student}**", 
            ["حاضر", "غائب", "خارج الفصل", "متأخر"], 
            key=f"{grade}_{section}_{period}_{student}",
            horizontal=True
        )
        attendance_status[student] = status
        
    if st.button("💾 حفظ التحضير"):
        for student, status in attendance_status.items():
            st.session_state['attendance_data'].append({
                "التاريخ": str(att_date),
                "الصف": grade,
                "الفصل": section,
                "الحصة": period,
                "اسم الطالب": student,
                "الحالة": status
            })
        st.success("تم حفظ بيانات الحضور بنجاح!")

else:
    st.subheader("👔 لوحة الوكيل والمدير (المتابعة الإدارية)")
    df = pd.DataFrame(st.session_state['attendance_data'])
    
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("إجمالي الغياب", len(df[df['الحالة'] == 'غائب']))
        c2.metric("إجمالي المتأخرين", len(df[df['الحالة'] == 'متأخر']))
        c3.metric("خارج الفصل", len(df[df['الحالة'] == 'خارج الفصل']))
        c4.metric("الحاضرون", len(df[df['الحالة'] == 'حاضر']))
        
        st.write("---")
        t1, t2, t3 = st.tabs(["❌ قائمة الغياب", "⏰ المتأخرون", "🚪 خارج الفصل"])
        with t1:
            st.dataframe(df[df['الحالة'] == 'غائب'], use_container_width=True)
        with t2:
            st.dataframe(df[df['الحالة'] == 'متأخر'], use_container_width=True)
        with t3:
            st.dataframe(df[df['الحالة'] == 'خارج الفصل'], use_container_width=True)
    else:
        st.info("لا توجد بيانات حضور مرصودة حالياً.")
