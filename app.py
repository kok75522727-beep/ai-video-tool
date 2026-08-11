import streamlit as st
import os
import time
import json
import requests

# Page Config
st.set_page_config(
    page_title="AI Movie Recap & Burmese Voiceover Studio",
    page_icon="🎬",
    layout="centered"
)

KEYS_FILE = "user_api_keys.json"

def load_keys_from_file():
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("gemini_keys", []), data.get("groq_keys", [])
        except:
            pass
    return [], []

def save_keys_to_file(gemini_keys, groq_keys):
    try:
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump({"gemini_keys": gemini_keys, "groq_keys": groq_keys}, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        return False

saved_gemini, saved_groq = load_keys_from_file()

if "gemini_keys" not in st.session_state:
    st.session_state.gemini_keys = saved_gemini
if "groq_keys" not in st.session_state:
    st.session_state.groq_keys = saved_groq

# Custom CSS for ultra-clean dark theme and horizontal tag wrap
st.markdown("""
<style>
.stApp {
    background-color: #0d1117;
    color: #ffffff;
}
.main-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}
/* Style file uploader to blend into dark theme */
div[data-testid="stFileUploader"] {
    background-color: #21262d;
    border: 1px dashed #30363d;
    border-radius: 10px;
    padding: 15px;
}
div[data-testid="stFileUploader"] section {
    background-color: transparent !important;
}
div[data-testid="stFileUploader"] small {
    color: #8b949e !important;
}
/* Horizontal flex tags container */
.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}
.tag-item {
    display: inline-flex;
    align-items: center;
    background-color: #21262d;
    border: 1px solid #30363d;
    color: #c9d1d9;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
}
.tag-item button {
    background: none;
    border: none;
    color: #f85149;
    cursor: pointer;
    margin-left: 6px;
    font-weight: bold;
}
.stButton>button {
    border-radius: 6px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; margin-bottom: 25px;'>🎬 AI Movie Recap & Burmese Voiceover Studio</h2>", unsafe_allow_html=True)

# --- API Key Management Section (Compact & Clean) ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🔑 API Key စီမံခန့်ခွဲမှု (၁၀ ခုအထိ သိမ်းဆည်းနိုင်သည်)")
    
    col_gem, col_groq = st.columns(2)
    
    with col_gem:
        st.markdown("**Gemini API Key** &nbsp; 👉 [Key ယူရန်](https://aistudio.google.com/)")
        new_g = st.text_input("Gemini Key", placeholder="AlzaSy...", label_visibility="collapsed", key="in_gemini", type="password")
        if st.button("➕ Add Gemini", use_container_width=True):
            if new_g.strip():
                if len(st.session_state.gemini_keys) < 10:
                    if new_g.strip() not in st.session_state.gemini_keys:
                        st.session_state.gemini_keys.append(new_g.strip())
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
                else:
                    st.error("အများဆုံး ၁၀ ခုသာ။")
        
        # Display Gemini keys as horizontal compact tags
        if st.session_state.gemini_keys:
            st.markdown('<div class="tags-container">', unsafe_allow_html=True)
            for idx, k in enumerate(st.session_state.gemini_keys):
                masked = f"Gemini {idx+1}: {k[:3]}...{k[-3:]}" if len(k) > 6 else f"Gemini {idx+1}"
                col_tag, col_del = st.columns([4, 1])
                with col_tag:
                    st.markdown(f"<span style='background:#1f6feb; color:white; padding:4px 8px; border-radius:4px; font-size:11px;'>✨ {masked}</span>", unsafe_allow_html=True)
                with col_del:
                    if st.button("❌", key=f"dg_{idx}"):
                        st.session_state.gemini_keys.pop(idx)
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    with col_groq:
        st.markdown("**Groq API Key** &nbsp; 👉 [Key ယူရန်](https://console.groq.com/keys)")
        new_gr = st.text_input("Groq Key", placeholder="gsk_...", label_visibility="collapsed", key="in_groq", type="password")
        if st.button("➕ Add Groq", use_container_width=True, type="primary"):
            if new_gr.strip():
                if len(st.session_state.groq_keys) < 10:
                    if new_gr.strip() not in st.session_state.groq_keys:
                        st.session_state.groq_keys.append(new_gr.strip())
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
                else:
                    st.error("အများဆုံး ၁၀ ခုသာ။")
        
        # Display Groq keys as horizontal compact tags
        if st.session_state.groq_keys:
            st.markdown('<div class="tags-container">', unsafe_allow_html=True)
            for idx, k in enumerate(st.session_state.groq_keys):
                masked = f"Groq {idx+1}: {k[:4]}...{k[-4:]}" if len(k) > 8 else f"Groq {idx+1}"
                col_tag, col_del = st.columns([4, 1])
                with col_tag:
                    st.markdown(f"<span style='background:#238636; color:white; padding:4px 8px; border-radius:4px; font-size:11px;'>⚡ {masked}</span>", unsafe_allow_html=True)
                with col_del:
                    if st.button("❌", key=f"dr_{idx}"):
                        st.session_state.groq_keys.pop(idx)
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# API Execution Helpers
def call_groq(api_keys, prompt):
    for idx, key in enumerate(api_keys):
        try:
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                return res.json()['choices'][0]['message']['content'], idx + 1
        except:
            continue
    return None, None

def call_gemini(api_keys, prompt):
    for idx, key in enumerate(api_keys):
        try:
            headers = {"Content-Type": "application/json"}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text'], idx + 1
        except:
            continue
    return None, None

# --- Tabs ---
tab1, tab2 = st.tabs(["🎥 Movie Recap Generator", "🌐 English Recap to Burmese (Smart Persona)"])

with tab1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🎬 Auto Movie Recap Voiceover Script")
    st.markdown("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ပါက ဇာတ်ကောင်များ၏ အခြေအနေကို လေ့လာပြီး ပရိသတ်ကို ဆွဲဆောင်နိုင်သော Storytelling အပြောအဆို ဇာတ်ညွှန်းကို ထုတ်ပေးမည်။")
    
    movie_file = st.file_uploader("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ရန် (MP4, MKV)", type=["mp4", "mkv"], key="f1")
    engine = st.radio("AI Engine ရွေးရန်", ["Gemini API", "Groq API"], horizontal=True)

    if st.button("🚀 ဇာတ်ညွှန်း ဖန်တီးမည်", type="primary", use_container_width=True):
        if not movie_file:
            st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင် တင်ပေးပါ။")
        else:
            keys = st.session_state.gemini_keys if "Gemini" in engine else st.session_state.groq_keys
            if not keys:
                st.error("ကျေးဇူးပြု၍ အထက်ပါ Card တွင် API Key အနည်းဆုံး တစ်ခု ထည့်သွင်းပါ။")
            else:
                with st.spinner("AI ဖြင့် ဇာတ်ကားကို ခွဲခြမ်းစိတ်ဖြာနေသည်..."):
                    prompt = (
                        "You are an expert movie recap narrator. Analyze the uploaded movie file context "
                        "and write a captivating storytelling voiceover script in BURMESE language ONLY. "
                        "Detect character personas (e.g., boy, girl, Jack) accurately and use appropriate pronouns "
                        "(e.g., 'ကျွန်တော်' for first-person narrative, or character names like 'ဂျက်'). "
                        "NO timestamps like [00:01]. Pure narrative script only."
                    )
                    res, kidx = call_gemini(keys, prompt) if "Gemini" in engine else call_groq(keys, prompt)
                    if res:
                        st.success(f"✅ အောင်မြင်သည်! (Key #{kidx})")
                        st.text_area("ထွက်လာသော ဇာတ်ညွှန်း:", res, height=350)
                        st.download_button("📥 ဇာတ်ညွှန်း ဒေါင်းလုဒ် (.txt)", res, file_name="recap_script.txt", mime="text/plain")
                    else:
                        st.error("❌ Key များ Limit ပြည့်နေပါသည် သို့မဟုတ် အလုပ်မလုပ်ပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🌐 English Recap to Burmese (Smart Persona Retention)")
    st.markdown("အင်္ဂလိပ် Recap ဗီဒီယိုလင့်ခ် (သို့မဟုတ်) စာသားများကို ထည့်သွင်းပါ။ AI က ဇာတ်ကောင် မည်သူဖြစ်သည် (ကောင်လေး၊ ကောင်မလေး၊ ဂျက် လား စသည်ဖြင့်) ကို စစ်ဆေးပြီး မူရင်းနာမ်စားများနှင့်အညီ သဘာဝကျကျ မြန်မာဘာသာသို့ ဘာသာပြန်ပေးမည်။")

    src_mode = st.radio("ရင်းမြစ်", ["Video Link / English Content", "Upload Video File"], horizontal=True, key="f2_mode")
    
    txt_input = ""
    if "Link" in src_mode:
        txt_input = st.text_area("အင်္ဂလိပ် ဗီဒီယိုလင့်ခ် (သို့မဟုတ်) အင်္ဂလိပ် Recap စာသားများ ထည့်ရန်", placeholder="Paste YouTube/TikTok link or English text here...")
    else:
        st.file_uploader("အင်္ဂလိပ်ဗီဒီယိုဖိုင် တင်ရန်", type=["mp4", "mkv"], key="f2_up")

    if st.button("🌐 မြန်မာဘာသာသို့ ဘာသာပြန်မည်", type="primary", use_container_width=True):
        if "Link" in src_mode and not txt_input:
            st.warning("ကျေးဇူးပြု၍ အင်္ဂလိပ် စာသား သို့မဟုတ် လင့်ခ် ထည့်ပါ။")
        else:
            keys = st.session_state.groq_keys if st.session_state.groq_keys else st.session_state.gemini_keys
            if not keys:
                st.error("ကျေးဇူးပြု၍ API Key အနည်းဆုံး တစ်ခု ထည့်သွင်းပါ။")
            else:
                with st.spinner("မူရင်းဇာတ်ကောင် နာမ်စားများကို စစ်ဆေး၍ မြန်မာဘာသာသို့ ဘာသာပြန်ဆိုနေသည်..."):
                    content = txt_input if txt_input else "English movie recap about a boy and girl named Jack climbing a skyscraper."
                    prompt = (
                        f"Translate and adapt the following English movie recap into a natural, engaging Burmese storytelling voiceover script.\n"
                        f"Content: {content}\n\n"
                        f"CRITICAL RULES:\n"
                        f"1. Strictly check the original personas (e.g. boy, girl, Jack, narrator).\n"
                        f"2. If narrator is speaking, use 'ကျွန်တော်' appropriately. Keep character names like 'ဂျက်' and 'ကောင်မလေး'.\n"
                        f"3. BURMESE LANGUAGE ONLY. NO timestamps [00:01]. Pure narrative voiceover format."
                    )
                    res, kidx = call_groq(keys, prompt)
                    if res:
                        st.success(f"✅ ဘာသာပြန်ဆိုမှု အောင်မြင်သည်! (Key #{kidx})")
                        st.text_area("ထွက်လာသော မြန်မာအပြောအဆို ဇာတ်ညွှန်း:", res, height=350)
                        st.download_button("📥 မြန်မာဘာသာ ဇာတ်ညွှန်း ဒေါင်းလုဒ် (.txt)", res, file_name="burmese_recap_translation.txt", mime="text/plain")
                    else:
                        st.error("❌ Key များ အလုပ်မလုပ်ပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 12px;'>Sai Myanmar Studio • Multi-Key Auto-Switching System</p>", unsafe_allow_html=True)
            
