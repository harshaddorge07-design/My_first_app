import streamlit as st
import time
import base64
import itertools
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    


def premium_loading(messages=None, duration_per_message=1.2):
    """
    Drop-in replacement for st.spinner() with a custom flying-plane
    animation and cycling travel-themed status text.

    Usage:
        with premium_loading(["Checking flights...", "Mapping your route...", "Finding hidden gems..."]):
            result = call_your_ai_function()
    """
    if messages is None:
        messages = ["Loading..."]

    class _PremiumLoader:
        def __enter__(self):
            self.placeholder = st.empty()
            self.stop = False
            self._render(messages[0])
            return self

        def _render(self, text):
            self.placeholder.markdown(
                f"""
                <div style="
                    display:flex;
                    flex-direction:column;
                    align-items:center;
                    justify-content:center;
                    padding: 2rem 0;
                ">
                    <div style="
                        position:relative;
                        width:220px;
                        height:40px;
                        margin-bottom:1rem;
                    ">
                        <div style="
                            position:absolute;
                            top:50%;
                            left:0;
                            right:0;
                            height:1px;
                            background:repeating-linear-gradient(
                                90deg,
                                rgba(202,161,93,0.4) 0px,
                                rgba(202,161,93,0.4) 6px,
                                transparent 6px,
                                transparent 14px
                            );
                        "></div>
                        <div style="
                            position:absolute;
                            top:50%;
                            font-size:22px;
                            transform: translateY(-50%);
                            animation: flyacross 1.8s ease-in-out infinite;
                        ">✈️</div>
                    </div>
                    <div style="
                        color:#caa15d;
                        font-size:0.9rem;
                        font-weight:500;
                        letter-spacing:0.02em;
                    ">{text}</div>
                </div>

                <style>
                @keyframes flyacross {{
                    0%   {{ left: 0%; opacity: 0; }}
                    10%  {{ opacity: 1; }}
                    90%  {{ opacity: 1; }}
                    100% {{ left: 92%; opacity: 0; }}
                }}
                </style>
                """,
                unsafe_allow_html=True,
            )

        def cycle(self):
            """Call this in a loop if your task has no natural steps to hook into."""
            for msg in itertools.cycle(messages):
                if self.stop:
                    break
                self._render(msg)
                time.sleep(duration_per_message)

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.placeholder.empty()
            return False

    return _PremiumLoader()


# --- Example usage: simple wrap around a slow call ---

st.markdown("""
<div style= "glass card: center; padding: 20px 0px;">
    <h1 style="color: #1E88E5; font-size: 3rem; margin-bottom: 0px;">🌍 AI Travel Assistant</h1>
    <p style="font-size: 1.2rem; color: #555555; font-style: italic;">
        Discover personalized itineraries, smart recommendations, and seamless travel planning.
    </p>
</div>
<hr style="margin-top: 10px; margin-bottom: 30px;">
""", unsafe_allow_html=True)

st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def set_premium_background(map_image_path=None):
    """
    Dark, premium-feeling background:
    - deep navy/black gradient base
    - optional faint line-art world map at low opacity as texture
    - glassmorphism card styling for content
    """
    map_layer = ""
    if map_image_path:
        b64_img = get_base64(map_image_path)
        map_layer = f"""
        background-image:
            linear-gradient(rgba(6, 10, 20, 0.94), rgba(6, 10, 20, 0.94)),
            url("data:image/png;base64,{b64_img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        """
    else:
        # No image? Pure gradient mesh — zero licensing hassle, still feels premium.
        map_layer = """
        background: radial-gradient(circle at 20% 20%, #10182b 0%, #060a14 45%),
                    radial-gradient(circle at 80% 80%, #1a1030 0%, transparent 50%),
                    #060a14;
        background-attachment: fixed;
        """

    st.markdown(
        f"""
        <style>
        .stApp {{
            {map_layer}
            color: #eef1f8;
        }}

        /* Glassmorphism cards for content blocks */
        .glass-card {{
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 1.5rem 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
        }}

        /* Restrained accent color for buttons/links — swap for your brand */
        .stButton>button {{
            background: linear-gradient(135deg, #caa15d, #e8c988);
            color: #1a1400;
            border: none;
            border-radius: 10px;
            font-weight: 600;
        }}

        h1, h2, h3 {{
            font-weight: 600;
            letter-spacing: -0.01em;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_premium_background()
st.title("AI Travel Assistant")
st.write("Welcome!")

destination = st.text_input("Where you would like to go")
days = st.number_input("How many days of trip",min_value=1, max_value=30)
budget = st.selectbox("Select your Budget", ["Luxury", "Moderate", "Budget"], placeholder= "select option", index= None)
travel_type = st.selectbox("Who is travelling", ["Solo","Couple", "Family with kids", "Group of friends"], placeholder="select option", index=None)
interest = st.multiselect("What is your goal for this trip", ["relaxation", "adventure", "culture", "history", "food", "nightlife", "nature"])
transportation = st.multiselect("which transport would you like to pefer",["Public transit", "rental car", "walking", "taxis"] )


prompt = f"""You are a travel planner. 
He/She want to go {destination} placesfor {days} days.
He/She is on the budget of {budget}. The travel type of He/She is {travel_type} 
Give me suggestion in bullet format. He/she want {transportation} 
to travel, he/she have interest in {interest}"""
if st.button("Plan trip"):
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input= prompt        
        )
    
    with premium_loading(["Checking flights...", "Comparing prices...", "Almost there..."]):
        time.sleep(3)  # replace with your actual AI/API call
    

    st.success("Destination guide loaded!")
    st.success("OK, Here is your fab suggestion.")
    st.write(interaction.output_text)
