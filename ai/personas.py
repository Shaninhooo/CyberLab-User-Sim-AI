from google import genai
from dotenv import load_dotenv
import os
import pandas as pd
import re

load_dotenv()  # Load variables from .env
api_key = os.getenv("API_KEY")


client = genai.Client(api_key=api_key)

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


# Generates Event Infos Using Gemini LLM
def createEventInfo():
    prompt = "Generate a event title, event start time in 09:00 24hr format, start date in year-month-day format just date no extra text, event end time in 09:00 24hr format, end date in year-month-day format date no extra text, event location and event description for a event the persona is scheduling. Make the dates in April 2025"
    text = usePersona(prompt)

    title_match = re.search(r"\*\*Event Title:\*\*\s*(.*)", text)
    start_time_match = re.search(r"\*\*Event Start Time:\*\*\s*(.*)", text)
    start_date_match = re.search(r"\*\*Start Date:\*\*\s*(.*)", text)
    end_time_match = re.search(r"\*\*Event End Time:\*\*\s*(.*)", text)
    end_date_match = re.search(r"\*\*End Date:\*\*\s*(.*)", text)
    location_match = re.search(r"\*\*Event Location:\*\*\s*(.*)", text)
    description_match = re.search(r"\*\*Event Description:\*\*\n+(.*)", text, re.DOTALL)

    event_title = title_match.group(1).strip() if title_match else "N/A"
    start_time = start_time_match.group(1).strip() if start_time_match else "N/A"
    start_date = start_date_match.group(1).strip() if start_date_match else "N/A"
    end_time = end_time_match.group(1).strip() if end_time_match else "N/A"
    end_date = end_date_match.group(1).strip() if end_date_match else "N/A"
    event_location = location_match.group(1).strip() if location_match else "N/A"
    event_description = description_match.group(1).strip() if description_match else "N/A"

    eventInfos = [event_title, start_date, start_time, end_date, end_time, event_location, event_description]

    return eventInfos


# Generates Chat Infos Using Gemini LLM
def createChatInfo():
    prompt = "Generate a chat group title starting in **Group Chat Title:** format and chat description starting in **Group Chat Description:** format for a group chat the persona is creating with no special characters e.g. emojis."
    text = usePersona(prompt)

    title_match = re.search(r"\*\*Group Chat Title:\*\*\s*(.*)", text)
    description_match = re.search(r"\*\*Group Chat Description:\*\*\s*(.*)", text, re.DOTALL)

    chat_title = title_match.group(1).strip() if title_match else "N/A"
    chat_description = description_match.group(1).strip() if description_match else "N/A"

    eventInfos = [chat_title, chat_description]

    return eventInfos


