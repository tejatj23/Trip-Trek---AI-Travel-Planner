import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables (like the API key) from the .env file
load_dotenv()

# --- Configuration ---
MODEL = "gemini-2.5-flash" 

def get_itinerary_prompt(destination, days, budget, interests):
    """
    Constructs the detailed prompt for the Gemini model.
    """
    return f"""
    You are an expert, friendly AI travel planner named **TripTrek AI**. Your task is to create a detailed, personalized travel itinerary based on the user's input.

    **Travel Details:**
    - Destination: {destination}
    - Duration: {days} days
    - Budget: {budget} (Low, Medium, High)
    - Interests/Travel Style: {interests}

    **Instructions for Output:**
    1.  Generate a **{days}-day itinerary** for {destination}.
    2.  Use **clear Markdown formatting** with headings and lists for easy reading.
    3.  Begin with a brief, exciting introduction to the trip.
    4.  For each day, provide:
        * A **Day Header** (e.g., "**Day 1: Arrive and Explore the Old Town**").
        * **Morning Activity**
        * **Lunch Suggestion** (and cuisine type)
        * **Afternoon Activity**
        * **Evening Activity/Dinner Suggestion**
    5.  Include a final section titled "**Trip Summary & Budget Estimate ({budget})**" with a brief overview of the expected costs for accommodation, transport, and activities, matching the user's budget level.
    6.  Ensure all suggestions align with the user's specified **Interests**.

    Produce ONLY the itinerary and summary, formatted strictly in Markdown.
    """

def generate_itinerary(destination, days, budget, interests):
    """
    Handles the API call to the Gemini model.
    """
    try:
        # Check and get API key from environment
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            return "An unexpected API error occurred: API key is missing. Please ensure GEMINI_API_KEY is set in your .env file."

        # Initialize the client with the API key
        client = genai.Client(api_key=gemini_api_key)
        
        prompt = get_itinerary_prompt(destination, days, budget, interests)
        
        # Call the model
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7 
            )
        )
        return response.text

    except Exception as e:
        # Return a user-friendly error message if the API call fails
        return f"An unexpected API error occurred: {e}"