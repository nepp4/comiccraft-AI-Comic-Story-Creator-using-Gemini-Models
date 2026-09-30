import streamlit as st
import json
import urllib.parse
import urllib.request
import time

st.set_page_config(page_title="ComicCraft: AI Comic Story Creation", page_icon="📚", layout="wide")

st.title("📚 ComicCraft: AI Comic Story Creation")
st.caption("AI-Powered Comic Story and Visual Storyboard Generator using Neural AI Models")

with st.sidebar:
    st.header("⚙️ Configuration")
    genre = st.selectbox("Story Genre", ["Superhero", "Sci-Fi", "Action & Adventure", "Fantasy", "Mystery", "Anime"])
    art_style = st.selectbox("Visual Style", ["Comic Book Style", "Manga / Anime", "Vintage 90s Comic", "Watercolor Graphic Novel"])
    panels_count = st.slider("Visual Story Panels", min_value=3, max_value=4, value=4)

story_idea = st.text_area(
    "Enter your story concept or premise:", 
    placeholder="E.g., A police officer trying to catch a cyber thief in a neon city"
)

def query_ai_story(system_prompt, user_prompt):
    # Free, unmetered AI inference endpoint without API keys
    full_prompt = f"{system_prompt}\nUser Request: {user_prompt}"
    encoded = urllib.parse.quote(full_prompt)
    url = f"https://text.pollinations.ai/{encoded}?model=openai-large&json=true"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        result = response.read().decode("utf-8")
        return result

if st.button("🚀 Create Full Comic Story"):
    if not story_idea.strip():
        st.warning("Please enter a story concept!")
    else:
        try:
            system_prompt = f"""
            You are a creative author and comic writer. Create a complete comic story and {panels_count}-panel visual storyboard based on the user's premise.
            Genre: {genre}
            Art Style: {art_style}

            Respond ONLY with a valid raw JSON object without markdown fences, without backticks ```json.
            JSON Format:
            {{
              "story_title": "Story Title",
              "logline": "One sentence summary hook",
              "full_story": "A rich 2-paragraph comic narrative story.",
              "characters": [
                {{"name": "Name", "role": "Role", "traits": "Visual costume and appearance"}}
              ],
              "panels": [
                {{
                  "panel_number": 1,
                  "scene_prompt": "Scene visual prompt for {art_style}, detailed frame",
                  "speaker": "Speaker Name",
                  "dialogue": "Line spoken",
                  "sfx": "SFX sound"
                }}
              ]
            }}
            """
            
            with st.spinner("AI is writing the story narrative and illustrating comic panels..."):
                raw_text = query_ai_story(system_prompt, story_idea).strip()
                
                # Clean up any potential markdown wraps
                if "```" in raw_text:
                    parts = raw_text.split("```")
                    raw_text = parts[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                raw_text = raw_text.strip()
                
                data = json.loads(raw_text)
                
                # Story Section
                st.markdown(f"# 📖 {data.get('story_title', 'Comic Story')}")
                st.markdown(f"**Logline:** *{data.get('logline', '')}*")
                
                st.subheader("📜 Story Narrative")
                st.write(data.get("full_story", ""))
                
                st.subheader("👥 Character Profiles")
                for char in data.get("characters", []):
                    st.markdown(f"- **{char.get('name')}** ({char.get('role')}): {char.get('traits')}")
                
                st.markdown("---")
                
                # Panels Section
                st.subheader("🖼️ Comic Story Visual Panels")
                cols = st.columns(2)
                for idx, p in enumerate(data.get("panels", [])):
                    with cols[idx % 2]:
                        st.markdown(f"#### Panel {p.get('panel_number')}")
                        
                        img_prompt = urllib.parse.quote(f"{p.get('scene_prompt')}, {art_style}, comic art frame, masterpiece, highly detailed")
                        image_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){img_prompt}?width=512&height=512&nologo=true"
                        
                        st.image(image_url, use_container_width=True, caption=f"Panel {p.get('panel_number')}")
                        
                        if p.get("sfx"):
                            st.warning(f"💥 **SFX:** {p.get('sfx')}")
                        if p.get("speaker") and p.get("dialogue"):
                            st.info(f"🗣️ **{p.get('speaker')}:** \"{p.get('dialogue')}\"")
                        st.markdown("---")
                        
                st.success("✅ Comic Story & Illustrated Panels Created Successfully!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}. Please click Create again!")
