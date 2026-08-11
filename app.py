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

# Custom CSS for compact mobile UI
st.markdown("""
<style>
.stApp {
    background-color: #0d1117;
    color: #ffffff;
}
.main-card {
    background-color: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
}
div[data-testid="stFileUploader"] {
    background-color: #21262d;
    border: 1px dashed #30363d;
    border-radius: 8px;
    padding: 10px;
}
div[data-testid="stFileUploader"] section {
    background-color: transparent !important;
}
div[data-testid="stFileUploader"] small {
    color: #8b949e !important;
}
.stButton>button {
    border-radius: 6px;
    font-weight: 600;
    padding: 4px 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎬 AI Movie Recap & Voiceover Studio</h3>", unsafe_allow_html=True)

# --- API Key Management Section ---
with st.container():
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("🔑 **API Key စီမံခန့်ခွဲမှု** (၁၀ ခုအထိ သိမ်းဆည်းနိုင်သည်)", unsafe_allow_html=True)
    
    # Gemini Keys
    st.markdown("---")
    st.markdown("✨ **Gemini API Key** &nbsp; 👉 [Key ယူရန်](https://aistudio.google.com/)")
    col_g_in, col_g_btn = st.columns([3, 1])
    with col_g_in:
        new_g = st.text_input("Gemini Key", placeholder="AlzaSy...", label_visibility="collapsed", key="in_gemini", type="password")
    with col_g_btn:
        if st.button("➕ Add", use_container_width=True, key="btn_add_gemini"):
            if new_g.strip():
                if len(st.session_state.gemini_keys) < 10:
                    if new_g.strip() not in st.session_state.gemini_keys:
                        st.session_state.gemini_keys.append(new_g.strip())
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
                else:
                    st.error("အများဆုံး ၁၀ ခု။")
    
    if st.session_state.gemini_keys:
        st.markdown("<div style='font-size: 12px; color: #8b949e; margin-top: 5px;'>သိမ်းဆည်းထားသော Gemini Keys:</div>", unsafe_allow_html=True)
        for idx, k in enumerate(st.session_state.gemini_keys):
            masked = f"Gemini #{idx+1} ({k[:4]}...{k[-4:]})" if len(k) > 8 else f"Gemini #{idx+1}"
            c_tag, c_del = st.columns([5, 1])
            with c_tag:
                st.markdown(f"<div style='background: #1f6feb22; border: 1px solid #1f6feb; color: #58a6ff; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-bottom: 4px;'>✨ {masked}</div>", unsafe_allow_html=True)
            with c_del:
                if st.button("❌", key=f"dg_{idx}"):
                    st.session_state.gemini_keys.pop(idx)
                    save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                    st.rerun()

    # Groq Keys
    st.markdown("---")
    st.markdown("⚡ **Groq API Key** &nbsp; 👉 [Key ယူရန်](https://console.groq.com/keys)")
    col_gr_in, col_gr_btn = st.columns([3, 1])
    with col_gr_in:
        new_gr = st.text_input("Groq Key", placeholder="gsk_...", label_visibility="collapsed", key="in_groq", type="password")
    with col_gr_btn:
        if st.button("➕ Add", use_container_width=True, key="btn_add_groq", type="primary"):
            if new_gr.strip():
                if len(st.session_state.groq_keys) < 10:
                    if new_gr.strip() not in st.session_state.groq_keys:
                        st.session_state.groq_keys.append(new_gr.strip())
                        save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                        st.rerun()
                else:
                    st.error("အများဆုံး ၁၀ ခု။")

    if st.session_state.groq_keys:
        st.markdown("<div style='font-size: 12px; color: #8b949e; margin-top: 5px;'>သိမ်းဆည်းထားသော Groq Keys:</div>", unsafe_allow_html=True)
        for idx, k in enumerate(st.session_state.groq_keys):
            masked = f"Groq #{idx+1} ({k[:6]}...{k[-4:]})" if len(k) > 10 else f"Groq #{idx+1}"
            c_tag, c_del = st.columns([5, 1])
            with c_tag:
                st.markdown(f"<div style='background: #23863622; border: 1px solid #238636; color: #3fb950; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-bottom: 4px;'>⚡ {masked}</div>", unsafe_allow_html=True)
            with c_del:
                if st.button("❌", key=f"dr_{idx}"):
                    st.session_state.groq_keys.pop(idx)
                    save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# API Helpers with Auto-Switching
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
tab1, tab2 = st.tabs(["🎥 Movie Recap", "🌐 English to Burmese"])

with tab1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🎬 Auto Movie Recap Voiceover Script")
    movie_file = st.file_uploader("ဗီဒီယိုဖိုင် တင်ရန် (MP4, MKV)", type=["mp4", "mkv"], key="f1")
    engine = st.radio("AI Engine", ["Gemini API", "Groq API"], horizontal=True)

    if st.button("🚀 ဇာတ်ညွှန်း ဖန်တီးမည်", type="primary", use_container_width=True):
        if not movie_file:
            st.warning("ဗီဒီယိုဖိုင် တင်ပေးပါ။")
        else:
            keys = st.session_state.gemini_keys if "Gemini" in engine else st.session_state.groq_keys
            if not keys:
                st.error("API Key ထည့်သွင်းပေးပါ။")
            else:
                with st.spinner("ပညာသားပါသော Storytelling ဇာတ်ညွှန်း ရေးသားနေသည်..."):
                    prompt = (
                        "You are an elite movie recap narrator. Write a highly engaging, smooth, and professional storytelling "
                        "voiceover script in BURMESE language ONLY. DO NOT repeat sentences unnecessarily. "
                        "Use natural phrasing like a professional YouTube movie recap creator (e.g., engaging hooks, smooth narrative flow). "
                        "NO timestamps like [00:01]. Pure narrative script."
                    )
                    res, kidx = call_gemini(keys, prompt) if "Gemini" in engine else call_groq(keys, prompt)
                    if res:
                        st.success(f"✅ အောင်မြင်သည်! (Key #{kidx})")
                        st.text_area("ထွက်လာသော ဇာတ်ညွှန်း:", res, height=300)
                        st.download_button("📥 ဒေါင်းလုဒ် (.txt)", res, file_name="recap_script.txt", mime="text/plain")
                    else:
                        st.error("❌ Key အလုပ်မလုပ်ပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown("#### 🌐 English to Burmese (Professional Storytelling Adaptation)")
    txt_input = st.text_area("အင်္ဂလိပ် Recap စာသား (သို့) လင့်ခ် ထည့်ရန်", placeholder="Paste English text or link here...")

    if st.button("🌐 မြန်မာဘာသာသို့ ဘာသာပြန်မည်", type="primary", use_container_width=True):
        if not txt_input:
            st.warning("စာသား (သို့) လင့်ခ် ထည့်ပါ။")
        else:
            keys = st.session_state.groq_keys if st.session_state.groq_keys else st.session_state.gemini_keys
            if not keys:
                st.error("API Key ထည့်သွင်းပေးပါ။")
            else:
                with st.spinner("ဆွဲဆောင်မှုရှိသော မြန်မာဘာသာ Storytelling ဇာတ်ညွှန်းအဖြစ် ပြောင်းလဲနေသည်..."):
                    prompt = (
                        f"You are a professional Burmese movie recap script writer and translator. "
                        f"Take the following English recap content and completely adapt it into an engaging, smooth, and natural "
                        f"Burmese storytelling voiceover script. DO NOT do a word-for-word clumsy translation. Avoid repetitive phrasing. "
                        f"Make it flow like a top-tier cinematic story.\n\n"
                        f"Source Content: {txt_input}\n\n"
                        f"CRITICAL RULES:\n"
                        f"1. BURMESE LANGUAGE ONLY.\n"
                        f"2. NO timestamps [00:01] or subtitle markers.\n"
                        f"3. Use proper narrative pronouns ('ကျွန်တော်', character names like 'ဂျက်', 'ကောင်မလေး') naturally without repetition."
                    )
                    res, kidx = call_groq(keys, prompt) if keys == st.session_state.groq_keys else call_gemini(keys, prompt)
                    if res:
                        st.success(f"✅ အောင်မြင်သည်! (Key #{kidx})")
                        st.text_area("မြန်မာအပြောအဆို ဇာတ်ညွှန်း:", res, height=300)
                        st.download_button("📥 ဒေါင်းလုဒ် (.txt)", res, file_name="burmese_recap.txt", mime="text/plain")
                    else:
                        st.error("❌ Key အလုပ်မလုပ်ပါ။")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #8b949e; font-size: 11px;'>Sai Myanmar Studio • Auto-Switching System</p>", unsafe_allow_html=True)
            
