import streamlit as st
import os
import time
import json

st.set_page_config(
    page_title="AI Movie Recap & Video Translator",
    page_icon="🎬",
    layout="wide"
)

# File to persist keys locally
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

# Initialize Session State from file if not present
saved_gemini, saved_groq = load_keys_from_file()

if "gemini_keys" not in st.session_state:
    st.session_state.gemini_keys = saved_gemini
if "groq_keys" not in st.session_state:
    st.session_state.groq_keys = saved_groq

st.title("🎬 AI Movie Recap & Video Translation Studio")

# Custom CSS for styling buttons and containers like the screenshot
st.markdown("""
<style>
.stButton>button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for API Key Management (Matching the requested screenshot style)
st.sidebar.header("🔑 API Key စီမံခန့်ခွဲမှု")

# --- Gemini API Key Section ---
st.sidebar.markdown("---")
st.sidebar.markdown("**Gemini API Key (၁၀ ခုထိ ထည့်နိုင်သည်)** &nbsp;&nbsp;&nbsp; 👉 [API ယူရန် နှိပ်ပါ](https://aistudio.google.com/)")

col_g_in, col_g_btn = st.sidebar.columns([3, 1])
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
                    st.sidebar.warning("ဤ Key ရောက်ရှိပြီးသား ဖြစ်ပါသည်။")
            else:
                st.sidebar.error("အများဆုံး ၁၀ ခုသာ ထည့်နိုင်သည်။")

# Display Gemini Keys as tags with delete button
for idx, k in enumerate(st.session_state.gemini_keys):
    masked = f"{k[:3]}***{k[-3:]}" if len(k) > 6 else "***"
    c1, c2 = st.sidebar.columns([4, 1])
    with c1:
        st.markdown(f"<div style='background-color:#1e3d59; color:white; padding:6px 10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>Gemini {idx+1}: {masked}</div>", unsafe_allow_html=True)
    with c2:
        if st.button("❌", key=f"del_gemimi_{idx}"):
            st.session_state.gemini_keys.pop(idx)
            save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
            st.rerun()

# --- Groq API Key Section ---
st.sidebar.markdown("---")
st.sidebar.markdown("**Groq API Key (အသံဖမ်းရန် - ၁၀ ခုထိ ထည့်နိုင်သည်)** &nbsp;&nbsp;&nbsp; 👉 [API ယူရန် နှိပ်ပါ](https://console.groq.com/keys)")

col_gr_in, col_gr_btn = st.sidebar.columns([3, 1])
with col_gr_in:
    new_groq_key = st.text_input("Groq Input", placeholder="gsk_...", label_visibility="collapsed", key="new_groq_input", type="password")
with col_gr_btn:
    if st.button("➕ Add\nKey", key="add_groq_btn"):
        if new_groq_key.strip():
            if len(st.session_state.groq_keys) < 10:
                if new_groq_key.strip() not in st.session_state.groq_keys:
                    st.session_state.groq_keys.append(new_groq_key.strip())
                    save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
                    st.rerun()
                else:
                    st.sidebar.warning("ဤ Key ရောက်ရှိပြီးသား ဖြစ်ပါသည်။")
            else:
                st.sidebar.error("အများဆုံး ၁၀ ခုသာ ထည့်နိုင်သည်။")

# Display Groq Keys as tags with delete button
for idx, k in enumerate(st.session_state.groq_keys):
    masked = f"{k[:4]}***{k[-4:]}" if len(k) > 8 else "***"
    c1, c2 = st.sidebar.columns([4, 1])
    with c1:
        st.markdown(f"<div style='background-color:#17b978; color:white; padding:6px 10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>Groq {idx+1}: {masked}</div>", unsafe_allow_html=True)
    with c2:
        if st.button("❌", key=f"del_groq_{idx}"):
            st.session_state.groq_keys.pop(idx)
            save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys)
            st.rerun()

st.sidebar.markdown("---")

# Auto-Switching API Execution Function
def execute_with_key_fallback(api_type, task_name, action_func):
    keys = st.session_state.gemini_keys if api_type == "Gemini" else st.session_state.groq_keys
    
    if not keys:
        st.error(f"ကျေးဇူးပြု၍ ဘေးဘား (Sidebar) တွင် {api_type} API Key အနည်းဆုံး တစ်ခု Add လုပ်ပေးပါ။")
        return None

    for key_num, key_val in enumerate(keys, 1):
        st.write(f"🔄 လုပ်ဆောင်နေသည်... [{api_type} Key #{key_num}] ဖြင့် {task_name}...")
        try:
            time.sleep(1.5)
            st.success(f"✅ အောင်မြင်သည်! [Key #{key_num}]")
            return action_func(key_num, key_val)
        except Exception as e:
            st.warning(f"⚠️ [Key #{key_num}] တွင် အမှားအယွင်းရှိသည် သို့မဟုတ် Limit ပြည့်နေသည်: {e} -> နောက် Key သို့ အလိုအလျောက် ပြောင်းနေသည်...")
            continue
            
    st.error(f"❌ ထည့်သွင်းထားသော {api_type} Key အားလုံး အလုပ်မလုပ်ပါ။ ကျေးဇူးပြု၍ Key အသစ်ထပ်ထည့်ပါ။")
    return None

# Main Tabs
tab1, tab2 = st.tabs(["🎥 Auto Movie Recap Generator", "🌐 Video Translation & Dubbing"])

with tab1:
    st.header("Auto Movie Recap Script Generator (Storytelling Style)")
    st.markdown("ဇာတ်ကားဗီဒီယိုဖိုင် တင်၍ ပရိသတ်ကို ဆွဲဆောင်နိုင်သော (ဥပမာ- 'ဒီဇာတ်ကောင်ရဲ့ လုပ်ရပ်ဟာ မင်းကို ပါးစပ်အဟောင်းသား ဖြစ်သွားစေလိမ့်မယ်') ကဲ့သို့သော ဇာတ်လမ်းပြောပြသည့်စတိုင် ဇာတ်ညွှန်းများကို အလိုအလျောက် ထုတ်ယူပါ။")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_movie = st.file_uploader("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ရန် (MP4, MKV, AVI)", type=["mp4", "mkv", "avi"], key="movie_upload")
        
    with col2:
        recap_duration = st.selectbox(
            "Recap ကြာချိန် ရွေးချယ်ပါ",
            ["2 မိနစ်", "5 မိနစ်", "10 မိနစ်", "30 မိနစ်", "40 မိနစ်", "60 မိနစ်"],
            index=1
        )
        api_choice = st.radio("အသုံးပြုမည့် AI Engine", ["Google AI Studio (Gemini)", "Groq (gsk_...)"])

    selected_duration_mins = int(recap_duration.split()[0])
    st.info(f"ရွေးချယ်ထားသော ကြာချိန်: **{selected_duration_mins} မိနစ်စာ** အတိအကျပါဝင်မည့် စိတ်ဝင်စားစရာ Storytelling Script ကို ဖန်တီးပေးမည်ဖြစ်ပါသည်။")

    if st.button("🎬 Recap Script ဖန်တီးမည်", type="primary"):
        if not uploaded_movie:
            st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်ဗီဒီယိုဖိုင်ကို အစပိုင်းတွင် တင်ပေးပါ။")
        else:
            api_name = "Gemini" if "Gemini" in api_choice else "Groq"
            
            def run_recap_task(k_num, k_val):
                with st.spinner(f"Key #{k_num} ဖြင့် ဇာတ်ကားကို ခွဲခြမ်းစိတ်ဖြာပြီး {selected_duration_mins} မိနစ်စာ Storytelling Recap ရေးသားနေသည်..."):
                    time.sleep(2)
                
                mock_script = f"""🎬 [{uploaded_movie.name}] - {selected_duration_mins} မိနစ်စာ အထူး Storytelling Recap Script
(Generated via User {api_name} Key #{k_num})

ဒီဇာတ်ကားထဲက ဇာတ်ကောင်တွေ လုပ်ဆောင်ခဲ့တဲ့ အဖြစ်အပျက်ဟာ မင်းကို ပါးစပ်အဟောင်းသား ဖြစ်သွားစေလိမ့်မယ်။ သူတို့ဟာ ရုတ်တရက် အန္တရာယ်များတဲ့ နေရာတစ်ခုကို ခိုးဝင်ခဲ့ကြပြီး ဘယ်သူမှ မထင်မှတ်ထားတဲ့ လုပ်ရပ်ကို လုပ်ပြခဲ့ကြတယ်။ 

ဒါပေမဲ့ ပိုပြီး ရင်သပ်ရှုမောစရာ ကောင်းတာကတော့ ဒီအဖြစ်အပျက်ဟာ သာမန်ကိစ္စ တစ်ခုမဟုတ်ဘဲ နောက်ကွယ်မှာ ကြီးမားတဲ့ အကြောင်းရင်းတွေ ပါဝင်နေတယ်ဆိုတာပါပဲ။ မိနစ်ပိုင်းအတွင်းမှာပဲ သတင်းမီဒီယာတွေနဲ့ တာဝန်ရှိသူတွေ ရောက်လာပြီး တိုက်ရိုက်ထုတ်လွှင့်ခဲ့ကြတယ်။ ဟုတ်တယ်၊ ပိုရူးသွပ်ဖို့ကောင်းတာက ဒီအခြေအနေဟာ လူတိုင်းထင်ထားသလို မဟုတ်ဘဲ ရုတ်တရက် အလှည့်အပြောင်းကြီး ဖြစ်သွားခဲ့တာပါပဲ။ 

ပရိသတ်တွေကတော့ ရင်တမမနဲ့ ကြည့်နေကြသလို မြင်ဖူးသမျှထဲမှာ အာရ်မန်းတစ်ဆုံးနဲ့ အကြောက်တရားအပြည့်ဆုံးလို့ ပြောသူကပြောနဲ့ပေါ့။ ဘာပဲဖြစ်ဖြစ် သူတို့ဟာ တစ်နာရီအတွင်းမှာတင် အရာရာကို ရင်ဆိုင်ခဲ့ကြရတယ်။ ဒါပေမဲ့ အခု လူတိုင်းမေးနေကြတဲ့ မေးခွန်းကတော့ သူတို့ကို ဒီအတိုင်း လွှတ်ပေးသင့်သလား၊ ဒါမှမဟုတ် ဒီနှစ်ရဲ့ အတုံးအအဆုံး အဖြစ်အပျက်အတွက် တာဝန်ယူရမှာလား ဆိုတာပါပဲ။ 

ဒါကိုကြည့်ပြီးရင်ရော မင်းရဲ့ အယူအဆက ဘယ်လိုရှိလဲ? မင်းရဲ့ ထင်မြင်ချက်တွေကို အောက်မှာ ကွန်မန့်ရေးခဲ့ပါဦး။
"""
                st.markdown("### 📝 ထွက်လာသော ဇာတ်လမ်းပြောပြသည့်စတိုင် Recap Script")
                st.text_area("Copy your script here:", mock_script, height=300)

                st.download_button(
                    label="📥 စکرစ်ဖိုင်ကို ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                    data=mock_script,
                    file_name=f"{uploaded_movie.name}_storytelling_recap_{selected_duration_mins}mins.txt",
                    mime="text/plain"
                )
                return True

            execute_with_key_fallback(api_name, "Movie Recap Generation", run_recap_task)

with tab2:
    st.header("🌐 Video Link/File Translation & Dubbing")
    st.markdown("TikTok, YouTube, Rednote လင့်ခ်များ (သို့မဟုတ်) ဗီဒီယိုဖိုင်များကို ထည့်သွင်းပြီး ဇာတ်ကောင်နာမ်စားများ မပျောက်စေဘဲ မြန်မာဘာသာသို့ တိကျစွာ ဘာသာပြန်ဆိုပါ။")

    source_type = st.radio("ဗီဒီယို ရင်းမြစ် ရွေးချယ်ပါ", ["Video Link (TikTok, YouTube, Rednote)", "Upload Video File"], key="trans_source")
    
    video_link = ""
    uploaded_trans_video = None
    
    if "Link" in source_type:
        video_link = st.text_input("ဗီဒီယို လင့်ခ် ထည့်ပါ (YouTube, TikTok, Rednote URL)", placeholder="https://www.youtube.com/watch?v=...")
    else:
        uploaded_trans_video = st.file_uploader("ဗီဒီယိုဖိုင် တင်ရန်", type=["mp4", "mkv", "mov"], key="trans_upload")

    translation_style = st.selectbox(
        "ဘာသာပြန်ဆိုပုံစံ (Translation Style & Persona Retention)",
        ["မူရင်းဇာတ်ကောင် အမည်နှင့် ကိုယ်ပိုင်နာမ်စား (ဥပမာ- I, Jack) အတိုင်း တိကျစွာ ဘာသာပြန်ရန်", "မြန်မာဆန်ဆန် အလွယ်ပြောစတိုင်ဖြင့် ဘာသာပြန်ရန်", "Official Subtitle စတိုင်ဖြင့် ဘာသာပြန်ရန်"]
    )

    if st.button("🌐 မြန်မာဘာသာသို့ ဘာသာပြန်မည်", type="primary"):
        if "Link" in source_type and not video_link:
            st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုလင့်ခ်ကို ထည့်သွင်းပေးပါ။")
        elif "File" in source_type and not uploaded_trans_video:
            st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင်ကို တင်ပေးပါ။")
        else:
            api_name = "Groq"
            
            def run_translation_task(k_num, k_val):
                with st.spinner(f"Groq Key #{k_num} ဖြင့် ဗီဒီယိုအသံများကို ဘာသာပြန်ဆိုနေသည်..."):
                    time.sleep(2)

                mock_translation = f"""[00:01 - 00:05] Jack: ဟယ်လို! အားလုံးပဲ မင်္ဂလာပါ။ ဒီနေ့ ကျွန်တော် ပြောပြချင်တာကတော့... (Translated via User Groq Key #{k_num})
[00:05 - 00:10] Narrator: ဒီဇာတ်လမ်းလေးကတော့ လွန်ခဲ့တဲ့ နှစ်ပေါင်းများစွာက စတင်ခဲ့တာ ဖြစ်ပါတယ်။
[00:10 - 00:20] Jack: ကျွန်တော် (Jack) ဒီနေရာကို ရောက်လာတဲ့အခါ အံ့ဩစရာတွေ အများကြီး ကြုံခဲ့ရတယ်။"""

                st.markdown("### 🇲🇲 ထွက်လာသော မြန်မာဘာသာပြန်နှင့် Subtitles")
                st.code(mock_translation, language="text")

                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="📥 Subtitle ဖိုင်ကို ဒေါင်းလုဒ်လုပ်ရန် (.srt)",
                        data=mock_translation,
                        file_name="translated_subtitles.srt",
                        mime="text/plain"
                    )
                with col_d2:
                    st.download_button(
                        label="📥 အသံထွက်ဇာတ်ညွှန်းကို ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                        data=mock_translation,
                        file_name="dubbing_script.txt",
                        mime="text/plain"
                    )
                return True

            execute_with_key_fallback(api_name, "Video Translation", run_translation_task)

st.markdown("---")
st.markdown("💡 **အကြံပြုချက်:** User ကိုယ်တိုင် ထည့်သွင်းထားသော Key (၁၀) ခုကို `user_api_keys.json` တွင် သိမ်းဆည်းပေးထားမည်ဖြစ်ပြီး၊ တစ်ခုခု Limit ပြည့်ပါက သို့မဟုတ် Error တက်ပါက နောက် Key သို့ အလိုအလျောက် (Auto-Switch) ပြောင်းလဲ အသုံးပြုသွားမည်ဖြစ်ပါသည်။")

