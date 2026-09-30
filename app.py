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
    placeholder="E.g., A police officer trying to catch a thief"
)

if st.button("Generate Comic Strip"):
    if not api_key:
        st.error("Please provide your Google Gemini API Key in the sidebar.")
    elif not story_idea.strip():
        st.warning("Please enter a story idea!")
    else:
        try:
            genai.configure(api_key=api_key.strip())
            
            # Find an available model to avoid 404 version errors
            available_models = [
                m.name for m in genai.list_models() 
                if "generateContent" in m.supported_generation_methods
            ]
            
            chosen_model = None
            for candidate in ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]:
                if candidate in available_models:
                    chosen_model = candidate
                    break
            
            if not chosen_model and available_models:
                chosen_model = available_models[0]
                
            model = genai.GenerativeModel(chosen_model)
            
            prompt = f"""
            You are a professional comic scriptwriter. Create a structured comic strip storyboard based on:
            - Story Idea: {story_idea}
            - Genre: {genre}
            - Total Panels: {panels_count}

            Format your response clearly as follows:
            # Comic Title: [Title]
            **Synopsis:** [Brief summary]

            ## Characters
            - [Character Name]: [Appearance and visual traits]

            ## Comic Panels
            ### Panel 1
            - **Visual Scene:** [Camera angle and action]
            - **Dialogue:** [Speaker: Text]
            - **SFX:** [Sound effect]

            (Continue this structure for all {panels_count} panels)
            """
            
            with st.spinner("Writing script, dialogue, and blocking panels..."):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.success("✅ Comic Strip Storyboard Generated Successfully!")
                
        except Exception as e:
            st.error(f"Error occurred: {str(e)}")
