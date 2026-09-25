import streamlit as st
import pandas as pd
import urllib.parse
import requests

# 1. إعدادات الصفحة والنمط البصري (Design & Theme)
st.set_page_config(
    page_title="زواج مبارك - نظام إرسال الدعوات عبر UltraMsg",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق تنسيقات CSS مخصصة لتوحيد حجم ونوع الخط لكافة الأسماء (القديمة والجديدة)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #FAFAFA;
    }
    
    /* ترويسة البرنامج */
    .wedding-header {
        background: linear-gradient(135deg, #1B3B36 0%, #0D1F1D 100%);
        border: 2px solid #D4AF37;
        padding: 25px;
        border-radius: 18px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.15);
    }
    
    .wedding-title {
        font-family: 'Amiri', serif !important;
        font-size: 40px;
        color: #D4AF37;
        margin-top: 5px;
        margin-bottom: 5px;
        font-weight: bold;
    }

    .saudi-avatar {
        font-size: 65px;
        line-height: 1;
    }

    /* البطاقات */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-right: 5px solid #D4AF37;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    .preview-box {
        background-color: #F4F7F6;
        border: 1px dashed #D4AF37;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
    }

    /* توحيد خط وحجم أسماء وقائمة المدعوين بشكل دقيق وموحد */
    .guest-item-name {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        color: #1B3B36 !important;
        margin: 0;
        padding-top: 5px;
    }

    .guest-item-phone {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 15px !important;
        color: #666666 !important;
        direction: ltr;
        display: inline-block;
        margin: 0;
        padding-top: 5px;
    }

    /* أزرار الإرسال */
    .btn-wa-open {
        background-color: #25D366;
        color: white !important;
        padding: 7px 14px;
        border-radius: 6px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 14px;
        display: inline-block;
        text-align: center;
        width: 100%;
    }
    
    .btn-wa-open:hover {
        background-color: #1EBE5D;
    }
</style>
""", unsafe_allow_html=True)

# 2. تهيئة حالة الجلسة والبيانات التجريبية
if 'invitees' not in st.session_state:
    st.session_state.invitees = pd.DataFrame([
        {"الاسم": "عبد الله بن خالد الدوسري", "الجوال": "966501234567"},
        {"الاسم": "محمد بن أحمد القحطاني", "الجوال": "966559876543"},
        {"الاسم": "فهد بن سليم العتيبي", "الجوال": "966541122334"},
        {"الاسم": "سلمان بن عبد العزيز الشمري", "الجوال": "966567788990"}
    ])

if 'ultramsg_instance' not in st.session_state:
    st.session_state.ultramsg_instance = "instance10000"  # معرف الحساب التجريبي من UltraMsg
if 'ultramsg_token' not in st.session_state:
    st.session_state.ultramsg_token = "your_token_here"  # رمز التوثيق التجريبي

# 3. الترويسة الاحترافية
st.markdown("""
<div class="wedding-header">
    <div class="saudi-avatar">🧔🏻‍♂️💍</div>
    <div class="wedding-title">زواج مبارك</div>
    <p style="font-size: 17px; color: #E0E0E0; margin: 0;">نظام إرسال وتدبير دعوات الزفاف عبر خدمة UltraMsg</p>
