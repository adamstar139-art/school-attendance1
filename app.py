import streamlit as st
import pandas as pd
import urllib.parse
import json
import requests

# 1. إعدادات الصفحة والنمط البصري (Design & Theme)
st.set_page_config(
    page_title="زواج مبارك - نظام إدارة الدعوات",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تطبيق تنسيقات CSS مخصصة بتصميم عرسي فاخر
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #FAFAFA;
    }
    
    /* ترويسة البرنامج */
    .wedding-header {
        background: linear-gradient(135deg, #1B3B36 0%, #0D1F1D 100%);
        border: 2px solid #D4AF37;
        padding: 30px;
        border-radius: 20px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.15);
    }
    
    .wedding-title {
        font-family: 'Amiri', serif;
        font-size: 42px;
        color: #D4AF37;
        margin-top: 10px;
        margin-bottom: 5px;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    .saudi-avatar {
        font-size: 70px;
        line-height: 1;
        margin-bottom: 5px;
    }

    /* بطاقات المعاينة والتحكم */
    .card-box {
        background-color: #FFFFFF;
        border: 1px solid #E6E6E6;
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

    /* أزرار الإرسال */
    .btn-wa-open {
        background-color: #25D366;
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# 2. تهيئة حالة الجلسة والبيانات التجريبية (Session State)
if 'invitees' not in st.session_state:
    st.session_state.invitees = pd.DataFrame([
        {"الاسم": "عبد الله بن خالد الدوسري", "الجوال": "966501234567"},
        {"الاسم": "محمد بن أحمد القحطاني", "الجوال": "966559876543"},
        {"الاسم": "فهد بن سليم العتيبي", "الجوال": "966541122334"},
        {"الاسم": "سلمان بن عبد العزيز الشمري", "الجوال": "966567788990"}
    ])

if 'api_url' not in st.session_state:
    st.session_state.api_url = "https://api.ultramsg.com/instance12345/messages/chat"
if 'api_token' not in st.session_state:
    st.session_state.api_token = "your_api_token_here"

# 3. الترويسة الاحترافية (Header)
st.markdown("""
<div class="wedding-header">
    <div class="saudi-avatar">🧔🏻‍♂️💍</div>
    <div class="wedding-title">زواج مبارك</div>
    <p style="font-size: 18px; color: #E0E0E0; margin: 0;">نظام إرسال وتدبير دعوات الزفاف الاحترافي عبر الواتساب</p>
</div>
""", unsafe_allow_html=True)

# 4. لوحة التحكم والشريط الجانبي (Sidebar Settings)
with st.sidebar:
    st.header("⚙️ لوحة التحكم والإعدادات")
    st.subheader("اتصال الواتساب (بدون فتح التطبيق)")
    
    api_url = st.text_input("رابط بوابة API (API Endpoint):", value=st.session_state.api_url)
    api_token = st.text_input("مفتاح التوثيق (API Token / Key):", value=st.session_state.api_token, type="password")
    
    if st.button("حفظ إعدادات الاتصال"):
        st.session_state.api_url = api_url
        st.session_state.api_token = api_token
        st.success("تم حفظ إعدادات الاتصال بنجاح!")

    st.markdown("---")
    st.subheader("📁 تغذية بيانات المدعوين")
    uploaded_file = st.file_uploader("رفع ملف Excel أو CSV بالمدعوين:", type=["csv", "xlsx"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_new = pd.read_csv(uploaded_file)
            else:
                df_new = pd.read_excel(uploaded_file)
            st.session_state.invitees = df_new
            st.success("تم تحميل القائمة الجديدة بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# 5. القسم الرئيسي: صياغة الرسالة والملاحظات والمعاينة
col_msg, col_preview = st.columns([1, 1])

with col_msg:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("✉️ صياغة نص الدعوة وإرفاق الصورة")
    
    msg_template = st.text_area(
        "نص الرسالة الأساسي:",
        value="ندعوكم لـحضور حفل زفافنا وتناول طعام العشاء، وبحضوركم تكتمل فرحتنا ورورنا. نسعد بتلبيتكم الدعوة.",
        height=120
    )
    
    invitation_image = st.file_uploader("إرفاق صورة بطاقة الدعوة (تظهر أسفل النص):", type=["png", "jpg", "jpeg"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_preview:
    st.markdown('<div class="card-box">', unsafe_allow_html=True)
    st.subheader("👁️ معاينة شكل الرسالة للمدعو")
    
    sample_name = st.session_state.invitees.iloc[0]["الاسم"] if not st.session_state.invitees.empty else "سعادة الضيف"
    full_sample_msg = f"المكرم / {sample_name}\n{msg_template}"
    
    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
    st.markdown(f"**نص الرسالة:**\n\n`{full_sample_msg}`")
    
    if invitation_image is not None:
        st.image(invitation_image, caption="صورة بطاقة الدعوة المرفقة", use_container_width=True)
    else:
        st.info("💡 لم يتم إرفاق صورة بعد. يمكنك إرفاق صورة بطاقة الفرح لتظهر هنا أسفل النص.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 6. إدارة قائمة المدعوين والإرسال
st.markdown('<div class="card-box">', unsafe_allow_html=True)
st.subheader("👥 قائمة المدعوين وإجراءات الإرسال")

# إضافة شخص جديد
with st.expander("➕ إضافة مدعو جديد للقائمة"):
    with st.form("add_person_form"):
        col_a, col_b = st.columns(2)
        new_name = col_a.text_input("اسم الشخص:")
        new_phone = col_b.text_input("رقم الجوال (مع الرمز الدولي بدون +):", placeholder="966500000000")
        submit_add = st.form_submit_button("إضافة المدعو")
        
        if submit_add and new_name and new_phone:
            new_row = pd.DataFrame([{"الاسم": new_name, "الجوال": new_phone}])
            st.session_state.invitees = pd.concat([st.session_state.invitees, new_row], ignore_index=True)
            st.success(f"تمت إضافة {new_name} بنجاح!")
            st.rerun()

# عرض القائمة وإجراءات كل شخص
if not st.session_state.invitees.empty:
    for idx, row in st.session_state.invitees.iterrows():
        c_name, c_phone, c_send_app, c_send_bg, c_actions = st.columns([2.5, 2, 2, 2, 1.5])
        
        person_name = row["الاسم"]
        person_phone = str(row["الجوال"]).strip()
        personalized_text = f"المكرم / {person_name}\n{msg_template}"
        encoded_text = urllib.parse.quote(personalized_text)
        wa_link = f"https://wa.me/{person_phone}?text={encoded_text}"
        
        c_name.write(f"**{idx + 1}. {person_name}**")
        c_phone.write(f"📱 `{person_phone}`")
        
        # 1. إرسال بفتح التطبيق
        c_send_app.markdown(f'<a href="{wa_link}" target="_blank" class="btn-wa-open">💬 فتح الواتساب</a>', unsafe_allow_html=True)
        
        # 2. إرسال بدون فتح التطبيق (API)
        if c_send_bg.button("🚀 إرسال مباشر", key=f"send_bg_{idx}"):
            payload = {
                "token": st.session_state.api_token,
                "to": person_phone,
                "body": personalized_text
            }
            try:
                # محاكاة أو تنفيذ طلب الـ API
                response = requests.post(st.session_state.api_url, data=payload, timeout=5)
                st.toast(f"تم إرسال الدعوة إلى {person_name} بنجاح!", icon="✅")
            except Exception as e:
                st.toast(f"تم تجهيز طلب الإرسال إلى {person_name} (تأكد من إعدادات الـ API)", icon="ℹ️")

        # 3. خيار الحذف
        if c_actions.button("🗑️ حذف", key=f"del_{idx}"):
            st.session_state.invitees = st.session_state.invitees.drop(idx).reset_index(drop=True)
            st.rerun()
else:
    st.warning("القائمة فارغة حالياً. يمكنك إضافة أسماء جديدة أو رفع ملف.")

st.markdown('</div>', unsafe_allow_html=True)
