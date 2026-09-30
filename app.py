import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="ComicCraft AI", page_icon="", layout="wide")

st.title(" ComicCraft: AI Comic Story Creation")
st.caption("Generate dynamic comic strips and panel storyboards using Google Gemini")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    genre = st.selectbox("Genre", ["Superhero", "Sci-Fi", "Comedy", "Fantasy", "Mystery", "Anime"])
    panels_count = st.slider("Number of Panels", min_value=3, max_value=6, value=4)

story_idea = st.text_area("Enter your story premise or concept:", 
                          placeholder="E.g., A time-traveling detective visits ancient Rome to stop a cyber heist.")

if st.button(" Generate Comic Strip"):
    if not api_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    elif not story_idea.strip():
        st.warning("Please enter a story idea!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            You are a professional comic scriptwriter. Create a structured comic strip storyboard based on the following input:
            - Story Idea: {story_idea}
            - Genre: {genre}
            - Total Panels: {panels_count}

            Respond strictly in valid JSON format matching this schema:
            {{
              "title": "Comic Title",
              "synopsis": "Short summary",
              "characters": [
                {{"name": "Character Name", "appearance": "Costume and visual look"}}
              ],
              "panels": [
                {{
                  "panel_number": 1,
                  "scene_description": "Detailed camera angle and visual scene",
                  "dialogue": [
                    {{"speaker": "Name", "text": "Speech balloon text"}}
                  ],
                  "sfx": "Sound effect if any (e.g. BAM!, WHOOSH)"
                }}
              ]
            }}
            """
            
            with st.spinner("Writing script, dialogue, and blocking panels..."):
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
                comic_data = json.loads(response.text)
                
                st.subheader(f" {comic_data.get('title', 'Generated Comic')}")
                st.write(f"*{comic_data.get('synopsis', '')}*")
                
                st.markdown("###  Character Profiles")
                for char in comic_data.get("characters", []):
                    st.markdown(f"- **{char.get('name')}**: {char.get('appearance')}")
                    
                st.markdown("---")
                st.markdown("### ️ Comic Strip Panels")
                
                cols = st.columns(2)
                for idx, panel in enumerate(comic_data.get("panels", [])):
                    with cols[idx % 2]:
                        st.markdown(f"#### Panel {panel.get('panel_number')}")
                        st.info(f"**Visual:** {panel.get('scene_description')}")
                        if panel.get("sfx"):
                            st.warning(f"**SFX:** {panel.get('sfx')}")
                        for dia in panel.get("dialogue", []):
                            st.write(f"️ **{dia.get('speaker')}**: \"{dia.get('text')}\"")
                        st.markdown("---")
                        
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")

