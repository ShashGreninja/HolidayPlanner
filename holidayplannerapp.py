import streamlit as st
from mira_sdk import MiraClient, Flow
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_card import card
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_key():
    """Get API key from environment variable or Streamlit secrets"""
    # Try getting API key from environment variable
    api_key = os.getenv('API_KEY')
    
    # If not in env, try getting from Streamlit secrets
    if not api_key and 'API_KEY' in st.secrets:
        api_key = st.secrets['API_KEY']
    
    return api_key

# Get API key
api_key = get_api_key()

if not api_key:
    st.error("""
        API Key not found! Please set up your API key using one of these methods:
        1. Create a .env file with your API_KEY
        2. Set it in Streamlit secrets if deploying to Streamlit Cloud
        
        See the .env.template file for setup instructions.
    """)
    st.stop()

# Initialize MiraClient with API key
client = MiraClient(config={"API_KEY": api_key})

# Set page configuration
st.set_page_config(
    page_title="Holiday Planner ✈️",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add background image and text styling
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/2387793/pexels-photo-2387793.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
             background-attachment: fixed;
             background-size: cover;
         }}
         /* Make header/navbar transparent */
         header[data-testid="stHeader"] {{
             background-color: rgba(255, 255, 255, 0.05) !important;
             backdrop-filter: blur(0px);
         }}
         /* Style header buttons and menu items */
         .stDeployButton, button[kind="header"] {{
             background-color: rgba(255, 255, 255, 0.2) !important;
         }}
         /* Enhanced text styling without color override */
         .stMarkdown, .stExpander, .stSelectbox, .stSlider, .stSpinner {{
             font-size: 1.1rem !important;
         }}
         /* Make spinner text white */
         .stSpinner > div > div > div > div {{
             color: white !important;
         }}
         /* Headers and titles */
         h1, h2, h3, .stHeader {{
             font-size: 2.5rem !important;
             font-weight: 700 !important;
         }}
         /* Subheaders and colored headers */
         h4, h5, h6, .stSubheader {{
             font-size: 1.8rem !important;
             font-weight: 600 !important;
         }}
         /* Regular text and paragraphs */
         p, li, label {{
             font-size: 1.2rem !important;
             font-weight: 500 !important;
         }}
         /* Expander headers */
         .streamlit-expanderHeader {{
             font-size: 1.3rem !important;
             font-weight: 600 !important;
         }}
         /* Button text */
         .stButton button {{
             font-size: 1.2rem !important;
             font-weight: 600 !important;
         }}
         /* Input fields */
         .stTextInput input {{
             font-size: 1.1rem !important;
         }}
         /* Selectbox and slider labels */
         .stSelectbox label, .stSlider label {{
             font-size: 1.2rem !important;
             font-weight: 500 !important;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# Create main container with transparency
main_container = st.container()
with main_container:
    colored_header(
        label="✈️ Holiday Planner 🌴",
        description="Your personal travel planning assistant",
        color_name="red-70"
    )
    
    add_vertical_space(2)
    
    # Create a card for the description
    with st.expander("How it works", expanded=True):
        st.markdown("""
        Planning a vacation can be overwhelming - researching multiple destinations, comparing places to visit, 
        finding the best local cuisines, and figuring out the perfect time to visit. Let us simplify this for you! 
        
        Just follow these simple steps:
        1. Select the number of days for your vacation using the slider below
        2. Enter up to 5 destinations anywhere in the world you'd like to compare
        3. Click 'Plan My Holiday' and wait for about 30 seconds
        4. Get a detailed side-by-side comparison of your chosen destinations!
        """)

    add_vertical_space(1)

    # Create two columns for inputs
    col1, col2 = st.columns([2, 1])
    with col1:
        num_destinations = st.selectbox("🌍 Number of destinations", [1, 2, 3, 4, 5])
    with col2:
        daysofvisit = st.slider("📅 Duration (days)", 1, 30, 3)

    # Create containers for destinations
    destinations = []
    cols = st.columns(num_destinations)
    for i in range(num_destinations):
        with cols[i]:
            with st.expander(f"🎯 Destination {i + 1}", expanded=True):
                destination = st.text_input("Enter destination", key=f"dest{i + 1}")
                destinations.append(destination)

    add_vertical_space(1)

    # Center the button using columns
    _, col2, _ = st.columns([2, 1, 2])
    with col2:
        plan_button = st.button("🎉 Plan My Holiday!", use_container_width=True)

# ... rest of your existing code for get_image_url and the planning logic ...

def get_image_url(destination):
    # Placeholder approach; replace with your real API
    # e.g., Unsplash search URL, or any image hosting
    # For demo, returning an example static image
    return "https://source.unsplash.com/random/?"+destination

if plan_button:
    with st.spinner('✨ Creating your perfect travel plan...'):
        try:
            flow = Flow(source="holiday-planner.yaml")
            responses = []
            for i in range(num_destinations):
                if destinations[i]:  # Only process if destination is not empty
                    input_dict = {"destination": destinations[i], "daysofvisit": str(daysofvisit)}
                    api_response = client.flow.test(flow, input_dict)
                    responses.append(api_response['result'])

            colored_header(
                label="🎯 Your Travel Plans",
                description="Here's what we found for you",
                color_name="blue-70"
            )

            result_cols = st.columns(num_destinations)
            for i in range(num_destinations):
                with result_cols[i]:
                    if i < len(responses):  # Only show results for valid responses
                        with st.expander(f"📍 {destinations[i]}", expanded=True):
                            st.markdown(responses[i])
                            

        except Exception as e:
            st.error(f"An error occurred: {e}")

# Add footer
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h6>Made with ❤️ for travel enthusiasts</h6>
    </div>
    """, unsafe_allow_html=True)
