import streamlit as st
import json
import os
import sys
import time

# Add src to path so imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.agent import SchemeSetuAgent as Agent

# Streamlit config must be the first command
st.set_page_config(
    page_title="SchemeSetu AI",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def apply_custom_styles():
    """
    Injects custom CSS for the glassmorphism UI.
    Keeps the main logic clean.
    """
    st.markdown("""
    <style>
    /* Main gradient background */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e293b, #0f172a 40%, #020617 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Header Text */
    h1 {
        background: linear-gradient(90deg, #22d3ee, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        padding-bottom: 10px;
    }
    
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1.1rem;
        margin-top: -15px;
        margin-bottom: 30px;
    }

    /* Form Input Styling */
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Action Buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        height: 55px;
        font-size: 18px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.6);
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%);
    }

    /* Scheme Cards (Glassmorphism) */
    .scheme-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 20px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .scheme-card:hover {
        transform: scale(1.01);
        border-color: #3b82f6;
    }
    
    .scheme-card h3 {
        color: #60a5fa;
        font-size: 1.4rem;
        margin: 0 0 10px 0;
        font-weight: 700;
    }
    
    .scheme-card p {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .tag {
        display: inline-block;
        background: rgba(37, 99, 235, 0.2);
        color: #60a5fa;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 10px;
    }
    
    .link-btn {
        float: right;
        color: #fff;
        text-decoration: none;
        background: #334155;
        padding: 6px 15px;
        border-radius: 8px;
        font-size: 0.85rem;
        transition: background 0.2s;
    }
    
    .link-btn:hover {
        background: #475569;
    }

    /* Clean up Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Localization dictionary
UI_TEXT = {
    "English": {
        "header": "SchemeSetu",
        "subheader": "AI-Powered Citizen Benefit Navigator",
        "tabs": ["🔍 Search Schemes", "⚡ Teacher Mode"],
        "labels": ["Age", "Annual Income (₹)", "Category"],
        "btn_search": "Find Matching Schemes",
        "status_thinking": "🤖 Agent is analyzing government database...",
        "results_found": "Eligible Schemes Found",
        "no_results": "No matching schemes found.",
        "logs": "Show Technical Logs (Protocol Data)",
        "admin_title": "Teach New Scheme",
        "btn_save": "Save to Neural Database"
    },
    "Hindi": {
        "header": "स्कीम-सेतु",
        "subheader": "एआई-आधारित सरकारी योजना नेविगेटर",
        "tabs": ["🔍 योजना खोजें", "⚡ व्यवस्थापक (Admin)"],
        "labels": ["उम्र (आयु)", "वार्षिक आय (₹)", "श्रेणी / जाति"],
        "btn_search": "योजनाएं खोजें",
        "status_thinking": "🤖 एआई एजेंट डेटाबेस का विश्लेषण कर रहा है...",
        "results_found": "पात्र योजनाएं मिलीं",
        "no_results": "कोई योजना नहीं मिली।",
        "logs": "तकनीकी लॉग देखें",
        "admin_title": "नई योजना जोड़ें",
        "btn_save": "डेटाबेस में सहेजें"
    }
}

@st.cache_resource
def get_agent():
    return Agent()

def main():
    # Apply styles first
    apply_custom_styles()

    # Load logic engine
    try:
        agent = get_agent()
    except Exception as e:
        st.error(f"Failed to initialize AI Agent: {e}")
        st.stop()

    # Top Bar: Language Selector & Header
    col_head, col_lang = st.columns([5, 1])
    with col_lang:
        lang = st.selectbox("Language", ["English", "Hindi"], label_visibility="collapsed")
    
    txt = UI_TEXT[lang]

    with col_head:
        st.markdown(f"<h1>{txt['header']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='subtitle'>{txt['subheader']}</div>", unsafe_allow_html=True)

    # Main Interface Tabs
    tab_search, tab_admin = st.tabs(txt['tabs'])

    # --- TAB 1: SEARCH ---
    with tab_search:
        st.write("") # Spacing
        c1, c2, c3 = st.columns(3)
        
        with c1:
            age = st.number_input(txt['labels'][0], 0, 100, 22)
        with c2:
            income = st.number_input(txt['labels'][1], 0, 1000000, 120000, step=5000)
        with c3:
            caste = st.selectbox(txt['labels'][2], ["General", "OBC", "SC", "ST"])

        st.write("")
        st.write("")

        if st.button(txt['btn_search']):
            # Construct Agent Request
            payload = {
                "request_type": "check_eligibility",
                "age": age,
                "income": income,
                "caste": caste
            }
            
            # Simulate processing time for UX
            with st.status(txt['status_thinking'], expanded=True) as status:
                time.sleep(0.6)
                response_str = agent.listen(json.dumps(payload))
                status.update(label="Analysis Complete", state="complete", expanded=False)

            # Process Results
            resp = json.loads(response_str)
            
            # Save logs for dev view
            st.session_state['log_req'] = json.dumps(payload, indent=2)
            st.session_state['log_res'] = response_str

            st.write("")
            if resp.get("status") == "success":
                schemes = resp.get("data", [])
                
                if schemes:
                    for s in schemes:
                        st.markdown(f"""
                        <div class="scheme-card">
                            <a href="{s.get('link', '#')}" target="_blank" class="link-btn">Apply ↗</a>
                            <h3>{s['name']}</h3>
                            <p>{s['description']}</p>
                            <div class="tag">💰 {s['benefit']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning(txt['no_results'])

        # Dev Logs Section
        st.divider()
        with st.expander(txt['logs']):
            l1, l2 = st.columns(2)
            if 'log_req' in st.session_state:
                l1.caption("➡️ Outgoing Request")
                l1.code(st.session_state['log_req'], language="json")
                
                l2.caption("⬅️ Incoming Response")
                l2.code(st.session_state['log_res'], language="json")
            else:
                st.caption("No request history available.")

    # --- TAB 2: ADMIN ---
    with tab_admin:
        st.markdown(f"### {txt['admin_title']}")
        
        with st.form("new_scheme_form"):
            name = st.text_input("Scheme Name")
            desc = st.text_area("Description")
            benefit = st.text_input("Benefit")
            
            rc1, rc2 = st.columns(2)
            min_a = rc1.number_input("Min Age", 0, 100, 18)
            max_a = rc2.number_input("Max Age", 0, 100, 30)
            max_inc = st.number_input("Max Income Limit", 0, 1000000, 200000)
            
            if st.form_submit_button(txt['btn_save']):
                new_data = {
                    "name": name,
                    "description": desc,
                    "benefit": benefit,
                    "rules": {
                        "min_age": min_a,
                        "max_age": max_a,
                        "max_income": max_inc,
                        "category": ["General", "OBC", "SC", "ST"]
                    }
                }
                
                req = {
                    "request_type": "learn_new_scheme",
                    "scheme_data": new_data
                }
                
                with st.spinner("Writing to neural database..."):
                    time.sleep(0.5)
                    res = agent.listen(json.dumps(req))
                
                st.success("Success!")
                st.json(json.loads(res))

if __name__ == "__main__":
    main()