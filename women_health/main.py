import json
import logging
import time
import random
import os
import requests


from fastapi import FastAPI, Request
from . import server_apis
 # Your helper module for API calls

app = FastAPI()

from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.sequential import SequentialChain



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



email = "ziafigover@gmail.com"
        
api_url = f'{server_apis.SERVER_URL}/mobile-api-100-recommendation-input/{email}'  
user_data = server_apis.fetch_data_with_url(api_url)

api_url_context = f'{server_apis.SERVER_URL}/mobile-api-100-recommendation-input-context/{email}'
context_user_data = server_apis.fetch_data_with_url(api_url_context)


API_URL_Titles = f'{server_apis.SERVER_URL}/slack-api-recommendations-titles/{email}'
prior_habits_impact_response = server_apis.fetch_data_with_url(API_URL_Titles)
prior_habits_impact = prior_habits_impact_response if isinstance(prior_habits_impact_response, str) else json.dumps(prior_habits_impact_response)

API_URL_Change_Titles = f'{server_apis.SERVER_URL}/slack-api-recommendations-titles-change/{email}'
excluded_habits_response = server_apis.fetch_data_with_url(API_URL_Change_Titles)
excluded_habits = excluded_habits_response if isinstance(excluded_habits_response, str) else json.dumps(excluded_habits_response)

API_URL_Preferences = f'{server_apis.SERVER_URL}/slack-api-recommendations-titles-preferences/{email}'
preferences_response = server_apis.fetch_data_with_url(API_URL_Preferences)
preferences = preferences_response if isinstance(preferences_response, str) else json.dumps(preferences_response)

API_URL_Women = f'{server_apis.SERVER_URL}/mobile-api-100-recommendation-input-women/{email}'
women_response = server_apis.fetch_data_with_url(API_URL_Women)
women_data = women_response if isinstance(women_response, str) else json.dumps(women_response)





#women_data
#user_data
#context_user_data





cycle_prompt = PromptTemplate(
   input_variables=["cycle_context"],
   template="""
You are a health assistant predicting a woman's next menstrual period and cycle phase.


Cycle data:
{cycle_context}


Possible Phases:
- Last period date
- Average cycle length
- Next period start date
- Current phase (e.g., follicular, ovulation, luteal, menstruation)


 {{
   "Period_cycle": "Return only the phase name: Menstrual, Follicular, Ovulation, or Luteal ? output prediction.",
   "Explanition": "What is the prdeicted cycle phase and what sysmtoms could expect good or bad for this phase?",
 }}



"""
)





rec_prompt = PromptTemplate(
   input_variables=["cycle_phase", "user_profile"],
   template="""
You are a wellness and work-life assistant for a woman working in tech.
Here is her recent lifestyle and wellness data:
{user_profile}


Based on this, return a JSON array with 3 structured daily suggestions for the {cycle_phase} phase. Each suggestion should include:
- "title": A short title
- "why": Explanation why it's important with more details and emojies
- "how": How to implement it with more details and emojies
- "try": A practical tip or action with more details and emojies


Only return a valid JSON array like this:


[
 {{
   "title": "Breifly explain the recommendation title",
   "why": "Breifly explain the recommendation why it is important and provide data as references",
   "how": "Breifly explain the recommendation how to implement it",
   "try": "Breifly explain the approach time implementing the recommendation"
 }},
 {{
   "title": "Breifly explain the recommendation title",
   "why": "Breifly explain the recommendation why it is important and provide data as references",
   "how": "Breifly explain the recommendation how to implement it",
   "try": "Breifly explain the approach time implementing the recommendation"
 }},
 {{
  "title": "Breifly explain the recommendation title",
   "why": "Breifly explain the recommendation why it is important and provide data as references",
   "how": "Breifly explain the recommendation how to implement it",
   "try": "Breifly explain the approach time implementing the recommendation"
 }}
]
"""
)





'''
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import json


# Load menstrual data
cycle_context = women_data


# Load user data
user_profile = user_data
print(user_profile)


# Chain 1: Predict cycle phase
llm = ChatOpenAI(temperature=0.5, openai_api_key=server_apis.OPENAI_API_KEY)
cycle_chain = LLMChain(prompt=cycle_prompt, llm=llm)
cycle_result = cycle_chain.run(cycle_context=cycle_context)
print(cycle_result) 


# Extract phase name
import re
phase_match = re.search(r'(menstrual|follicular|ovulation|luteal)', cycle_result.lower())
cycle_phase = phase_match.group(1).capitalize() if phase_match else "Unknown"


# Chain 2: Personalized structured recommendations
rec_chain = LLMChain(prompt=rec_prompt, llm=llm)
# Parse cycle_result into a dictionary
try:
    cycle_result_dict = json.loads(cycle_result)
except json.JSONDecodeError:
    logger.error("Failed to parse cycle_result as JSON.")
    cycle_result_dict = {}

# Use the parsed dictionary to access 'Period_cycle'
recs_raw = rec_chain.run(cycle_phase=cycle_result_dict.get('Period_cycle', 'Unknown'), user_profile=user_data)



# Try to parse recommendations into JSON array
try:
   recs_json = json.loads(recs_raw)
except json.JSONDecodeError:
   logger.warning("Could not parse recommendations as JSON. Returning raw string.")
   recs_json = recs_raw


# Final structured output
output = {
   "predicted_cycle_phase": cycle_result_dict.get('Period_cycle', 'Unknown'),
   "raw_phase_prediction": cycle_result_dict.get('Explanation', 'Unknown'),
   "personalized_recommendations": recs_json
}




# Print structured JSON output
print("\n=== JSON Output ===")
print(json.dumps(output, indent=4, ensure_ascii=False))


#print("=== Prediction & Phase ===")
#print(cycle_result)
#print("\n=== Personalized Recommendations ===")
#print(recs)
'''





@app.post("/analyze")
async def analyze(request: Request):
    body = await request.json()
    email = body.get("email")

    if not email:
        return {"error": "Email is required."}

    try:
        # Fetch data
        logger.info(f"Fetching data for {email}")
        user_raw = server_apis.fetch_data_with_url(f"{server_apis.SERVER_URL}/mobile-api-100-recommendation-input/{email}")
        cycle_data = server_apis.fetch_data_with_url(f"{server_apis.SERVER_URL}/mobile-api-100-recommendation-input-women/{email}")

        # Format user profile
        user_entries = user_raw.get("user_data", [])
        user_profile = "\n".join([
            f"{entry['Question']} — Answer: {entry['Answer']} (Target: {entry['Target']})"
            for entry in user_entries
        ])

        # LLM setup
        llm = ChatOpenAI(temperature=0.5, openai_api_key=server_apis.OPENAI_API_KEY)

        # Chain 1: Predict phase
        cycle_chain = LLMChain(prompt=cycle_prompt, llm=llm)
        cycle_result = cycle_chain.run(cycle_context=cycle_data)

        try:
            cycle_result_dict = json.loads(cycle_result)
        except json.JSONDecodeError:
            cycle_result_dict = {}

        phase = cycle_result_dict.get("Period_cycle", "Unknown")

        # Chain 2: Recommendations
        rec_chain = LLMChain(prompt=rec_prompt, llm=llm)
        recs_raw = rec_chain.run(cycle_phase=phase, user_profile=user_profile)

        try:
            recs_json = json.loads(recs_raw)
        except json.JSONDecodeError:
            recs_json = recs_raw

        return {
            "predicted_cycle_phase": phase,
            "raw_phase_prediction": cycle_result_dict.get("Explanation", "No explanation provided"),
            "personalized_recommendations": recs_json
        }

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}

