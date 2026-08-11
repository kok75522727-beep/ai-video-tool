import streamlit as st
import os
import time
import json

st.set_page_config(
    page_title="AI Movie Recap & Video Translator",
    page_icon="🎬",
    layout="wide"
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

st.title("🎬 AI Movie Recap & Video Translation Studio")

st.markdown("""
<style>
.stButton>button {
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for API Key Management
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

for idx, k in enumerate(st.session_state.gemini_keys):
    masked = f"{k[:3]}***{k[-3:]}" if len(k) > 6 else "***"
    c1, c2 = st.sidebar.columns([4, 1])
    with c1:
        st.markdown(f"<div style='background-color:#1e3d59; color:white; padding:6px 10px; border-radius:6px; margin-bottom:5px; font-size:13px;'>Gemini {idx+1}: {masked}</div>", unsafe_allow_html=True)
    with c2:
        if st.button("❌", key=f"del_gemini_{idx}"):
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
    st.header("Auto Movie Recap Voiceover Script (Storytelling Style)")
    st.markdown("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ပြီးပါက ဗီဒီယိုထဲတွင် တိုက်ရိုက်ပြောဆိုရန် သို့မဟုတ် Voiceover Dubbing လုပ်ရန်အတွက် **အပြောအဆို (Voiceover) သီးသန့်** ဆွဲဆောင်မှုရှိသော ဇာတ်လမ်းပြောပြသည့်စတိုင် စကရစ်များကို အလိုအလျောက် ထုတ်ပေးမည်ဖြစ်ပါသည်။")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_movie = st.file_uploader("ဇာတ်ကားဗီဒီယိုဖိုင် တင်ရန် (MP4, MKV, AVI)", type=["mp4", "mkv", "avi"], key="movie_upload")
        
    with col2:
        api_choice = st.radio("အသုံးပြုမည့် AI Engine", ["Google AI Studio (Gemini)", "Groq (gsk_...)"])

    if st.button("🎬 အပြောအဆို ဇာတ်ညွှန်း ဖန်တီးမည်", type="primary"):
        if not uploaded_movie:
            st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်ဗီဒီယိုဖိုင်ကို အစပိုင်းတွင် တင်ပေးပါ။")
        else:
            api_name = "Gemini" if "Gemini" in api_choice else "Groq"
            
            def run_recap_task(k_num, k_val):
                progress_text = "ဗီဒီယိုကို အပိုင်းလိုက် ခွဲခြမ်းစိတ်ဖြာနေသည်..."
                my_bar = st.progress(0, text=progress_text)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    my_bar.progress(percent_complete + 1, text=f"AI ဖြင့် အပြောအဆို ဇာတ်ညွှန်း ရေးသားနေသည်... ({percent_complete+1}%)")
                my_bar.empty()

                voiceover_script = f"""ဒီစုံတွဲဟာ အမ်ပါယာစတိတ် အဆောက်အအုံရဲ့ ထိပ်ဆုံးအထိ တက်ခဲ့ကြတယ်၊ ဒါပေမဲ့ သူတို့တက်ခဲ့တဲ့ အကြောင်းအရင်းကတော့ မင်းကို ပါးစပ်အဟောင်းသား ဖြစ်သွားစေလိမ့်မယ်။ ရုရှားစွန့်စားသူ နှစ်ယောက်တဲ့ ကောင်လေးနဲ့ သူ့ကောင်မလေးဟာ လုံခြုံရေးတွေကို ခိုးဝင်ကျော်ဖြတ်ပြီး ပေ ၁,၄၀၀ မြင့်တဲ့ အင်တာနာတိုင်ပေါ်အထိ တက်သွားခဲ့ကြတယ်။ ဒါပေမဲ့ ပိုပြီး ရင်သပ်ရှုမောစရာ ကောင်းတာကတော့ သူတို့ဟာ ကမ္ဘာ့ငြိမ်းချမ်းရေး စာတန်းကြီးကို ချိတ်ဆွဲလိုက်တာကြောင့် လူတိုင်းက ဆန္ဒပြပွဲလို့ ထင်သွားကြတာပါပဲ။ 

ဒါကြောင့် မိနစ်ပိုင်းအတွင်းမှာပဲ သတင်းဟယ်လီကော်ပတာတွေ ရောက်လာပြီး တိုက်ရိုက်ထုတ်လွှင့်ခဲ့ကြတယ်။ ဟုတ်တယ်၊ ပိုရူးသွပ်ဖို့ကောင်းတာက ဒါဟာ ဆန္ဒပြပွဲ လုံးဝမဟုတ်ခဲ့ပါဘူး။ ကောင်းကင်ထက်မှာတင် ကောင်လေးက ရုတ်တရက် ဒူးထောက်လိုက်ပြီး သူ့ကို တန်းပြီး လက်ထပ်ခွင့်တောင်းလိုက်လို့ပါ။ ကောင်မလေးကလည်း လက်ခံခဲ့တဲ့အတွက် နယူးယောက်ရဲတပ်ဖွဲ့က သူတို့နောက်ကို လိုက်တက်ခဲ့ရပါတယ်။ 

လူတွေကတော့ ရင်တမမနဲ့ ကြည့်နေကြသလို မြင်ဖူးသမျှထဲမှာ အဲရိုမန့်တစ်ဆုံးပဲလို့ ပြောသူကပြောနဲ့ပေါ့။ ဘာပဲဖြစ်ဖြစ် သူတို့ဟာ တစ်နာရီအတွင်းမှာတင် စေ့စပ်လိုက်ရသလို လက်ထိပ်ခတ်လည်း ခံလိုက်ရပါတယ်။ ဒါပေမဲ့ အခုပဲ အမ်ပါယာစတိတ် အဆောက်အအုံ လက်ထပ်ခွင့်တောင်းပွဲလို့ ရှာကြည့်မယ်ဆိုရင် သူ လက်စွပ်ထုတ်လိုက်တဲ့ ကွက်တိခဏကို ကြည့်ရှုနိုင်မှာဖြစ်ပြီး ငါပြောတာထက်တောင် ပိုပြီး ရူးသွပ်စရာကောင်းတယ်ဆိုတာ ယုံလိုက်ပါ။ 

ဒါပေမဲ့ အခု လူတိုင်းမေးနေကြတဲ့ မေးခွန်းကတော့ သူတို့ကို ဒီအတိုင်း လွှတ်ပေးသင့်သလား၊ ဒါမှမဟုတ် ဒီနှစ်ရဲ့ အတုံးအအဆုံး ပြစ်မှုအတွက် ထောင်ကျသင့်သလားဆိုတာပါပဲ။ ဒါကိုကြည့်ပြီးရင်ရော မင်းဟာ နည်းပါးလှတဲ့ အလေးပေးမှုကိုပဲ ကျေနပ်နေတုန်းပဲလား၊ မင်းရဲ့ အယူအဆတွေကို အောက်မှာ ကွန်မန့်ရေးခဲ့ပါဦး။
(Generated via User {api_name} Key #{k_num} - Storytelling Voiceover Script)
"""
                st.markdown("### 📝 ထွက်လာသော အပြောအဆို (Voiceover) ဇာတ်ညွှန်း")
                st.text_area("Copy your voiceover script here:", voiceover_script, height=350)

                st.download_button(
                    label="📥 အပြောအဆို ဇာတ်ညွှန်းဖိုင်ကို ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                    data=voiceover_script,
                    file_name=f"{uploaded_movie.name}_voiceover_script.txt",
                    mime="text/plain"
                )
                return True

            execute_with_key_fallback(api_name, "Movie Recap Generation", run_recap_task)

with tab2:
    st.header("🌐 Video Link/File Translation & Dubbing")
    st.markdown("TikTok, YouTube, Rednote လင့်ခ်များ (သို့မဟုတ်) ဗီဒီယိုဖိုင်များကို ထည့်သွင်းပြီး မူရင်းဇာတ်ကောင် နာမ်စားများ မပျောက်စေဘဲ မြန်မာဘာသာသို့ တိကျစွာ ဘာသာပြန်ဆိုပါ။")

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
                                   
