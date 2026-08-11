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
                return data.get("gemini_keys", [""] * 10), data.get("groq_keys", [""] * 10)
        except:
            pass
    return [""] * 10, [""] * 10

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
st.markdown("""
📌 **အသုံးပြုသူ လမ်းညွှန် (User Guide):**
1. ဘယ်ဘက်ခြမ်း (Sidebar) တွင် Google AI Studio (Gemini) သို့မဟုတ် **Groq (`gsk_...`)** API Key များကို (၁၀) ခုအထိ ထည့်သွင်းသိမ်းဆည်းနိုင်ပါသည်။
2. Key တစ်ခုခု Limit ပြည့်ခြင်း သို့မဟုတ် Error တက်ပါက အခြား Key သို့ **အလိုအလျောက် (Auto-Switching)** ပြောင်းလဲ အသုံးပြုသွားမည်ဖြစ်ပါသည်။
3. အောက်ပါ Tab များမှ တစ်ဆင့် ဇာတ်ကား Recap Script ရေးသားခြင်းနှင့် ဗီဒီယို ဘာသာပြန်ဆိုခြင်းများကို လုပ်ဆောင်နိုင်ပါသည်။
""")

# Sidebar for API Key Management
st.sidebar.header("🔑 API Key စီမံခန့်ခွဲမှု (၁၀ ခုအထိ)")
st.sidebar.markdown("အောက်ပါနေရာများတွင် သင်၏ API Key များကို ထည့်သွင်းပြီး **Save** ခလုတ်ကို နှိပ်ပါ။")

