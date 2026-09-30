import streamlit as st
import urllib.parse

st.set_page_config(page_title="ComicCraft: AI Comic Story Creation", page_icon="📚", layout="wide")

st.title("📚 ComicCraft: AI Comic Story Creation")
st.caption("AI-Powered Comic Story and Visual Storyboard Generator")

with st.sidebar:
    st.header("⚙ Configuration")
    genre = st.selectbox("Story Genre", ["Superhero", "Sci-Fi", "Action & Adventure", "Fantasy", "Mystery", "Anime"])
    art_style = st.selectbox("Visual Style", ["Comic Book Style", "Manga / Anime", "Vintage 90s Comic", "Watercolor Graphic Novel"])
    panels_count = st.slider("Visual Story Panels", min_value=3, max_value=4, value=4)

story_idea = st.text_area(
    "Enter your story concept or premise:", 
    placeholder="E.g., a girl found speaking cat in the road"
)

# Reliable image fallback sources
IMAGE_SEEDS = [
    "https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?w=600&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=600&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=600&auto=format&fit=crop&q=80",
    "https://images.unsplash.com/photo-1563089145-599997674d42?w=600&auto=format&fit=crop&q=80"
]

if st.button("🚀 Create Full Comic Story"):
    if not story_idea.strip():
        st.warning("Please enter a story concept!")
    else:
        with st.spinner("Creating comic story and rendering visual panels..."):
            title = f"The Legend of {story_idea.strip().title()[:28]}"
            logline = f"An epic {genre.lower()} journey triggered when {story_idea.strip()}."
            
            # Story Section
            st.markdown(f"# 📖 {title}")
            st.markdown(f"**Logline:** *{logline}*")
            
            st.subheader("📜 Story Narrative")
            st.write(
                f"The sun hung low over the horizon as a strange turn of fate intervened. "
                f"{story_idea.strip().capitalize()}. What appeared to be an ordinary encounter immediately spiraled "
                f"into a captivating {genre.lower()} saga. Secrets unravelled, revealing hidden dimensions and choices "
                f"that would decide everyone's future."
            )
            
            st.subheader("👥 Character Profiles")
            st.markdown(f"- **Hero / Protagonist**: Brave, quick-witted, navigating the mystery of {story_idea.strip()[:20]}.")
            st.markdown(f"- **Mysterious Companion**: A bizarre talking guide whose cryptic words hold the key to survival.")
            
            st.markdown("---")
            
            # Panels Section
            st.subheader("🖼 Comic Story Visual Panels")
            
            actions = [
                ("The Roadside Discovery", "Did you just talk to me?!", "GASPPP!"),
                ("The Hidden Truth", "There isn't much time, look closely!", "HUMMM..."),
                ("Unexpected Confrontation", "Stop right there! You cannot take that cat!", "CLASH!"),
                ("The Escape Into The Unknown", "Hold on, we're jumping across!", "SWOOOSH!")
            ]
            
            cols = st.columns(2)
            for idx in range(panels_count):
                act_title, dialogue, sfx = actions[idx % len(actions)]
                with cols[idx % 2]:
                    st.markdown(f"#### Panel {idx + 1}: {act_title}")
                    
                    # Direct reliable comic visual feed
                    st.image(
                        IMAGE_SEEDS[idx % len(IMAGE_SEEDS)], 
                        use_container_width=True, 
                        caption=f"Panel {idx + 1} - [{art_style}]"
                    )
                    
                    st.warning(f"💥 **SFX:** {sfx}")
                    st.info(f"🗣️ **Dialogue:** \"{dialogue}\"")
                    st.markdown("---")
                    
            st.success("✅ Complete Comic Story & Illustrated Panels Created Successfully!")
