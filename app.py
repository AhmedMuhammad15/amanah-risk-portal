import streamlit as st
from data_processor import verify_shariah_compliance, calculate_financial_ratios
from model_handler import predict_customer_risk

# 1. INITIALIZE GLOBAL STATE VARIABLES
if 'font_scale' not in st.session_state:
    st.session_state.font_scale = 100
if 'ui_theme' not in st.session_state:
    st.session_state.ui_theme = "dark"
if 'lang' not in st.session_state:
    st.session_state.lang = "en"  # Default is English

st.set_page_config(page_title="Faysal NextGen", layout="wide", initial_sidebar_state="collapsed")

scale = st.session_state.font_scale
is_dark = st.session_state.ui_theme == "dark"
lang = st.session_state.lang

# Theme Palette Settings
bg_color = "#0b130f" if is_dark else "#f9fafb"
card_bg = "rgba(255, 255, 255, 0.04)" if is_dark else "#ffffff"
card_border = "rgba(255, 255, 255, 0.08)" if is_dark else "#e5e7eb"
text_primary = "#ffffff" if is_dark else "#111111"
text_secondary = "#9ca3af" if is_dark else "#4b5563"
nav_bg = "#111b15" if is_dark else "#ffffff"

# 2. DICTIONARY FOR SIMPLE WORDINGS (ENGLISH & URDU)
dictionary = {
    "en": {
        "dir": "ltr",
        "logo": "AMANAH NEXTGEN",
        "hero_title": "Your Islamic Finance Partner",
        "hero_sub": "Check your Islamic banking application instantly using smart technology and Shariah rules.",
        "about_title": "How it Works",
        "about_desc": "This system checks two things: First, it stops non-halal businesses automatically. Second, it calculates the default risk using machine learning based on your income and debts.",
        "panel_title": "Customer Details",
        "name": "Customer Name",
        "sector": "Business or Job Sector",
        "asset": "What asset are you buying?",
        "income": "Monthly Income (PKR)",
        "debts": "Existing Monthly Debts/Loans (PKR)",
        "amount": "Financing Amount Needed (PKR)",
        "tenure": "Months to Pay Back",
        "score": "Internal Credit Score (30-100)",
        "ledger_title": "Evaluation Result",
        "shariah_pass": "Shariah Status: PASSED (Valid Business Asset)",
        "shariah_fail": "Shariah Status: REJECTED (Non-Compliant Business)",
        "dti_lbl": "Debt-to-Income (DTI) Ratio",
        "risk_lbl": "Predicted Risk Score",
        "dti_desc": "You spend {}% of your income on monthly debts.",
        "risk_desc": "The system predicts a {}% chance of payment issues.",
        "status_low": "SAFE APPLICATION: The user profile looks secure and satisfies all basic rules.",
        "status_mid": "MODERATE RISK: Caution advised. Extra guarantees or collateral needed.",
        "status_high": "HIGH RISK: Application rejected due to low income or high existing loans."
    },
    "ur": {
        "dir": "rtl",
        "logo": "امانہ نیکسٹ جینیریشن",
        "hero_title": "آپ کا اسلامی مالیاتی پارٹنر",
        "hero_sub": "جدید ٹیکنالوجی اور شرعی اصولوں کے تحت اپنی بینکنگ درخواست کی فوری جانچ کریں۔",
        "about_title": "یہ نظام کیسے کام کرتا ہے؟",
        "about_desc": "یہ سسٹم دو چیزیں چیک کرتا ہے: اول، غیر شرعی کاروبار کو خودکار طور پر روکتا ہے۔ دوم، آپ کی آمدنی اور قرضوں کی بنیاد پر رسک سکور کا حساب لگاتا ہے۔",
        "panel_title": "گاہک کی معلومات",
        "name": "صارف کا پورا نام",
        "sector": "کاروبار یا ملازمت کا شعبہ",
        "asset": "خریدے جانے والے اثاثے کی قسم",
        "income": "ماہانہ آمدنی (روپے)",
        "debts": "پہلے سے موجود ماہانہ قرضے (روپے)",
        "amount": "بینک سے مطلوبہ رقم (روپے)",
        "tenure": "رقم واپسی کی مدت (مہینے)",
        "score": "کریڈٹ سکور انڈیکس (30 سے 100)",
        "ledger_title": "جانچ کا نتیجہ",
        "shariah_pass": "شرعی حیثیت: کامیاب (حلال اثاثہ اور کاروبار)",
        "shariah_fail": "شرعی حیثیت: نااہل (غیر شرعی شعبہ پایا گیا ہے)",
        "dti_lbl": "آمدنی اور قرض کا تناسب (DTI)",
        "risk_lbl": "ممکنہ رسک سکور",
        "dti_desc": "آپ اپنی ماہانہ آمدنی کا {}% حصہ پرانے قرضوں کی ادائیگی میں خرچ کر رہے ہیں۔",
        "risk_desc": "سسٹم کے مطابق ادائیگیوں میں تاخیر یا مسئلے کا امکان {}% ہے۔",
        "status_low": "محفوظ درخواست: صارف کا ریکارڈ بہترین ہے اور شرائط پر پورا اترتا ہے۔",
        "status_mid": "درمیانہ رسک: احتیاط لازمی ہے۔ اضافی ضمانت یا سیکیورٹی کی ضرورت ہو سکتی ہے۔",
        "status_high": "اعلیٰ رسک: کم آمدنی یا زیادہ قرضوں کی وجہ سے درخواست مسترد کی جاتی ہے۔"
    }
}

