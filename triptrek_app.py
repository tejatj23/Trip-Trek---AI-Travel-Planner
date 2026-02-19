import streamlit as st
import os

# Import the core AI function from the new module
from utils.gemini_client import generate_itinerary

# --- Application Setup ---

# Function to load custom CSS
def load_css(file_name):
    # This reads the CSS file and injects it into the app
    try:
        with open(file_name, encoding='utf-8') as f:
            css = f.read()
            # Inject the custom styles with proper Streamlit overrides
            st.markdown(f'''
                <style>
                    /* Custom font imports */
                    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&family=Playfair+Display:wght@600;800&display=swap');
                    
                    /* Override Streamlit's default styles */
                    .stApp {{
                        background: linear-gradient(135deg, PeachPuff 0%, PaleVioletRed 100%);
                    }}
                    
                    /* Force Streamlit to use our custom styles */
                    .st-emotion-cache-1cypcdb {{
                        background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.02));
                        backdrop-filter: blur(6px) saturate(120%);
                    }}
                    
                    /* Apply our custom CSS */
                    {css}
                </style>
            ''', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Could not find 'styles.css'. Running with default styles.")

st.set_page_config(
    page_title="TripTrek: AI Travel Planner",
    page_icon="✈️", # Updated icon for the tab
    layout="wide"
)

# Apply custom styles
load_css("styles.css")

# Updated Title with Emojis
st.title("✈️ TripTrek: AI-Powered Travel Planner 🗺️")
st.markdown("<p style='color: #495057; font-weight: 600;'>A Smart Travel Planner.</p>", unsafe_allow_html=True)
st.markdown("---")

# 1. Sidebar for User Inputs
with st.sidebar:
    # Updated Sidebar Header with Emojis
    st.header("Plan Your Adventure! 🎒✨")
    
    destination = st.text_input(
        "Destination City/Country:", 
        placeholder="e.g., Tokyo, Japan"
    )
    
    days = st.number_input(
        "Trip Duration (in days):", 
        min_value=1, 
        max_value=30, 
        value=5
    )
    
    budget = st.select_slider(
        "Budget Level:",
        options=["Low (Backpacking)", "Medium (Comfort)", "High (Luxury)"],
        value="Medium (Comfort)"
    )
    
    interests = st.text_area(
        "Travel Interests/Style:",
        value="Culture, local food, historical sites, some nightlife."
    )
    
    # Button to trigger the itinerary generation
    if st.button("Generate Trip Itinerary", key="generate_btn", type="primary"):
        if destination:
            st.session_state['inputs'] = {
                'destination': destination,
                'days': days,
                'budget': budget,
                'interests': interests
            }
            st.session_state['run_generation'] = True
        else:
            st.session_state['run_generation'] = False
            st.warning("Please enter a destination to start planning.")
    
# 2. Main Content Area for Output
if 'run_generation' in st.session_state and st.session_state.get('run_generation'):
    
    inputs = st.session_state['inputs']
    
    st.subheader(f"Trip Plan for: {inputs['destination']} 🌟")
    
    with st.spinner(f"Crafting your personalized {inputs['days']}-day itinerary for {inputs['destination']}..."):
        
        # Call the external function in utils/gemini_client.py
        itinerary = generate_itinerary(
            inputs['destination'], 
            inputs['days'], 
            inputs['budget'], 
            inputs['interests']
        )
    
    st.markdown(itinerary)
    
    if not itinerary.startswith("An unexpected API error occurred:"):
        st.success("Your TripTrek itinerary is ready! Happy travels! 🎉")
        
    st.session_state['run_generation'] = False

else:
    st.info("Enter your trip details in the sidebar and click **'Generate Trip Itinerary'** to receive your custom travel plan. Get ready for an amazing journey! 🌍")