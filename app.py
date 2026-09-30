import os
import json

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Gemini API configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please add it to your .env file."
    )

client = genai.Client(api_key=API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_comic():
    try:
        data = request.get_json()

        topic = data.get("topic", "").strip()
        genre = data.get("genre", "Adventure")
        panels = int(data.get("panels", 6))
        style = data.get("style", "Colorful comic")

        if not topic:
            return jsonify({
                "error": "Please enter a story topic."
            }), 400

        if panels not in [4, 6, 8]:
            return jsonify({
                "error": "Panels must be 4, 6, or 8."
            }), 400

        prompt = f"""
You are ComicCraft, an AI comic story creator.

Create an original comic story using these details:

Topic: {topic}
Genre: {genre}
Number of Panels: {panels}
Visual Style: {style}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "title": "Comic title",
    "summary": "Short story summary",
    "panels": [
        {{
            "panel": 1,
            "scene": "Description of the scene",
            "dialogue": "Short dialogue or narration",
            "image_prompt": "Detailed prompt for creating the panel image"
        }}
    ]
}}

Important rules:

1. Create exactly {panels} panels.
2. Keep the story simple and easy to understand.
3. Keep the same main characters throughout the story.
4. Every panel must continue the story.
5. Dialogue should be short.
6. Give a clear beginning, middle and ending.
7. Do not use copyrighted characters.
8. Make the image_prompt suitable for an AI image generator.
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.8,
                max_output_tokens=5000
            )
        )

        result = json.loads(response.text)

        return jsonify(result)

    except json.JSONDecodeError:
        return jsonify({
            "error": "Gemini returned an invalid response. Please try again."
        }), 500

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
