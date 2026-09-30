import streamlit as st
import google.generativeai as genai
import json
import urllib.parse

st.set_page_config(page_title="ComicCraft AI", page_icon="🎨", layout="wide")

st.title("🎨 ComicCraft: AI Comic Strip Creator")
st.caption("Generates full comic stories, dialogues, and visual comic illustrations using Gemini & AI Art")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    genre = st.selectbox("Genre", ["Superhero", "Sci-Fi", "Comedy", "Fantasy", "Mystery", "Anime"])
    art_style = st.selectbox("Art Style", ["Comic Book Style", "Manga / Anime", "Vintage 90s Comic", "Watercolor Comic"])
    panels_count = st.slider("Number of Panels", min_value=3, max_value=4, value=4)

story_idea = st.text_area(
    "Enter your story premise or concept:", 
    placeholder="E.g., A police officer trying to catch a thief in a futuristic neon city"
)

if st.button("🚀 Generate Full Comic with Images"):
    clean_key = api_key.strip() if api_key else ""
    if not clean_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    elif not story_idea.strip():
        st.warning("Please enter a story idea!")
    else:
        try:
            genai.configure(api_key=clean_key)
            
            # Select working Gemini model
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
            except Exception:
                model = genai.GenerativeModel("gemini-pro")
            
            prompt = f"""
            You are a professional comic creator. Create a {panels_count}-panel comic strip based on:
            Story: {story_idea}
            Genre: {genre}
            Style: {art_style}

            Respond ONLY with a valid raw JSON object (without markdown blocks, without backticks ```json).
            Format:
            {{
              "title": "Comic Title",
              "synopsis": "One line summary",
              "panels": [
                {{
                  "panel_number": 1,
                  "image_prompt": "Detailed description of scene visual, {art_style}, highly detailed comic frame, vibrant colors, comic art",
                  "speaker": "Character name",
                  "dialogue": "Spoken sentence",
                  "sfx": "SFX sound"
                }}
              ]
            }}
            """
            
            with st.spinner("Writing story & drawing comic panels..."):
                response = model.generate_content(prompt)
                raw_text = response.text.strip()
                
                # Clean markdown formatting if returned
                if raw_text.startswith("```"):
                    raw_text = raw_text.split("```")[1]
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:]
                raw_text = raw_text.strip()
                
                data = json.loads(raw_text)
                
                st.markdown(f"## 📖 {data.get('title', 'Generated Comic')}")
                st.write(f"*{data.get('synopsis', '')}*")
                st.markdown("---")
                
                # Display panels in a 2-column comic layout
                cols = st.columns(2)
                for idx, p in enumerate(data.get("panels", [])):
                    with cols[idx % 2]:
                        st.markdown(f"### 🖼️ Panel {p.get('panel_number')}")
                        
                        # Generate real AI image dynamically via free image API
                        img_prompt = urllib.parse.quote(f"{p.get('image_prompt')}, comic book art, masterpiece")
                        image_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){img_prompt}?width=512&height=512&nologo=true"
                        
                        st.image(image_url, use_column_width=True, caption=f"Panel {p.get('panel_number')}")
                        
                        if p.get("sfx"):
                            st.warning(f"💥 **SFX:** {p.get('sfx')}")
                        if p.get("speaker") and p.get("dialogue"):
                            st.info(f"🗣️ **{p.get('speaker')}:** \"{p.get('dialogue')}\"")
                        st.markdown("---")
                        
                st.success("✅ Complete Comic Strip with Images Generated!")
                
        except Exception as e:
            st.error(f"Error: {str(e)}. Try clicking Generate again!")
