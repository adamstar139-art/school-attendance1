import streamlit as st
import pandas as pd
import urllib.parse
import requests
import os

# 1. إعدادات الصفحة والتصميم المتجاوب مع الجوال
st.set_page_config(
    page_title="زواج مبارك - نظام إدارة الدعوات",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DB_FILE = "saved_invitees.csv"

# وظائف حفظ وقراءة البيانات بشكل دائم
def load_data():
    if os.path.exists(DB_FILE):
        try:
            return pd.read_csv(DB_FILE, dtype=str)
        except Exception:
            pass
    # بيانات افتراضية للتجربة في حال عدم وجود ملف محفوظ
    return pd.DataFrame([
        {"الاسم": "عبد الله بن خالد الدوسري", "الجوال": "966501234567"},
        {"الاسم": "محمد بن أحمد القحطاني", "الجوال": "966559876543"},
        {"الاسم": "فهد بن سليم العتيبي", "الجوال": "966541122334"},
        {"الاسم": "سلمان بن عبد العزيز الشمري", "الجوال": "966567788990"}
    ])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

# تحميل البيانات عند التشغيل
if 'invitees' not in st.session_state:
    st.session_state.invitees = load_data()

if 'ultramsg_instance' not in st.session_state:
    st.session_state.ultramsg_instance = "instance10000"
if 'ultramsg_token' not in st.session_state:
    st.session_state.ultramsg_token = "your_token_here"

# CSS مخصص للمحاذاة والتجاوب التام مع الشاشات والجوالات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
        background-color: #FAFAFA;
    }
    
    /* الترويسة */
    .wedding-header {
        background: linear-gradient(135deg, #1B3B36 0%, #0D1F1D 100%);
        border: 2px solid #D4AF37;
        padding: 20px;
        border-radius: 16px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(212, 175, 55, 0.15);
    }
    
    .wedding-title {
        font-family: 'Amiri', serif !important;
        font-size: 36px;
        color: #D4AF37;
        margin: 5px 0;
        font-weight: bold;
    }

    .saudi-avatar {
        font-size: 55px;
        line-height: 1;
    }

    /* بطاقات العرض */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        border-right: 5px solid #D4AF37;
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 18px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.02);
    }

    /* محاذاة وتنسيق صفوف المدعوين */
    .guest-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F0F0F0;
    }

    .guest-name {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #1B3B36 !important;
        text-align: right !important;
        margin: 0;
        line-height: 1.5;
    }

    .guest-phone {
        font-family: 'Tajawal', sans-serif !important;
        font-size: 14px !important;
        color: #555555 !important;
        direction: ltr !important;
        text-align: right !important;
        margin: 0;
    }

    /* زر الواتساب */
    .btn-wa-open {
        background-color: #25D366;
        color: white !important;
        padding: 6px 12px;
        border-radius: 6px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 13px;
        display: block;
        text-align: center;
        width: 100%;
        box-sizing: border-box;
    }

    /* تحسين التجاوب مع الجوال (Mobile Optimization) */
    @media (max-width: 768px) {
        .wedding-title { font-size: 28px; }
        .saudi-avatar { font-size: 45px; }
        .card-box { padding: 12px; }
        .guest-name { font-size: 15px !important; }
        .guest-phone { font-size: 13px !important; }
        .stButton button { width: 100% !important; margin-bottom: 5px; }
    }
</style>
""", unsafe_allow_html=True)

# 2. الترويسة
st.markdown("""
<div class="wedding-header">
    <div class="saudi-avatar">🧔🏻‍♂️💍</div>
    <div class="wedding-title">زواج مبارك</div>
    <p style="font-size: 15px; color: #E0E0E0; margin: 0;">نظام إرسال وتدبير دعوات الزفاف عبر UltraMsg</p>
