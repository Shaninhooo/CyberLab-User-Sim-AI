from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import re

load_dotenv()  # Load variables from .env
api_key = os.getenv("API_KEY")


client = genai.Client(api_key=api_key)
df = pd.read_csv('ai/personas.csv')

# Function to create a new persona using the Google GEMINI LLM and write it to the CSV file
def createPersona():
    persona_prompt = "Create a brief persona for him. A persona should include the following attributes: Full Name, Gender, Age, Location, Language, Occupation, Interests, Education, Online Behavior, IT Proficiency, Unique Attributes, and a Summary.  Please be creative in creating the characteristics."

    # Generates persona with response
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=" Example: Maximilian is a 32-year-old accountant based in Berlin, Germany. His native language is English. create a different persona with different details every time using this example,Create one brief persona for him. A persona should include the following attributes: Full Name, Gender, Age, Location, Language, Occupation, Interests, Education, Online Behavior, IT Proficiency, Unique Attributes, and a Summary. Please be creative in creating the characteristics. output in a format easy to read in csv also break line for end of each attribute "
    )

    # Filters response into csv data
    new_row = {}
    for line in response.text.split('\n'):
        for header in df.columns:
            if header in line:
                info = line.split(header+',')[1]
                cleanedInfo = info.replace(',', '')  # Replace commas with empty string
                new_row[header] = cleanedInfo

    df.loc[len(df)] = new_row  # Append row
    df.to_csv('personas.csv', index=False)  # Overwrite

    print("Row added to the original CSV!")


def usePersona(creationPrompt):
    for _, row in df.iterrows():
        persona = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        prompt = f"You are interacting as the following persona:\n{persona}\n\nPlease respond in character."
        
        # Send this to Gemini
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}\n {creationPrompt}"
    )
        return(response.text.encode('utf-8', errors='ignore').decode('utf-8'))

def setPersonaActivities():
    prompt = "generate a list of daily online activities, browsing habits, and social media interactions. Format the output as a CSV-friendly list."
    usePersona(prompt)

def createEventInfo():
    prompt = "Generate a event title, event location and event description for a event the persona is scheduling."
    text = usePersona(prompt)

    title_match = re.search(r"\*\*Event Title:\*\*\s*(.*)", text)
    location_match = re.search(r"\*\*Event Location:\*\*\s*(.*)", text)
    description_match = re.search(r"\*\*Event Description:\*\*\n+(.*)", text, re.DOTALL)

    event_title = title_match.group(1).strip() if title_match else "N/A"
    event_location = location_match.group(1).strip() if location_match else "N/A"
    event_description = description_match.group(1).strip() if description_match else "N/A"


    eventInfos = [event_title, event_location, event_description]

    return eventInfos
