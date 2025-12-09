import streamlit as st
import random
import time
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="COSMIC COMMAND: ELITE",
    page_icon="👾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. ASSETS & SOUNDS ---
# We use HTML5 audio tags to play sounds in the browser
def play_sound(sound_type):
    # These are simple hosted sound effect links (or you can use base64)
    sounds = {
        "scan": "https://www.soundjay.com/buttons/beep-01a.mp3",
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",
        "error": "https://www.soundjay.com/buttons/button-10.mp3"
    }
    if sound_type in sounds:
        # This invisible HTML component triggers the audio
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_type]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 2. ADVANCED CSS (THE VISUAL MAGIC) ---
st.markdown("""
    <style>
    /* IMPORT ORBITRON FONT */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

    /* ANIMATED STARFIELD BACKGROUND */
    .stApp {
        background-color: #000;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
            radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
        background-size: 550px 550px, 350px 350px, 250px 250px;
        background-position: 0 0, 40px 60px, 130px 270px;
        animation: star-move 20s linear infinite;
    }
    
    @keyframes star-move {
        from { background-position: 0 0, 40px 60px, 130px 270px; }
        to { background-position: 550px 550px, 590px 610px, 680px 820px; }
    }

    /* GENERAL TEXT STYLING */
    h1, h2, h3, p, div, span {
        font-family: 'Orbitron', sans-serif !important;
        text-shadow: 0px 0px 5px rgba(0, 240, 255, 0.7);
    }

    /* GLASSMORPHISM CARD ( The Main Panel ) */
    .cosmic-card {
        background: rgba(16, 16, 21, 0.85);
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
        text-align: center;
        margin-bottom: 20px;
        backdrop-filter: blur(5px);
    }

    /* NEON BUTTONS */
    .stButton>button {
        background: transparent;
        color: #00f0ff;
        border: 2px solid #00f0ff;
        border-radius: 5px;
        padding: 10px 25px;
        font-size: 18px;
        transition: 0.3s;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
    }
    .stButton>button:hover {
        background: #00f0ff;
        color: #000;
        box-shadow: 0 0 20px #00f0ff;
        border-color: #00f0ff;
    }
    .stButton>button:active {
        color: white;
    }

    /* CUSTOM SLIDER */
    div[data-baseweb="slider"] > div {
        background-color: #00f0ff !important;
    }

    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. GAME LOGIC ---
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 100)
if 'fuel' not in st.session_state:
    st.session_state.fuel = 100
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = "SYSTEM ONLINE. SCANNER READY."
if 'feedback_color' not in st.session_state:
    st.session_state.feedback_color = "#00f0ff" # Cyan default
if 'sound_trigger' not in st.session_state:
    st.session_state.sound_trigger = None

def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "TARGET LOCKED! SYSTEM UNLOCKED.", "#39ff14", "win" # Neon Green
    elif diff <= 2: return "CRITICAL PROXIMITY (HOT!!)", "#ff073a", "scan" # Neon Red
    elif diff <= 5: return "HIGH INTERFERENCE (HOT)", "#ff4500", "scan" # Orange Red
    elif diff <= 10: return "SIGNAL DETECTED (WARM)", "#ffd700", "scan" # Gold
    elif diff <= 20: return "WEAK SIGNAL (COOL)", "#00bfff", "scan" # Deep Sky Blue
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error" # Purple

def scan():
    if st.session_state.fuel <= 0:
        st.session_state.message = "FUEL CRITICAL. MISSION ABORT."
        st.session_state.feedback_color = "#ff0000"
        st.session_state.game_over = True
        st.session_state.sound_trigger = "error"
        return

    # Logic
    guess = st.session_state.current_guess
    target = st.session_state.target
    st.session_state.fuel -= 5
    
    # Feedback
    msg, color, sound = get_feedback(guess, target)
    st.session_state.message = msg
    st.session_state.feedback_color = color
    st.session_state.sound_trigger = sound
    
    if guess == target:
        st.session_state.game_over = True
        st.balloons()

def reset_game():
    st.session_state.target = random.randint(1, 100)
    st.session_state.fuel = 100
    st.session_state.game_over = False
    st.session_state.message = "SYSTEM RESET. TARGET ACQUIRED."
    st.session_state.feedback_color = "#00f0ff"
    st.session_state.sound_trigger = "scan"

# --- 4. THE LAYOUT (HTML INJECTION) ---

# Trigger Sound if needed
if st.session_state.sound_trigger:
    play_sound(st.session_state.sound_trigger)
    st.session_state.sound_trigger = None # Reset sound

# Header
st.markdown("<h1 style='text-align: center; color: #00f0ff;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>SECURE ARCHIVE DECRYPTION MODULE</p>", unsafe_allow_html=True)

# Main Display Panel (Glassmorphism)
st.markdown(f"""
<div class="cosmic-card">
    <h2 style='color: {st.session_state.feedback_color}; font-size: 32px; margin: 0;'>
        {st.session_state.message}
    </h2>
    <p style='color: #888; margin-top: 10px;'>SIGNAL INTEGRITY MONITOR</p>
</div>
""", unsafe_allow_html=True)

# Fuel Bar (Custom Styled)
fuel_color = "#00f0ff" if st.session_state.fuel > 30 else "#ff0000"
st.markdown(f"""
<div style="background-color: #333; border-radius: 5px; padding: 3px; margin-bottom: 20px; border: 1px solid #555;">
    <div style="width: {st.session_state.fuel}%; background-color: {fuel_color}; height: 10px; border-radius: 2px;
    box-shadow: 0 0 10px {fuel_color}; transition: width 0.5s;"></div>
</div>
""", unsafe_allow_html=True)

# Game Controls
if not st.session_state.game_over:
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Just a visual rank indicator
        st.markdown("""
        <div style="border: 1px solid #333; padding: 10px; border-radius: 5px; text-align: center;">
            <div style="color: #ffd700; font-size: 12px;">RANK</div>
            <div style="color: white; font-weight: bold;">CADET</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.session_state.current_guess = st.slider(
            "ADJUST FREQUENCY", 
            1, 100, 50, label_visibility="collapsed"
        )

    st.write("")
    if st.button("INITIATE SCAN SEQUENCE", use_container_width=True):
        scan()

else:
    # Win/Lose State
    if st.session_state.fuel > 0:
        st.markdown(f"""
        <div style="background: rgba(57, 255, 20, 0.1); border: 1px solid #39ff14; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h3 style="color: #39ff14;">ACCESS GRANTED</h3>
            <p style="color: white;">The secret frequency was <b>{st.session_state.target}</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"CONNECTION LOST. TARGET WAS {st.session_state.target}.")
    
    if st.button("REBOOT SYSTEM"):
        reset_game()

# Footer Lore
st.markdown("---")
with st.expander("📂 VIEW DECRYPTED INTEL"):
    intel_data = [
        "Great Attractor: Pulling our galaxy at 1.3M mph.",
        "Zombie Stars: Type Ia supernovas explode twice.",
        "Void: The Bootes Void is 330M light-years empty."
    ]
    st.info(random.choice(intel_data))