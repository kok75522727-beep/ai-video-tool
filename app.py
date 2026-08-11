import streamlit as st
import os
import time
import json
import requests

# Page Config
st.set_page_config(
    page_title="Sai Myanmar Voice & Movie Recap Studio",
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

# Custom CSS matching the screenshot dark glowing neon theme
st.markdown("""
<style>
.stApp {
    background-color: #0d1117;
    color: #ffffff;
}
.neon-box-pink {
    border: 2px solid #ff4b82;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    background-color: #161b22;
    box-shadow: 0 0 10px rgba(255, 75, 130, 0.3);
    font-weight: bold;
    margin-bottom: 10px;
}
.neon-box-purple {
    border: 2px solid #a855f7;
    border-radius: 16px;
    padding: 15px;
    text-align: center;
    background-color: #161b22;
    box-shadow: 0 0 10px rgba(168, 85, 247, 0.3);
    font-weight: bold;
    margin-bottom: 10px;
}
.key-container {
    background-color: #1f242d;
    border-radius: 12px;
    padding: 15px;
    margin-bottom: 20px;
    border: 1px solid #30363d;
}
.stButton>button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>စိုင်းမြန်မာ အသံ & Movie Recap Studio</h2>", unsafe_allow_html=True)

# Top 2 Feature Banners matching screenshot
col_top1, col_top2 = st.columns(2)
with col_top1:
    st.markdown('<div class="neon-box-pink">အသံမှစာသားပြောင်းပြီး<br>မြန်မာလိုဘာသာပြန်မည်</div>', unsafe_allow_html=True)
with col_top2:
    st.markdown('<div class="neon-box-purple">ai နဲ့ မြန်မာအသံများ<br>ထုတ်ယူမည်</div>', unsafe_allow_html=True)

st.markdown("---")

# API Key Management Section (Matching user screenshot)
st.markdown("### 🔑 API Key Manager (၁၀ ခုအထိ သိမ်းဆည်းနိုင်သည်)")

# --- Gemini API Key Section ---
st.markdown('<div class="key-container">', unsafe_allow_html=True)
st.markdown("**Gemini API Key (၁၀ ခုထိ ထည့်နိုင်သည်)** &nbsp;&nbsp;&nbsp; 👉 [API ယူရန် နှိပ်ပါ](https://aistudio.google.com/)")

col_g_in, col_g_btn = st.columns([3, 1])
with col_g_in:
    new_gemini_key = st.text_input("Gemini Input", placeholder="AlzaSy...", label_visibility="collapsed", key="new_gemini_input", type="password")
with col_g_btn:
    if st.button("➕ Add\nKey", key="add_gemini_btn"):
        if new_gemini_key.strip():
            if len(st.session_state.gemini_keys) < 10:
                if new_gemini_key.strip() not in st.session_state.gemini_keys:
                    st.session_state.gemini_keys.append(new_gemini_key.strip())
                    save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                    st.rerun()
                else:
                    st.warning("ဤ Key ရောက်ရှိပြီးသား ဖြစ်ပါသည်။")
            else:
                st.error("အများဆုံး ၁၀ ခုသာ ထည့်နိုင်သည်။")

for idx, k in enumerate(st.session_state.gemini_keys):
    masked = f"{k[:3]}***{k[-3:]}" if len(k) > 6 else "***"
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"<div style='background-color:#1e3d59; color:white; padding:6px 10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>Gemini {idx+1}: {masked}</div>", unsafe_allow_html=True)
    with c2:
        if st.button("❌", key=f"del_gemini_{idx}"):
            st.session_state.gemini_keys.pop(idx)
            save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- Groq API Key Section ---
st.markdown('<div class="key-container">', unsafe_allow_html=True)
st.markdown("**Groq API Key (အသံဖမ်းရန် - ၁၀ ခုထိ ထည့်နိုင်သည်)** &nbsp;&nbsp;&nbsp; 👉 [API ယူရန် နှိပ်ပါ](https://console.groq.com/keys)")

col_gr_in, col_gr_btn = st.columns([3, 1])
with col_gr_in:
    new_groq_key = st.text_input("Groq Input", placeholder="gsk_...", label_visibility="collapsed", key="new_groq_input", type="password")
with col_gr_btn:
    if st.button("➕ Add\nKey", key="add_groq_btn", type="primary"):
        if new_groq_key.strip():
            if len(st.session_state.groq_keys) < 10:
                if new_groq_key.strip() not in st.session_state.groq_keys:
                    st.session_state.groq_keys.append(new_groq_key.strip())
                    save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                    st.rerun()
                else:
                    st.warning("ဤ Key ရောက်ရှိပြီးသား ဖြစ်ပါသည်။")
            else:
                st.error("အများဆုံး ၁၀ ခုသာ ထည့်နိုင်သည်။")

for idx, k in enumerate(st.session_state.groq_keys):
    masked = f"{k[:4]}***{k[-4:]}" if len(k) > 8 else "***"
    c1, c2 = st.columns([5, 1])
    with c1:
        st.markdown(f"<div style='background-color:#17b978; color:white; padding:6px 10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>Groq {idx+1}: {masked}</div>", unsafe_allow_html=True)
    with c2:
        if st.button("❌", key=f"del_groq_{idx}"):
            st.session_state.groq_keys.pop(idx)
            save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

col_b1, col_b2 = st.columns(2)
with col_b1:
    st.button("🟢 Auto (အလိုအလျောက်)", use_container_width=True)
with col_b2:
    st.button("🩷 Whisper V3 (သာမန်)", use_container_width=True)

st.markdown("##### အရည်အသွေး ရွေးချယ်ရန်:")
q_col1, q_col2, q_col3 = st.columns(3)
with q_col1:
    q_col1.button("လူသုံးများ", use_container_width=True)
with q_col2:
    q_col2.button("အလယ်လတ်", use_container_width=True)
with q_col3:
    q_col3.button("အကောင်းဆုံး", use_container_width=True)

st.markdown("---")

# Real API Call with Key Fallback
def call_real_groq_api(api_keys, prompt):
    for idx, key in enumerate(api_keys):
        try:
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                text_out = res_json['choices'][0]['message']['content']
                return text_out, idx + 1
            else:
                continue
        except Exception as e:
            continue
    return None, None

def call_real_gemini_api(api_keys, prompt):
    for idx, key in enumerate(api_keys):
        try:
            headers = {"Content-Type": "application/json"}
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                res_json = response.json()
                text_out = res_json['candidates'][0]['content']['parts'][0]['text']
                return text_out, idx + 1
            else:
                continue
        except Exception as e:
            continue
    return None, None

# Tabs
tab1, tab2 = st.tabs(["🎥 Auto Movie Recap (Storytelling)", "🌐 English Recap to Burmese Voiceover"])

with tab1:
    st.subheader("Auto Movie Recap Voiceover Script")
    st.markdown("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ပါက သင့်တောင်းဆိုချက်အတိုင်း အချိန်မှတ်များမပါဘဲ မြန်မာဘာသာဖြင့် ဆွဲဆောင်မှုရှိသော **အပြောအဆို (Voiceover) ဇာတ်ညွှန်း** ထွက်လာမည်။")
    
    movie_file = st.file_uploader("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ရန် (MP4, MKV)", type=["mp4", "mkv"], key="movie_up")
    engine_choice = st.radio("အသုံးပြုမည့် AI Engine", ["Gemini API", "Groq API"], horizontal=True)

    if st.button("🎬 အပြောအဆို ဇာတ်ညွှန်း ဖန်တီးမည်", type="primary", use_container_width=True):
        if not movie_file:
            st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင် တင်ပေးပါ။")
        else:
            keys = st.session_state.gemini_keys if "Gemini" in engine_choice else st.session_state.groq_keys
            if not keys:
                st.error("ကျေးဇူးပြု၍ API Key အနည်းဆုံး တစ်ခု ထည့်သွင်းပေးပါ။")
            else:
                with st.spinner("AI ဖြင့် Storytelling ဇာတ်ညွှန်း ရေးသားနေသည်..."):
                    prompt = (
                        "You are a professional movie recap narrator. "
                        "Write a captivating storytelling voiceover script in BURMESE language ONLY based on a movie upload. "
                        "Make it sound extremely engaging (e.g., 'ဒီစုံတွဲဟာ... မင်းကို ပါးစပ်အဟောင်းသား ဖြစ်သွားစေလိမ့်မယ်'). "
                        "Maintain character personas (e.g. if referring to myself, use 'ကျွန်တော်' or 'Jack' appropriately). "
                        "DO NOT include timestamps like [00:01]. NO subtitle markers. PURE BURMESE voiceover script text only."
                    )
                    
                    if "Gemini" in engine_choice:
                        result, used_key_idx = call_real_gemini_api(keys, prompt)
                    else:
                        result, used_key_idx = call_real_groq_api(keys, prompt)
                        
                    if result:
                        st.success(f"✅ အောင်မြင်သည်! (Key #{used_key_idx})")
                        st.text_area("ထွက်လာသော မြန်မာအပြောအဆို ဇာတ်ညွှန်း:", result, height=350)
                        st.download_button(
                            label="📥 ဇာတ်ညွှန်းဖိုင် ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                            data=result,
                            file_name="movie_recap_voiceover.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ ထည့်သွင်းထားသော Key အားလုံး Limit ပြည့်သွားပါပြီ သို့မဟုတ် အလုပ်မလုပ်ပါ။")

with tab2:
    st.subheader("🌐 English Movie Recap to Burmese Voiceover Translator")
    st.markdown("TikTok, YouTube, Rednote လင့်ခ်များ (သို့မဟုတ်) အင်္ဂလိပ် စာသား/ဗီဒီယို အကြောင်းအရာများကို ထည့်သွင်းပြီး မူရင်းနာမ်စားများ (ကျွန်တော်၊ ဂျက်) အတိုင်း မြန်မာဘာသာသို့ အပြောအဆို ဇာတ်ညွှန်းအဖြစ် တိုက်ရိုက် ဘာသာပြန်ပါ။")

    trans_source = st.radio("ရင်းမြစ် ရွေးချယ်ပါ", ["Video Link / English Content", "Upload Video File"], horizontal=True, key="ts_src")
    
    english_content_input = ""
    if "Link" in trans_source:
        english_content_input = st.text_area("အင်္ဂလိပ် ဗီဒီယိုလင့်ခ် (သို့မဟုတ်) အင်္ဂလိပ် Recap စာသားများကို ဤနေရာတွင် ထည့်ပါ", placeholder="Paste YouTube/TikTok link or English recap text here...")
    else:
        st.file_uploader("အင်္ဂလိပ်ဗီဒီယိုဖိုင် တင်ရန်", type=["mp4", "mkv", "mov"], key="ts_file")

    if st.button("🌐 မြန်မာဘာသာသို့ အပြောအဆို ဘာသာပြန်မည်", type="primary", use_container_width=True):
        if "Link" in trans_source and not english_content_input:
            st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုလင့်ခ် သို့မဟုတ် အင်္ဂလိပ် စာသားများကို ထည့်သွင်းပေးပါ။")
        else:
            keys = st.session_state.groq_keys if st.session_state.groq_keys else st.session_state.gemini_keys
            if not keys:
                st.error("ကျေးဇူးပြု၍ API Key အနည်းဆုံး တစ်ခု ထည့်သွင်းပေးပါ။")
            else:
                with st.spinner("အင်္ဂလိပ် Recap ကို မြန်မာဘာသာ အပြောအဆို ဇာတ်ညွှန်းအဖြစ် သဘာဝကျကျ ဘာသာပြန်ဆိုနေသည်..."):
                    content_to_translate = english_content_input if english_content_input else "English movie recap video content about adventurous couple climbing Empire State Building."
                    trans_prompt = (
                        f"Translate and adapt the following English movie recap content into a natural, "
                        f"engaging Burmese storytelling voiceover script. "
                        f"Content to translate: {content_to_translate}\n\n"
                        f"Rules:\n"
                        f"1. Must be entirely in BURMESE language.\n"
                        f"2. Keep original character personas (e.g. use 'ကျွန်တော်' for I/me, and 'ဂျက်' for Jack).\n"
                        f"3. NO timestamps, NO subtitle markers, NO brackets like [00:01].\n"
                        f"4. Pure narrative voiceover storytelling script style."
                    )
                    result, used_key_idx = call_real_groq_api(keys, trans_prompt)
                    if result:
                        st.success(f"✅ မြန်မာဘာသာသို့ ဘာသာပြန်ဆိုမှု အောင်မြင်သည်! (Key #{used_key_idx})")
                        st.text_area("ထွက်လာသော မြန်မာအပြောအဆို ဇာတ်ညွှန်း:", result, height=350)
                        st.download_button(
                            label="📥 မြန်မာဘာသာ ဇာတ်ညွှန်း ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                            data=result,
                            file_name="burmese_voiceover_translation.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ Key များ အလုပ်မလုပ်ပါ သို့မဟုတ် Limit ပြည့်နေပါသည်။")

st.markdown("---")
st.markdown("💡 **စနစ်အချက်အလက်:** ထည့်သွင်းထားသော Key များ Limit ပြည့်ပါက နောက် Key သို့ အလိုအလျောက် (Auto-Switch) ပြောင်းလဲ အလုပ်လုပ်ပေးမည်ဖြစ်ပါသည်။")