</div>
""", unsafe_allow_html=True)

# 3. لوحة التحكم والشريط الجانبي
with st.sidebar:
    st.header("⚙️ إعدادات UltraMsg")
    instance_id = st.text_input("معرف الحساب (Instance ID):", value=st.session_state.ultramsg_instance)
    token_id = st.text_input("رمز التوثيق (Token):", value=st.session_state.ultramsg_token, type="password")
    
    if st.button("حفظ إعدادات الربط"):
        st.session_state.ultramsg_instance = instance_id.strip()
        st.session_state.ultramsg_token = token_id.strip()
        st.success("تم حفظ الإعدادات!")

    st.markdown("---")
    st.subheader("📁 تغذية بيانات المدعوين (Excel / CSV)")
    uploaded_file = st.file_uploader("رفع ملف جديد (سيتم حفظه دائماً):", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_new = pd.read_csv(uploaded_file, dtype=str)
            else:
                df_new = pd.read_excel(uploaded_file, dtype=str)
            
            # حفظ الملف دائمياً
            st.session_state.invitees = df_new
            save_data(df_new)
            st.success("تم رفع وحفظ قائمة المدعوين بنجاح دائم!")
            st.rerun()
        except Exception as e:
            st.error(f"خطأ في قراءة الملف: {e}")

# 4. صياغة الرسالة والمعاينة
col_msg, col_preview = st.columns([1, 1])

with col_msg:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("✉️ نص الدعوة والصورة")
    msg_template = st.text_area(
        "نص الرسالة الأساسي:",
        value="ندعوكم لـحضور حفل زفافنا وتناول طعام العشاء، وبحضوركم تكتمل فرحتنا وسرورنا. نسعد بتلبيتكم الدعوة.",
        height=120
    )
    invitation_image = st.file_uploader("إرفاق صورة بطاقة الدعوة:", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("👁️ معاينة الدعوة")
    sample_name = st.session_state.invitees.iloc[0]["الاسم"] if not st.session_state.invitees.empty else "سعادة الضيف"
    full_sample_msg = f"المكرم / {sample_name}\n{msg_template}"
    
    st.info(f"**النموذج:**\n\n{full_sample_msg}")
    if invitation_image is not None:
        st.image(invitation_image, caption="الصورة المرفقة اسفل النص", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 5. قائمة المدعوين وإدارتها
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.subheader("👥 قائمة المدعوين المحفوظة")

# إضافة شخص جديد مع الحفظ التلقائي
with st.expander("➕ إضافة مدعو جديد"):
    with st.form("add_person_form"):
        col_a, col_b = st.columns(2)
        new_name = col_a.text_input("الاسم:")
        new_phone = col_b.text_input("الجوال (مثال: 966500000000):")
        submit_add = st.form_submit_button("حفظ وإضافة")
        
        if submit_add and new_name and new_phone:
            new_row = pd.DataFrame([{"الاسم": new_name.strip(), "الجوال": new_phone.strip()}])
            st.session_state.invitees = pd.concat([st.session_state.invitees, new_row], ignore_index=True)
            save_data(st.session_state.invitees) # حفظ دائم
            st.success(f"تمت إضافة وحفظ {new_name} بنجاح!")
            st.rerun()

# عرض القائمة بمحاذاة ممتازة وتناسق على الجوال
if not st.session_state.invitees.empty:
    for idx, row in st.session_state.invitees.iterrows():
        c_name, c_phone, c_send_app, c_send_bg, c_actions = st.columns([2.5, 2, 1.8, 1.8, 1])
        
        person_name = str(row["الاسم"])
        person_phone = str(row["الجوال"]).strip()
        personalized_text = f"المكرم / {person_name}\n{msg_template}"
        encoded_text = urllib.parse.quote(personalized_text)
        wa_link = f"https://wa.me/{person_phone}?text={encoded_text}"
        
        # محاذاة الأسماء والأرقام بشكل منسق
        c_name.markdown(f'<div class="guest-name">{idx + 1}. {person_name}</div>', unsafe_allow_html=True)
        c_phone.markdown(f'<div class="guest-phone">📱 {person_phone}</div>', unsafe_allow_html=True)
        
        # أزرار الإرسال
        c_send_app.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa-open">💬 تطبيق الواتساب</a>', unsafe_allow_html=True)
        
        if c_send_bg.button("🚀 إرسال تلقائي", key=f"send_um_{idx}"):
            inst = st.session_state.ultramsg_instance
            tok = st.session_state.ultramsg_token
            
            if inst == "instance10000" or tok == "your_token_here":
                st.warning("يرجى إدخال بيانات UltraMsg في الشريط الجانبي أولاً.")
            else:
                api_url = f"https://api.ultramsg.com/{inst}/messages/chat"
                payload = f"token={tok}&to={person_phone}&body={urllib.parse.quote(personalized_text)}"
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                try:
                    res = requests.post(api_url, data=payload.encode('utf-8'), headers=headers, timeout=10)
                    st.toast(f"تم الإرسال التلقائي إلى {person_name}!", icon="✅")
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")

        # حذف شخص مع التحديث الدائم
        if c_actions.button("🗑️", key=f"del_{idx}"):
            st.session_state.invitees = st.session_state.invitees.drop(idx).reset_index(drop=True)
            save_data(st.session_state.invitees) # حفظ التغييرات دائمياً
            st.rerun()
else:
    st.warning("القائمة فارغة حالياً.")

st.markdown('</div>', unsafe_allow_html=True)