</div>
""", unsafe_allow_html=True)

# 4. لوحة التحكم والشريط الجانبي (إعدادات UltraMsg)
with st.sidebar:
    st.header("⚙️ إعدادات UltraMsg")
    st.info("احصل على البيانات من لوحة التحكم في ultramsg.com")
    
    instance_id = st.text_input("معرف الحساب (Instance ID):", value=st.session_state.ultramsg_instance, help="مثال: instance10000")
    token_id = st.text_input("رمز التوثيق (Token):", value=st.session_state.ultramsg_token, type="password")
    
    if st.button("حفظ إعدادات الربط"):
        st.session_state.ultramsg_instance = instance_id.strip()
        st.session_state.ultramsg_token = token_id.strip()
        st.success("تم حفظ إعدادات UltraMsg بنجاح!")

    st.markdown("---")
    st.subheader("📁 تغذية بيانات المدعوين")
    uploaded_file = st.file_uploader("رفع ملف Excel أو CSV بالمدعوين:", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_new = pd.read_csv(uploaded_file, dtype=str)
            else:
                df_new = pd.read_excel(uploaded_file, dtype=str)
            st.session_state.invitees = df_new
            st.success("تم تحميل القائمة الجديدة بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# 5. القسم الرئيسي: صياغة الرسالة والمعاينة
col_msg, col_preview = st.columns(2)

with col_msg:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("✉️ صياغة نص الدعوة وإرفاق الصورة")
    
    msg_template = st.text_area(
        "نص الرسالة الأساسي:",
        value="ندعوكم لـحضور حفل زفافنا وتناول طعام العشاء، وبحضوركم تكتمل فرحتنا وسرورنا. نسعد بتلبيتكم الدعوة.",
        height=130
    )
    
    invitation_image = st.file_uploader("إرفاق صورة بطاقة الدعوة (تظهر أسفل النص):", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("👁️ معاينة الرسالة للمدعو")
    
    sample_name = st.session_state.invitees.iloc[0]["الاسم"] if not st.session_state.invitees.empty else "سعادة الضيف"
    full_sample_msg = f"المكرم / {sample_name}\n{msg_template}"
    
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.markdown(f"**نص الرسالة:**\n\n`{full_sample_msg}`")
    
    if invitation_image is not None:
        st.image(invitation_image, caption="صورة بطاقة الدعوة المرفقة", use_container_width=True)
    else:
        st.info("💡 يمكنك إرفاق صورة بطاقة الفرح لتظهر هنا أسفل النص.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. إدارة قائمة المدعوين والإرسال
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.subheader("👥 قائمة المدعوين وإجراءات الإرسال")

# نموذج إضافة شخص جديد بتنسيق موحد
with st.expander("➕ إضافة مدعو جديد للقائمة"):
    with st.form("add_person_form"):
        col_a, col_b = st.columns(2)
        new_name = col_a.text_input("اسم الشخص:")
        new_phone = col_b.text_input("رقم الجوال (مع الرمز الدولي بدون +):", placeholder="966500000000")
        submit_add = st.form_submit_button("إضافة المدعو")
        
        if submit_add and new_name and new_phone:
            new_row = pd.DataFrame([{"الاسم": new_name.strip(), "الجوال": new_phone.strip()}])
            st.session_state.invitees = pd.concat([st.session_state.invitees, new_row], ignore_index=True)
            st.success(f"تمت إضافة {new_name} بنجاح بتنسيق موحد!")
            st.rerun()

# عرض القائمة والتنسيق الموحد للخط
if not st.session_state.invitees.empty:
    for idx, row in st.session_state.invitees.iterrows():
        c_name, c_phone, c_send_app, c_send_bg, c_actions = st.columns([2.5, 2, 2, 2, 1.2])
        
        person_name = str(row["الاسم"])
        person_phone = str(row["الجوال"]).strip()
        personalized_text = f"المكرم / {person_name}\n{msg_template}"
        encoded_text = urllib.parse.quote(personalized_text)
        wa_link = f"https://wa.me/{person_phone}?text={encoded_text}"
        
        # تطبيق التنسيق الموحد للأسماء القديمة والجديدة بنفس الحجم والنوع
        c_name.markdown(f'<p class="guest-item-name">{idx + 1}. {person_name}</p>', unsafe_allow_html=True)
        c_phone.markdown(f'<p class="guest-item-phone">📱 {person_phone}</p>', unsafe_allow_html=True)
        
        # 1. إرسال بفتح التطبيق
        c_send_app.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa-open">💬 فتح الواتساب</a>', unsafe_allow_html=True)
        
        # 2. إرسال عبر UltraMsg بدون فتح التطبيق
        if c_send_bg.button("🚀 إرسال UltraMsg", key=f"send_um_{idx}"):
            inst = st.session_state.ultramsg_instance
            tok = st.session_state.ultramsg_token
            
            if inst == "instance10000" or tok == "your_token_here":
                st.warning("يرجى إدخال Instance ID و Token الخاصين بحسابك في UltraMsg من الشريط الجانبي أولاً.")
            else:
                # رابط API الخاص بـ UltraMsg لإرسال الرسائل النصية
                api_url = f"https://api.ultramsg.com/{inst}/messages/chat"
                payload = f"token={tok}&to={person_phone}&body={urllib.parse.quote(personalized_text)}"
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                
                try:
                    res = requests.post(api_url, data=payload.encode('utf-8'), headers=headers, timeout=10)
                    res_json = res.json()
                    if "sent" in str(res_json).lower() or res_json.get("status") == "success" or "id" in res_json:
                        st.toast(f"تم إرسال الدعوة عبر UltraMsg إلى {person_name} بنجاح!", icon="✅")
                    else:
                        st.toast(f"نتيجة UltraMsg: {res_json}", icon="ℹ️")
                except Exception as e:
                    st.error(f"خطأ أثناء الاتصال بـ UltraMsg: {e}")

        # 3. حذف الشخص
        if c_actions.button("🗑️ حذف", key=f"del_{idx}"):
            st.session_state.invitees = st.session_state.invitees.drop(idx).reset_index(drop=True)
            st.rerun()
else:
    st.warning("القائمة فارغة حالياً.")

st.markdown('</div>', unsafe_allow_html=True)
