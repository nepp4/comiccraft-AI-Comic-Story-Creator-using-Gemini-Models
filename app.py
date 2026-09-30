import streamlit as st
import urllib.parse
import random

st.set_page_config(page_title="ComicCraft: AI Comic Story Creation", page_icon="📚", layout="wide")

st.title("📚 ComicCraft: AI Comic Story Creation")
st.caption("AI-Powered Comic Story and Dynamic Visual Comic Panel Generator")

with st.sidebar:
    st.header("⚙️ Configuration")
    genre = st.selectbox("Story Genre", ["Superhero", "Sci-Fi", "Action & Adventure", "Fantasy", "Mystery", "Anime"])
    art_style = st.selectbox("Visual Style", [
        "Classic American Comic Book (Marvel/DC style)",
        "Japanese Manga / Anime",
        "Vintage 90s Graphic Novel",
        "Cyberpunk Vibrant Comic"
    ])
    panels_count = st.slider("Visual Story Panels", min_value=3, max_value=4, value=4)

story_idea = st.text_area(
    "Enter your story concept or premise:", 
    placeholder="E.g., a girl found speaking cat in the road"
)

if st.button("🚀 Create Full Comic Story"):
    clean_idea = story_idea.strip()
    if not clean_idea:
        st.warning("Please enter a story concept!")
    else:
        with st.spinner("Drawing comic art panels and scripting dialogue..."):
            title = f"The Tale of {clean_idea.title()[:30]}"
            
            # Story Section
            st.markdown(f"# 📖 {title}")
            st.markdown(f"**Genre:** `{genre}` | **Art Style:** `{art_style}`")
            
            st.subheader("📜 Story Narrative")
            st.write(
                f"An ordinary day took a magical twist when {clean_idea}. "
                f"Under the vibrant atmosphere of a {art_style.lower()}, unexpected secrets began to surface. "
                f"What started as a shocking encounter soon opened doors to an unforgettable adventure, "
                f"pulling everyone into a whirlwind of destiny and courage."
            )
            
            st.subheader("👥 Character Profiles")
            st.markdown(f"- **Lead Character**: A courageous young protagonist experiencing the event of '{clean_idea[:25]}'.")
            st.markdown(f"- **Key Figure / Mystery Guide**: The talking, enchanted creature whose voice holds ancient secrets.")
            
            st.markdown("---")
            
            # Panels with Story-Specific Prompts
            st.subheader("🖼️ Comic Story Visual Panels")
            
            panel_data = [
                {
                    "title": "The Strange Encounter",
                    "action": f"Close-up comic illustration of {clean_idea}, wide shocked eyes, detailed street background",
                    "dialogue": "Wait... did you just speak words to me?!",
                    "sfx": "GASP!"
                },
                {
                    "title": "The Secret Unfolds",
                    "action": f"Mystical talking creature replying with glowing eyes, {clean_idea}, glowing aura, dramatic angle",
                    "dialogue": "Listen carefully, there isn't much time before they arrive!",
                    "sfx": "MEOWW-SHING!"
                },
                {
                    "title": "Danger Approaches",
                    "action": f"Dark robotic shadows chasing down {clean_idea}, dynamic action motion lines, intense perspective",
                    "dialogue": "They tracked us down! We need to move now!",
                    "sfx": "RUMBLE!"
                },
                {
                    "title": "Leap of Faith",
                    "action": f"Hero running away holding the miraculous talking creature, jumping across rooftops, comic burst background",
                    "dialogue": "Hold on tight! Here we go!",
                    "sfx": "WHOOSH!"
                }
            ]
            
            # Style prompt modifiers to force authentic comic look
            style_tags = (
                "comic book art style, graphic novel panel, clear bold ink outlines, "
                "vibrant cinematic comic coloring, speech bubble aesthetic, masterpiece"
            )
            
            cols = st.columns(2)
            base_seed = random.randint(100, 99999)
            
            for idx in range(panels_count):
                p = panel_data[idx % len(panel_data)]
                with cols[idx % 2]:
                    st.markdown(f"#### Panel {idx + 1}: {p['title']}")
                    
                    # Exact story-based prompt with heavy comic-style modifiers
                    full_image_prompt = f"{p['action']}, {art_style}, {style_tags}"
                    encoded_prompt = urllib.parse.quote(full_image_prompt)
                    
                    # Direct free AI image synthesis url with unique seed for variety
                    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512&seed={base_seed + idx}&nologo=true"
                    
                    st.image(image_url, use_container_width=True, caption=f"Panel {idx + 1} - [{art_style}]")
                    
                    st.warning(f"💥 **SFX:** {p['sfx']}")
                    st.info(f"🗣️ **Dialogue:** \"{p['dialogue']}\"")
                    st.markdown("---")
                    
            st.success("✅ Complete Illustrated Comic Story Generated Successfully!")