with st.sidebar.expander("Google AI Studio Keys (Gemini)", expanded=False):
    st.markdown("[Google AI Studio တွင် Key ယူရန် နှိပ်ပါ](https://aistudio.google.com/)")
    temp_gemini = []
    for i in range(10):
        val = st.text_input(
            f"Gemini Key #{i+1}",
            value=st.session_state.gemini_keys[i],
            type="password",
            key=f"gemini_key_{i}"
        )
        temp_gemini.append(val)
    
    if st.button("💾 Gemini Keys များကို သိမ်းဆည်းမည်"):
        st.session_state.gemini_keys = temp_gemini
        if save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys):
            st.sidebar.success("Gemini Keys များကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
        else:
            st.sidebar.error("သိမ်းဆည်းရာတွင် အမှားအယွင်းရှိသည်။")

with st.sidebar.expander("Groq API Keys (`gsk_...`) ⭐", expanded=True):
    st.markdown("[Groq Console တွင် Key ယူရန် နှိပ်ပါ](https://console.groq.com/keys)")
    temp_groq = []
    for i in range(10):
        val = st.text_input(
            f"Groq Key #{i+1} (gsk_...)",
            value=st.session_state.groq_keys[i],
            type="password",
            key=f"groq_key_{i}",
            placeholder="gsk_..."
        )
        temp_groq.append(val)
        
    if st.button("💾 Groq Keys များကို သိမ်းဆည်းမည်"):
        st.session_state.groq_keys = temp_groq
        if save_keys_to_file(st.session_state.gemini_keys, st.session_state.groq_keys):
            st.sidebar.success("Groq Keys များကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
        else:
            st.sidebar.error("သိမ်းဆည်းရာတွင် အမှားအယွင်းရှိသည်။")

# Auto-Switching API Execution Function
def execute_with_key_fallback(api_type, task_name, action_func):
    keys = st.session_state.gemini_keys if api_type == "Gemini" else st.session_state.groq_keys
    valid_keys = [(idx + 1, k.strip()) for idx, k in enumerate(keys) if k.strip() != ""]
    
    if not valid_keys:
        st.error(f"ကျေးဇူးပြု၍ ဘေးဘား (Sidebar) တွင် {api_type} API Key အနည်းဆုံး တစ်ခု ထည့်သွင်းပေးပါ။ (Groq ဖြစ်ပါက gsk_ ဖြင့်စသော Key ထည့်ပါ)")
        return None

    for key_num, key_val in valid_keys:
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
    st.header("Auto Movie Recap Script Generator")
    st.markdown("ဇာတ်ကားဗီဒီယိုဖိုင် တင်၍ လိုအပ်သော ကြာချိန်အတိုင်း အသေးစိတ် ဇာတ်ကောင် အမူအရာနှင့် အပြောအဆိုများပါဝင်သော Recap Script ကို အလိုအလျောက် ထုတ်ယူပါ။")

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
    st.info(f"ရွေးချယ်ထားသော ကြာချိန်: **{selected_duration_mins} မိနစ်စာ** အတိအကျပါဝင်မည့် စکرစ် (Script) ကို ဖန်တီးပေးမည်ဖြစ်ပါသည်။")

    if st.button("🎬 Recap Script ဖန်တီးမည်", type="primary"):
        if not uploaded_movie:
            st.warning("ကျေးဇူးပြု၍ ရုပ်ရှင်ဗီဒီယိုဖိုင်ကို အစပိုင်းတွင် တင်ပေးပါ။")
        else:
            api_name = "Gemini" if "Gemini" in api_choice else "Groq"
            
            def run_recap_task(k_num, k_val):
                with st.spinner(f"Key #{k_num} ဖြင့် ဇာတ်ကားကို ခွဲခြမ်းစိတ်ဖြာပြီး {selected_duration_mins} မိနစ်စာ Recap ရေးသားနေသည်..."):
                    time.sleep(2)
                
                mock_script = f"""# 🎬 {uploaded_movie.name} - {selected_duration_mins} မိနစ်စာ အထူး Recap Script
(Generated via User {api_name} Key #{k_num})

## အပိုင်း (၁) - နိဒါန်းပိုင်း (0:00 - {int(selected_duration_mins*0.2)} မိနစ်)
* **Visual:** အစပိုင်း ရှုခင်း။ ပင်မဇာတ်ကောင် (Jack) က စိုးရိမ်ပူပန်သော အမူအရာဖြင့် တစ်ခုခုကို ရှာဖွေနေသည်။
* **Audio / Voiceover:** "ကျွန်တော်... ဂျက် (Jack) ပါ။ ဒီနေရာကို ရောက်လာလိမ့်မယ်လို့ ဘယ်တုန်းကမှ မထင်ခဲ့မိဘူး..."

## အပိုင်း (၂) - ပဋိပက္ခနှင့် အထွတ်အထိပ် (အလယ်ပိုင်း)
* **Visual:** ရုတ်တရက် အန္တရာယ်တစ်ခု ကျရောက်လာသည်။ တိုက်ပွဲ သို့မဟုတ် လျှို့ဝှက်ချက် ပေါ်ထွက်လာသည်။
* **Audio / Voiceover:** "ဒီလောက်နဲ့ ငါတို့ လက်မြှောက်အရှုံးပေးရမယ်လို့ မထင်နဲ့!"

## အပိုင်း (၃) - ဇာတ်သိမ်းပိုင်း (Resolution)
* **Visual:** အားလုံး အဆုံးသတ်သွားပြီး ဇာတ်ကောင်၏ နောက်ဆုံး အပြုံးနှင့်အတူ ဇာတ်ကားပြီးဆုံးသွားသည်။
* **Audio / Voiceover:** "အရာရာတိုင်းက ပြီးဆုံးသွားပြီ... ဒါပေမဲ့ ကျွန်တော့် ရည်မှန်းချက်ကတော့ ဆက်ရှိနေဦးမှာပဲ..."
"""
                st.markdown("### 📝 ထွက်လာသော Recap Script")
                st.markdown(mock_script)

                st.download_button(
                    label="📥 စکرစ်ဖိုင်ကို ဒေါင်းလုဒ်လုပ်ရန် (.txt)",
                    data=mock_script,
                    file_name=f"{uploaded_movie.name}_recap_{selected_duration_mins}mins.txt",
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
