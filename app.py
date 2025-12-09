import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="COSMIC COMMAND: GAME EDITION",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 1. SOUND ENGINE ---
def play_sound(sound_type):
    # Reliable hosted sound effects
    sounds = {
        "start": "https://www.soundjay.com/buttons/button-10.mp3",       # Restart/Boot
        "scan": "https://www.soundjay.com/buttons/beep-01a.mp3",        # Scanning
        "win": "https://www.soundjay.com/misc/success-bell-01.mp3",     # Excellent/Unlocked
        "error": "https://www.soundjay.com/buttons/button-42.mp3",      # Fail
        "ping": "https://www.soundjay.com/buttons/button-30.mp3"        # Intel
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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');

    /* ANIMATED BACKGROUND */
    .stApp {
        background-color: #050508;
        background-image: 
            radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
            radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px);
        background-size: 550px 550px, 350px 350px;
        background-position: 0 0, 40px 60px;
        animation: star-move 100s linear infinite;
    }
    @keyframes star-move {
        from { background-position: 0 0, 40px 60px; }
        to { background-position: 1000px 1000px, 1040px 1060px; }
    }

    /* FONTS */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif !important; text-shadow: 0 0 10px rgba(0, 240, 255, 0.6); }
    div, button, p { font-family: 'Rajdhani', sans-serif !important; font-weight: 700; }

    /* DISPLAY BOX */
    .cosmic-display {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.95), rgba(0, 20, 30, 0.95));
        border: 2px solid #00f0ff;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.2);
    }

    /* WINNER TEXT */
    .winner-text {
        color: #39ff14;
        font-size: 45px;
        font-weight: 900;
        text-shadow: 0 0 20px #39ff14;
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0% { text-shadow: 0 0 10px #39ff14; }
        50% { text-shadow: 0 0 30px #39ff14; }
        100% { text-shadow: 0 0 10px #39ff14; }
    }

    /* BUTTON STYLES */
    div.stButton > button {
        background: #0a0a0f;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        width: 100%;
        border-radius: 5px;
        padding: 12px;
        font-size: 18px;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background: #00f0ff;
        color: black;
        box-shadow: 0 0 20px #00f0ff;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. GAME STATE ---
if 'game_active' not in st.session_state: st.session_state.game_active = False
if 'target' not in st.session_state: st.session_state.target = 50
if 'fuel' not in st.session_state: st.session_state.fuel = 100
if 'msg_main' not in st.session_state: st.session_state.msg_main = "SYSTEM ONLINE"
if 'msg_sub' not in st.session_state: st.session_state.msg_sub = "READY TO START"
if 'color' not in st.session_state: st.session_state.color = "#00f0ff"
if 'input_type' not in st.session_state: st.session_state.input_type = "SLIDER"
if 'intel_txt' not in st.session_state: st.session_state.intel_txt = ""
if 'sound' not in st.session_state: st.session_state.sound = None
if 'mode' not in st.session_state: st.session_state.mode = "EXPLORATION"
if 'max_val' not in st.session_state: st.session_state.max_val = 100

# --- 4. GAME LOGIC ---
def start_game(mode):
    st.session_state.game_active = True
    st.session_state.mode = mode
    
    # Difficulty Settings
    if mode == "EXPLORATION": st.session_state.max_val = 100
    elif mode == "SURVIVAL": st.session_state.max_val = 100
    elif mode == "QUANTUM": st.session_state.max_val = 150

    st.session_state.target = random.randint(1, st.session_state.max_val)
    st.session_state.fuel = 100
    st.session_state.msg_main = "SCANNER INITIALIZED"
    st.session_state.msg_sub = "ENTER FREQUENCY"
    st.session_state.color = "#00f0ff"
    st.session_state.intel_txt = ""
    st.session_state.sound = "start" # Initiating Sound

def get_feedback(guess, target):
    diff = abs(target - guess)
    # EASIER DIFFICULTY LOGIC
    if diff == 0: return "YOU GUESSED IT RIGHT!", "#39ff14", "win"
    elif diff <= 2: return "CRITICAL (HOT!!)", "#ff073a", "scan"
    elif diff <= 8: return "VERY CLOSE (HOT)", "#ff4500", "scan" # Widened from 5 to 8
    elif diff <= 15: return "SIGNAL DETECTED (WARM)", "#ffd700", "scan" # Widened from 10 to 15
    elif diff <= 25: return "WEAK SIGNAL (COOL)", "#00bfff", "scan"
    else: return "NO SIGNAL (FAR)", "#bf00ff", "error"

def scan(guess):
    # Juicier Animation
    with st.spinner("ANALYZING FREQUENCY..."):
        time.sleep(0.3)

    # EASIER FUEL COST
    cost = 3 # Reduced from 5
    if st.session_state.mode == "SURVIVAL": cost = 8
    
    st.session_state.fuel -= cost
    
    # Win Check
    if guess == st.session_state.target:
        st.session_state.msg_main = "YOU GUESSED IT RIGHT!"
        st.session_state.msg_sub = f"TARGET: {st.session_state.target} // EXCELLENT WORK"
        st.session_state.color = "#39ff14"
        st.session_state.sound = "win" # Success Sound
        st.balloons()
        return

    # Lose Check
    if st.session_state.fuel <= 0:
        st.session_state.msg_main = "MISSION FAILED"
        st.session_state.msg_sub = f"HIDDEN TARGET WAS: {st.session_state.target}"
        st.session_state.color = "#ff0000"
        st.session_state.sound = "error"
        return

    # Feedback
    main, col, snd = get_feedback(guess, st.session_state.target)
    
    # Helpful Direction
    if guess < st.session_state.target: sub = "TRY HIGHER ↑"
    elif guess > st.session_state.target: sub = "TRY LOWER ↓"
    else: sub = ""

    st.session_state.msg_main = main
    st.session_state.msg_sub = sub
    st.session_state.color = col
    st.session_state.sound = snd

def buy_intel():
    if st.session_state.fuel >= 15:
        st.session_state.fuel -= 15
        tgt = st.session_state.target
        
        # Easy Intel
        parity = "EVEN" if tgt % 2 == 0 else "ODD"
        sector = "1-50" if tgt <= 50 else "51-100"
        if st.session_state.max_val > 100 and tgt > 100: sector = "101-150"
        
        st.session_state.intel_txt = f"💡 INTEL: Number is {parity} & in Sector {sector}"
        st.session_state.sound = "ping"
    else:
        st.session_state.intel_txt = "❌ NOT ENOUGH FUEL"
        st.session_state.sound = "error"

# --- 5. UI RENDER ---

# Sound Trigger
if st.session_state.sound:
    play_sound(st.session_state.sound)
    st.session_state.sound = None

st.markdown("<h1 style='text-align:center; color:#00f0ff;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

if not st.session_state.game_active:
    # --- MENU ---
    st.markdown("<h3 style='text-align:center; color:#666;'>SELECT DIFFICULTY</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("EXPLORE (EASY)"): start_game("EXPLORATION")
    if c2.button("SURVIVAL (HARD)"): start_game("SURVIVAL")
    if c3.button("QUANTUM (CHAOS)"): start_game("QUANTUM")

else:
    # --- GAME BOARD ---
    
    # 1. DISPLAY SCREEN
    # If Won, show giant text
    if "RIGHT" in st.session_state.msg_main:
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: #39ff14;'>
            <div class='winner-text'>{st.session_state.msg_main}</div>
            <div style='color: #fff; letter-spacing: 2px; margin-top: 10px;'>{st.session_state.msg_sub}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Normal Display
        st.markdown(f"""
        <div class='cosmic-display' style='border-color: {st.session_state.color};'>
            <h2 style='color: {st.session_state.color}; margin:0; font-size:36px;'>{st.session_state.msg_main}</h2>
            <p style='color: #aaa; margin-top:5px; font-size:18px;'>{st.session_state.msg_sub}</p>
        </div>
        """, unsafe_allow_html=True)

    # 2. FUEL BAR
    fuel_pct = max(0, st.session_state.fuel) / 100.0
    st.progress(fuel_pct)
    st.caption(f"HYPERFUEL: {max(0, st.session_state.fuel)}%")

    # 3. CONTROLS (Hide if Game Over)
    if st.session_state.fuel > 0 and "RIGHT" not in st.session_state.msg_main:
        st.write("---")
        
        # Toggle
        c_tog1, c_tog2 = st.columns(2)
        if c_tog1.button("🎚️ SLIDER"): st.session_state.input_type = "SLIDER"
        if c_tog2.button("⌨️ KEYPAD"): st.session_state.input_type = "KEYPAD"
        
        # Input
        guess = 50
        if st.session_state.input_type == "SLIDER":
            guess = st.slider("FREQUENCY", 1, st.session_state.max_val, 50)
        else:
            guess = st.number_input("COORDINATES", 1, st.session_state.max_val, 50)

        # Actions
        c_act1, c_act2 = st.columns([2,1])
        with c_act1:
            if st.button("INITIATE SCAN", type="primary"):
                scan(guess)
        with c_act2:
            if st.button("BUY INTEL (-15)"):
                buy_intel()

        # Hints
        if st.session_state.intel_txt:
            st.info(st.session_state.intel_txt)

        st.write("")
        if st.button("🛑 ABORT MISSION"):
            st.session_state.game_active = False
            st.rerun()
            
    else:
        # RESTART BUTTON (Appears on Win or Loss)
        st.write("---")
        if st.button("🔄 REBOOT SYSTEM (PLAY AGAIN)"):
            st.session_state.game_active = False
            st.session_state.sound = "start"
            st.rerun()