from google import genai
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()  # Load variables from .env
api_key = os.getenv("API_KEY")


client = genai.Client(api_key=api_key)

persona_prompt = "Create a brief persona for him. A persona should include the following attributes: Full Name, Gender, Age, Location, Language, Occupation, Interests, Education, Online Behavior, IT Proficiency, Unique Attributes, and a Summary.  Please be creative in creating the characteristics."

# Generates persona with response
response = client.models.generate_content(
    model="gemini-2.0-flash", contents=" Example: Maximilian is a 32-year-old accountant based in Berlin, Germany. His native language is English. create a different persona with different details every time using this example,Create one brief persona for him. A persona should include the following attributes: Full Name, Gender, Age, Location, Language, Occupation, Interests, Education, Online Behavior, IT Proficiency, Unique Attributes, and a Summary. Please be creative in creating the characteristics. output in a format easy to read in csv also break line for end of each attribute "
)

# Read, modify, and overwrite the original persona csv file
df = pd.read_csv('dataset/personas.csv')

# Filters response into csv data
new_row = {}
for line in response.text.split('\n'):
    for header in df.columns:
        if header in line:
            info = line.split(header+',')[1]
            cleanedInfo = info.replace(',', '')  # Replace commas with empty string
            new_row[header] = cleanedInfo

df.loc[len(df)] = new_row  # Append row
df.to_csv('dataset/personas.csv', index=False)  # Overwrite

print("Row added to the original CSV!")
