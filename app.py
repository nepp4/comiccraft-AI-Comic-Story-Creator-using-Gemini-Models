import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="ComicCraft AI", page_icon="🎨", layout="wide")

st.title("🎨 ComicCraft: AI Comic Story Creation")
st.caption("Generate dynamic comic strips and panel storyboards using Google Gemini")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    genre = st.selectbox("Genre", ["Superhero", "Sci-Fi", "Comedy", "Fantasy", "Mystery", "Anime"])
    panels_count = st.slider("Number of Panels", min_value=3, max_value=6, value=4)

story_idea = st.text_area(
    "Enter your story premise or concept:", 
    placeholder="E.g., a police officer trying to catch a thief"
)

if st.button("Generate Comic Strip"):
    clean_key = api_key.strip() if api_key else ""
    if not clean_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    elif not story_idea.strip():
        st.warning("Please enter a story idea!")
    else:
        try:
            genai.configure(api_key=clean_key)
            
            # Use recommended Gemini 3.8 Flash model
            try:
                model = genai.GenerativeModel("gemini-3.8-flash")
            except Exception:
                # Fallback to any active supported model
                active_models = [
                    m.name for m in genai.list_models() 
                    if "generateContent" in m.supported_generation_methods
                ]
                model = genai.GenerativeModel(active_models[0])
            
            prompt = f"""
            You are a professional comic scriptwriter. Create a structured comic strip storyboard based on:
            - Story: {story_idea}
            - Genre: {genre}
            - Total Panels: {panels_count}

            Format your response clearly as:
            # Comic Title: [Title]
            **Synopsis:** [Story summary]
            
            ## Characters
            - [Name]: [Visual look and description]
            
            ## Comic Panels
            (Provide details for each of the {panels_count} panels with Scene, Dialogue, and SFX)
            """
            
            with st.spinner("Writing script and generating comic panels..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("✅ Comic Strip Created Successfully!")
                
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
