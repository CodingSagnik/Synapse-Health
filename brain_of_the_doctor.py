#Step 1: Setup GROQ API key
import os
from load_env import load_environment_variables

# Load environment variables
GROQ_API_KEY = load_environment_variables()

#Step 2: Convert image to required format
import base64



#image_path = "acne.jpg"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#Step 3: Setup Multimodal LLM 
from groq import Groq


query = "Is there something wrong with my face?"
model = "meta-llama/llama-4-scout-17b-16e-instruct"


def analyze_image_with_query(query, encoded_image, model):
    client = Groq(api_key=GROQ_API_KEY)
    

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }]

    chat_completion = client.chat.completions.create(
        messages = messages,
        model = model
    )

    return chat_completion.choices[0].message.content