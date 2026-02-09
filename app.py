import base64
from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_data = None
    prompt_text = ""

    if request.method == "POST":
        prompt_text = request.form["prompt"]

        try:
            response = openai.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "developer", "content": "Interpret the dreams described in the prompts. Analyze the dreams with respect to Jungian psychology, focusing on the dream's symbolic elements and the user's emotional state. Attempt to understand the user's unconscious mind and what they can do to aid their personal growth. Avoid directly stating the terms 'Jungian' or 'Jungian psychology'. Limit responses to 1-2 complete sentences (max 35-50 words). Never cut off a sentence. If you approach the word limit, end the sentence early rather than cutting it off."},
                    {"role": "user", "content": prompt_text}
                ],
                temperature=1.4,
                max_output_tokens=100
            )
            result = response.output_text
        except Exception as e:
            result = f"Error generating text: {str(e)}"

        try:
            image_response = openai.images.generate(
                model="gpt-image-1",
                prompt = f"A dreamlike, mystical, ethereal illustration of a dream described as follows: {prompt_text}. Interpret this dream as a stepping stone on the user's journey to self growth.",
                size="1024x1024" 
            )

            # image_response.data[0].b64_json contains the base64 string
            b64_image = image_response.data[0].b64_json
            image_data = f"data:image/png;base64,{b64_image}"
        except Exception as e:
            image_data = None
            print(f"Error generating image: {e}")

    return render_template("index.html", result=result, prompt=prompt_text, image_data=image_data)

if __name__ == "__main__":
    app.run(debug=True)  # Run locally for testing