import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: ARCHIVES",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS FOR COSMIC THEME ---
# This forces the dark/neon aesthetic in the browser
st.markdown("""
    <style>
    .stApp {
        background-color: #050508;
        color: #00f0ff;
    }
    .stButton>button {
        color: #050508;
        background-color: #00f0ff;
        border: 1px solid #00f0ff;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }
    .stButton>button:hover {
        color: #00f0ff;
        background-color: #050508;
        border: 1px solid #ffffff;
    }
    h1, h2, h3 {
        color: #ffd700;
        font-family: 'Orbitron', sans-serif;
    }
    .stProgress > div > div > div > div {
        background-color: #00f0ff;
    }
    .metric-card {
        background-color: #101015;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GAME LOGIC & STATE ---
if 'target' not in st.session_state:
    st.session_state.target = random.randint(1, 100)
if 'fuel' not in st.session_state:
    st.session_state.fuel = 100
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'message' not in st.session_state:
    st.session_state.message = "SYSTEM READY. AWAITING INPUT."
if 'feedback_color' not in st.session_state:
    st.session_state.feedback_color = "gray"

# --- HELPER FUNCTIONS ---
def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "TARGET LOCKED! EXCELLENT WORK.", "green"
    elif diff <= 2: return "CRITICAL PROXIMITY (HOT!!)", "red"
    elif diff <= 5: return "HIGH INTERFERENCE (HOT)", "orange"
    elif diff <= 10: return "SIGNAL STRENGTHENING (WARM)", "yellow"
    elif diff <= 20: return "WEAK SIGNAL (COOL)", "blue"
    else: return "NO SIGNAL (FAR)", "violet"

def scan():
    if st.session_state.fuel <= 0:
        st.session_state.message = "FUEL DEPLETED. MISSION FAILED."
        st.session_state.feedback_color = "red"
        st.session_state.game_over = True
        return

    guess = st.session_state.current_guess
    target = st.session_state.target
    
    # Fuel Cost
    st.session_state.fuel -= 5
    
    # Check Win
    msg, color = get_feedback(guess, target)
    st.session_state.message = msg
    st.session_state.feedback_color = color
    
    if guess == target:
        st.session_state.game_over = True
        st.balloons() # The web version of "Fireworks"

def reset_game():
    st.session_state.target = random.randint(1, 100)
    st.session_state.fuel = 100
    st.session_state.game_over = False
    st.session_state.message = "SYSTEM RESET. NEW TARGET ACQUIRED."
    st.session_state.feedback_color = "gray"

# --- UI LAYOUT ---
st.title("🚀 COSMIC COMMAND")
st.markdown(f"**RANK:** CADET | **MODE:** EXPLORATION")

# 1. VISUALIZER SCREEN
st.markdown(f"""
<div class="metric-card">
    <h1 style='color: {st.session_state.feedback_color}; font-size: 40px;'>
        {st.session_state.message}
    </h1>
</div>
""", unsafe_allow_html=True)

st.write("") # Spacer

# 2. FUEL BAR
fuel_val = max(0, st.session_state.fuel)
st.progress(fuel_val / 100)
st.caption(f"HYPERFUEL CELL: {fuel_val}%")

st.divider()

# 3. INPUT CONTROLS
if not st.session_state.game_over:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Replaces the Slider/Keypad toggle with a simple unified input
        st.session_state.current_guess = st.slider(
            "TUNING FREQUENCY", 
            1, 100, 50
        )
    
    with col2:
        st.write("") # Alignment spacing
        st.write("") 
        if st.button("INITIATE SCAN", use_container_width=True):
            scan()
else:
    # Game Over / Win Screen
    if st.session_state.fuel > 0:
        st.success(f"INTEL ACQUIRED: The target frequency was {st.session_state.target}.")
    else:
        st.error(f"SIGNAL LOST. Target was {st.session_state.target}.")
    
    if st.button("REBOOT SYSTEM"):
        reset_game()

# 4. FOOTER / LORE
with st.expander("ACCESS CLASSIFIED INTEL DATABASE"):
    intel = [
        "THE GREAT ATTRACTOR: Pulling our galaxy at 1.3M mph.",
        "DIAMOND PLANET: 55 Cancri e is worth $26.9 nonillion.",
        "SPACE SMELL: Astronauts say space smells like seared steak."
    ]
    st.info(random.choice(intel))