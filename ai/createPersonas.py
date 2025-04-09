from google import genai
from google.genai import types
from dotenv import load_dotenv
from mongoUtils import getAllUsers
import json
import os

load_dotenv()  # Load variables from .env
api_key = os.getenv("API_KEY")

client = genai.Client(api_key=api_key)

def generatePersona():
    existingPersonas = getAllUsers()
    formatted_personas = json.dumps(existingPersonas, indent=4)
    persona_prompt = """Create a brand new fictional, realistic persona with the following attributes. Make sure the values are internally consistent and formatted cleanly.  Return the response as a JSON object with double quotes, following this exact structure with no extra text outside the json code:
    {{
    "fullname": "",
    "gender": "",
    "email": "",
    "mbti": "",
    "age": ,
    "ethnicity": "",
    "traits": [],
    "communication style": "",
    "motivations": [],
    "interests": [],
    "education": "",
    "online behaviour": "",
    "unique attributes": ""
    }}
    The persona should reflect a believable character. You can be creative but stay grounded in reality. Info should be changed up every new persona givent these are the already existing personas:
    {existingPersonas}
    """.format(existingPersonas=formatted_personas)

    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        response_mime_type="text/plain",
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=persona_prompt,
        config=generate_content_config,
    )
    return(response.text)