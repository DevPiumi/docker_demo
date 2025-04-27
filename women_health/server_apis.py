import requests
import logging


SERVER_URL = "https://test-medtechai.pantheonsite.io/"
USERNAME = "jinyao"
PASSWORD = "jinyao-password"
OPENAI_API_KEY = "sk-svcacct-eduGediAsqkaHqfWZQu_yETmPoWNxuSC6D01X5H9WL0aw5KdgOjimK_kF3gJDT3BlbkFJIsoXFnFRU3M4fYKtINT0V_HxKqhXAIdx0u_7f389Gogw6fEYxvHeR0ORMP5AA"



def fetch_data_with_url(api_url):
    try:
        response = requests.get(api_url, auth=(USERNAME, PASSWORD))
        
        # Check for 404 explicitly
        if response.status_code == 404:
            print("Resource not found at this URL.")
            return "None"
           

        # If not 404, raise any other potential errors
        response.raise_for_status()

        data = response.json()

        # Ensure data is valid (list or dict)
        if not isinstance(data, (dict, list)):
            return "None"

        # Check if data is empty
        if not data:
            return "None"

        # Check if 'user_data' key exists and is non-empty
        if 'user_data' in data and not data['user_data']:
            return "None"

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return "None"

