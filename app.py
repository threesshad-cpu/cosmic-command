import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: ULTIMATE",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. SOUND ENGINE (WEB) ---
def play_sound(sound_type):
    sounds = {
        "scan": "https://www.soundjay.com/buttons/beep-01a.mp3",
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",
        "error": "https://www.soundjay.com/buttons/button-10.mp3",
        "ping": "https://www.soundjay.com/buttons/button-30.mp3" 
    }
    if sound_type in sounds:
        st.markdown(f"""
            <audio autoplay>
                <source src="{sounds[sound_type]}" type="audio/mp3">
            </audio>
            """, unsafe_allow_html=True)

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto+Mono&display=swap');

    .stApp {
        background-color: #000;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px);
        background-size: 550px 550px, 350px 350px;
        background-position: 0 0, 40px 60px;
        animation: star-move 60s linear infinite;
    }
    @keyframes star-move {
        from { background-position: 0 0, 40px 60px; }
        to { background-position: 550px 550px, 590px 610px; }
    }

    h1, h2, h3, button { font-family: 'Orbitron', sans-serif !important; text-shadow: 0 0 5px rgba(0, 240, 255, 0.5); }
    p, div, label, input { font-family: 'Roboto Mono', monospace; }

    .cosmic-display {
        background: rgba(10, 10, 15, 0.9);
        border: 2px solid #00f0ff;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.2);
    }

    div.stButton > button {
        background: #050508;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        width: 100%;
        border-radius: 5px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: #00f0ff;
        color: black;
        box-shadow: 0 0 15px #00f0ff;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'message' not in st.session_state: st.session_state.message = "SYSTEM STANDBY"
if 'feedback_color' not in st.session_state: st.session_state.feedback_color = "#444"
if 'input_method' not in st.session_state: st.session_state.input_method = "SLIDER"
if 'hint_text' not in st.session_state: st.session_state.hint_text = ""
if 'sound_trigger' not in st.session_state: st.session_state.sound_trigger = None

# --- 4. GAME FUNCTIONS ---
def start_game(mode):
    st.session_state.game_active = True
    st.session_state.target = random.randint(1, 100)
    st.session_state.fuel = 100
    st.session_state.message = "SCANNER INITIALIZED"
    st.session_state.feedback_color = "#00f0ff"
    st.session_state.hint_text = ""
    st.session_state.sound_trigger = "scan"

def get_feedback(guess, target):
    diff = abs(target - guess)
    if diff == 0: return "TARGET LOCKED!", "#39ff14", "win"
    elif diff <= 2: return "CRITICAL (HOT!!)", "#ff073a", "scan"
    elif diff <= 5: return "HIGH SIGNAL (HOT)", "#ff4500", "scan"
    elif diff <= 10: return "DETECTING (WARM)", "#ffd700", "scan"
    elif diff <= 20: return "WEAK SIGNAL (COOL)", "#00bfff", "scan"
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error"

def scan_target(guess):
    # 1. Deduct Fuel First
    st.session_state.fuel -= 5
    
    # 2. Check Win Condition (Prioritize winning over dying on the last turn)
    if guess == st.session_state.target:
        st.session_state.message = f"TARGET LOCKED: {st.session_state.target}"
        st.session_state.feedback_color = "#39ff14"
        st.session_state.sound_trigger = "win"
        st.balloons()
        return

    # 3. Check Loss Condition (Game Over)
    if st.session_state.fuel <= 0:
        st.session_state.message = f"FAILED. TARGET WAS {st.session_state.target}"
        st.session_state.feedback_color = "#ff0000"
        st.session_state.sound_trigger = "error"
        return

    # 4. Normal Feedback Loop (Game Continues)
    msg, color, sound = get_feedback(guess, st.session_state.target)
    
    if guess < st.session_state.target: direction = "(TOO LOW)"
    elif guess > st.session_state.target: direction = "(TOO HIGH)"
    else: direction = ""

    st.session_state.message = f"{msg} {direction}"
    st.session_state.feedback_color = color
    st.session_state.sound_trigger = sound

def buy_intel():
    if st.session_state.fuel >= 15:
        st.session_state.fuel -= 15
        tgt = st.session_state.target
        low = max(1, tgt - random.randint(5,15))
        high = min(100, tgt + random.randint(5,15))
        st.session_state.hint_text = f"INTEL: Target is between {low} and {high}"
        st.session_state.sound_trigger = "ping"
    else:
        st.session_state.hint_text = "ERROR: Insufficient Fuel"
        st.session_state.sound_trigger = "error"

# --- 5. UI LAYOUT ---

if st.session_state.sound_trigger:
    play_sound(st.session_state.sound_trigger)
    st.session_state.sound_trigger = None

st.markdown("<h1 style='text-align:center; color:#00f0ff; margin-bottom:0;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    # MENU SCREEN
    st.markdown("<div class='cosmic-display'><h3>SELECT MISSION PROTOCOL</h3></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("EXPLORATION"): start_game("EXPLORATION")
    if c2.button("SURVIVAL"): start_game("SURVIVAL")
    if c3.button("QUANTUM"): start_game("QUANTUM")

else:
    # GAME SCREEN
    st.markdown(f"""
    <div class='cosmic-display' style='border-color: {st.session_state.feedback_color};'>
        <h2 style='color: {st.session_state.feedback_color}; font-size: 32px; margin: 0;'>
            {st.session_state.message}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    fuel_pct = max(0, st.session_state.fuel) / 100.0
    st.progress(fuel_pct)
    st.caption(f"HYPERFUEL CELL: {max(0, st.session_state.fuel)}%")
    
    # Only show controls if fuel is remaining OR if we just won
    if st.session_state.fuel > 0 and "LOCKED" not in st.session_state.message:
        c_mode1, c_mode2 = st.columns(2)
        if c_mode1.button("QUANTUM TUNER (SLIDER)"): st.session_state.input_method = "SLIDER"
        if c_mode2.button("DIGITAL KEYPAD (TYPE)"): st.session_state.input_method = "KEYPAD"
        
        st.write("---")
        
        guess = 50
        if st.session_state.input_method == "SLIDER":
            guess = st.slider("FREQUENCY", 1, 100, 50, label_visibility="collapsed")
        else:
            guess = st.number_input("ENTER COORDINATES", 1, 100, 50, label_visibility="collapsed")
        
        c_act1, c_act2 = st.columns([2, 1])
        with c_act1:
            if st.button("INITIATE SCAN", type="primary"):
                scan_target(guess)     
        with c_act2:
            if st.button("BUY INTEL (-15)"):
                buy_intel()

        if st.session_state.hint_text:
            st.info(st.session_state.hint_text)
            
        st.write("")
        if st.button("< ABORT MISSION"):
            st.session_state.game_active = False
            st.rerun()

    else:
        # GAME OVER / WIN SCREEN ACTIONS
        st.write("---")
        if st.button("REBOOT MISSION (PLAY AGAIN)"):
            st.session_state.game_active = False
            st.rerun()