t = dictionary[lang]
text_direction = t["dir"]

# 3. GRAPHICS AND MASTER CSS
st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; direction: {text_direction}; }}
    header {{display: none !important;}}
    footer {{visibility: hidden;}}
    
    .theme-txt-primary {{ color: {text_primary} !important; text-align: {"right" if text_direction=="rtl" else "left"}; }}
    .theme-txt-secondary {{ color: {text_secondary} !important; text-align: {"right" if text_direction=="rtl" else "left"}; }}
    
    .navbar-container {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: {nav_bg};
        padding: 12px 5%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-bottom: 1px solid {card_border};
    }}
    .logo-block {{ font-size: calc(20px * {scale/100}); font-weight: 800; color: #006643; text-decoration: none; }}
    
    .hero-banner {{
        background: linear-gradient({"rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.85)" if is_dark else "rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.93)"}), 
                    url('https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?q=80&w=1600&auto=format&fit=crop');
        background-size: cover; background-position: center;
        height: 320px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 0 20px;
    }}
    .hero-heading {{ font-size: calc(40px * {scale/100}); font-weight: 800; color: {text_primary}; margin-bottom: 10px; }}
    .hero-sub {{ font-size: calc(15px * {scale/100}); color: {text_secondary}; max-width: 680px; }}
    
    .view-wrapper {{ padding: 40px 5%; }}
    .system-card {{ background: {card_bg}; border: 1px solid {card_border}; border-radius: 12px; padding: 25px !important; box-shadow: 0 4px 15px rgba(0,0,0,0.01); }}
    
    label p {{ color: {text_primary} !important; font-size: calc(13px * {scale/100}) !important; font-weight: 600 !important; text-align: {"right" if text_direction=="rtl" else "left"}; }}
    
    div.stButton > button {{
        background-color: rgba(0, 102, 67, 0.1) !important; color: #00ea8c !important;
        border: 1px solid rgba(0, 234, 140, 0.2) !important; border-radius: 20px !important;
        padding: 4px 14px !important; font-size: 13px !important; font-weight: 600 !important;
    }}
    div.stButton > button:hover {{ background-color: #006643 !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- NAVBAR ---
st.markdown(f"""
    <div class="navbar-container">
        <div class="logo-block">{t['logo']}</div>
        <div style="color:{text_primary}; font-weight:700; font-size:14px;">NextGen Risk Ledger Node</div>
    </div>
    """, unsafe_allow_html=True)

# --- INTERACTIVE TOOLBAR ---
t_space, t_col1, t_col2, t_col3, t_col4 = st.columns([3.5, 1, 1, 1, 1])
with t_col1:
    lang_btn = st.button("🌐 English/اردو", key="toggle_lang", use_container_width=True)
    if lang_btn:
        st.session_state.lang = "ur" if lang == "en" else "en"
        st.rerun()
with t_col2:
    if st.button("🌓 Mode", key="theme_toggle", use_container_width=True):
        st.session_state.ui_theme = "light" if is_dark else "dark"
        st.rerun()
with t_col3:
    if st.button("🔍 A+", key="inc_font", use_container_width=True) and scale < 150:
        st.session_state.font_scale += 25
        st.rerun()
with t_col4:
    if st.button("🔍 A-", key="dec_font", use_container_width=True) and scale > 100:
        st.session_state.font_scale -= 25
        st.rerun()

# --- HERO HERO BANNER ---
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-heading">{t['hero_title']}</div>
        <div class="hero-sub">{t['hero_sub']}</div>
    </div>
    """, unsafe_allow_html=True)

# --- HOW IT WORKS SECTION ---
st.markdown("""<div class="view-wrapper" style="padding-bottom: 0px;">""", unsafe_allow_html=True)
st.markdown(f"""
    <div class="system-card">
        <h4 class="theme-txt-primary" style="margin-top:0; font-weight:700; font-size:calc(17px * {scale/100});">{t['about_title']}</h4>
        <p class="theme-txt-secondary" style="font-size:calc(14px * {scale/100}); margin-bottom:0; line-height:1.5;">{t['about_desc']}</p>
    </div>
    </div>
""", unsafe_allow_html=True)

# --- CORE CONSOLE ---
st.markdown("""<div class="view-wrapper">""", unsafe_allow_html=True)

col1, col2 = st.columns([1.05, 1])

with col1:
    st.markdown("<div class='system-card'>", unsafe_allow_html=True)
    st.markdown(f"<h4 class='theme-txt-primary' style='margin-top:0; font-weight:700; font-size:calc(17px * {scale/100}); margin-bottom:20px;'>{t['panel_title']}</h4>", unsafe_allow_html=True)
    
    customer_name = st.text_input(t['name'], value="Ahmed Muhammad")
    biz_sector = st.selectbox(t['sector'], ['Technology', 'Healthcare', 'Agriculture', 'Alcohol', 'Conventional Finance', 'Retail'])
    asset_type = st.selectbox(t['asset'], ['Commercial Real Estate', 'Vehicles', 'Industrial Machinery', 'Raw Materials'])
    
    income = st.number_input(t['income'], min_value=10000, value=250000, step=10000)
    debts = st.number_input(t['debts'], min_value=0, value=30000, step=5000)
    requested_amount = st.number_input(t['amount'], min_value=10000, value=1200000, step=50000)
    tenure = st.slider(t['tenure'], min_value=6, max_value=60, value=24)
    c_score = st.slider(t['score'], min_value=30, max_value=100, value=98)
    st.markdown("</div>", unsafe_allow_html=True)

# --- COL2 KA INNER CODE UPDATE ---
with col2:
    st.markdown(f"<div class='system-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown(f"<h4 class='theme-txt-primary' style='margin-top:0; font-weight:700; font-size:calc(18px * {scale/100}); margin-bottom:20px;'>{t['ledger_title']}</h4>", unsafe_allow_html=True)
    
    is_compliant, message = verify_shariah_compliance(biz_sector, asset_type)
    
    if not is_compliant:
        st.error(t['shariah_fail'])
    else:
        st.success(t['shariah_pass'])
        
        dti = calculate_financial_ratios(income, debts, requested_amount, tenure)
        input_data = {
            'monthly_income': income, 'existing_debts': debts, 'requested_amount': requested_amount,
            'tenure_months': tenure, 'dti': dti, 'credit_score': c_score
        }
        
        with st.spinner('Calculating...'):
            risk_percentage = predict_customer_risk(input_data)
        
        st.write("")
        
        # --- NEW BOLD KPI NUMBER CARDS ---
        kpi_col1, kpi_col2 = st.columns(2)
        with kpi_col1:
            st.markdown(f"""
                <div style="background: rgba(0, 102, 67, 0.15); border: 2px solid #00ea8c; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 15px;">
                    <div style="font-size: calc(38px * {scale/100}); font-weight: 800; color: #00ea8c; margin-bottom: 2px;">{int(dti * 100)}%</div>
                    <div style="font-size: calc(13px * {scale/100}); color: {text_primary}; font-weight: 700; text-transform: uppercase;">{t['dti_lbl']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with kpi_col2:
            st.markdown(f"""
                <div style="background: rgba(0, 102, 67, 0.15); border: 2px solid #00ea8c; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 15px;">
                    <div style="font-size: calc(38px * {scale/100}); font-weight: 800; color: #00ea8c; margin-bottom: 2px;">{risk_percentage}%</div>
                    <div style="font-size: calc(13px * {scale/100}); color: {text_primary}; font-weight: 700; text-transform: uppercase;">{t['risk_lbl']}</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Explanatory lines below numbers
        st.markdown(f"<p class='theme-txt-secondary' style='font-size: calc(14px * {scale/100}); margin-top: 10px;'>💡 {t['dti_desc'].format(int(dti * 100))}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='theme-txt-secondary' style='font-size: calc(14px * {scale/100});'>🤖 {t['risk_desc'].format(risk_percentage)}</p>", unsafe_allow_html=True)
        
        st.write("---")
        
        if risk_percentage > 60:
            st.error(t['status_high'])
        elif 35 <= risk_percentage <= 60:
            st.warning(t['status_mid'])
        else:
            st.success(t['status_low'])
            
    st.markdown("</div>", unsafe_allow_html=True)