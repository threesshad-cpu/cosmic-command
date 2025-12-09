import streamlit as st
import random
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cosmic Command: Omega", layout="wide", page_icon="🌌")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .stButton button { border-radius: 5px; }
    .feedback-box { padding: 15px; border-radius: 10px; text-align: center; color: black; font-weight: bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. LOGIC, AUDIO & PROGRESSION
# ==========================================

def play_sound(sound_type):
    # Using reliable sound effects
    sounds = {
        "start": "https://www.soundjay.com/buttons/sounds/button-30.mp3",
        "win": "https://www.soundjay.com/misc/sounds/magic-chime-02.mp3",
        "reset": "https://www.soundjay.com/mechanical/sounds/clank-1.mp3",
        "scan": "https://www.soundjay.com/buttons/sounds/button-09.mp3"
    }
    if sound_type in sounds:
        st.markdown(f"""<audio autoplay><source src="{sounds[sound_type]}" type="audio/mpeg"></audio>""", unsafe_allow_html=True)

def calculate_rank(xp):
    if xp < 300: return "ROOKIE"
    elif xp < 500: return "CADET"     
    elif xp < 1000: return "COMMANDER"
    else: return "ADMIRAL"

def check_badges():
    # Only adds badges if criteria met
    new_badge = None
    if st.session_state.wins >= 1 and "First Contact" not in st.session_state.badges:
        st.session_state.badges.append("First Contact")
        new_badge = "First Contact"
    # Sniper: Win with > 80 fuel left
    if st.session_state.fuel > 80 and st.session_state.game_over and st.session_state.last_diff == 0:
        if "Sniper" not in st.session_state.badges:
            st.session_state.badges.append("Sniper")
            new_badge = "Sniper"
    if st.session_state.wins >= 5 and "Veteran" not in st.session_state.badges:
        st.session_state.badges.append("Veteran")
        new_badge = "Veteran"
    return new_badge

def get_feedback_data(diff):
    if diff == 0: return "🌌 SIGNAL LOCKED! TARGET ACQUIRED!", "#00FF00", 1.0 
    elif diff <= 4: return "🔥 CRITICAL! (VERY CLOSE!)", "#FF0000", 0.9  
    elif diff <= 10: return "🔥 HOT", "#FF4500", 0.8                     
    elif diff <= 20: return "☀️ WARMER", "#FF8C00", 0.6                  
    elif diff <= 30: return "🌤️ WARM", "#FFD700", 0.4 
    elif diff <= 50: return "☁️ COOL", "#87CEEB", 0.2 
    elif diff <= 75: return "❄️ COLD", "#1E90FF", 0.1 
    else: return "🧊 FREEZING (FAR)", "#00008B", 0.05 

# --- STATE INITIALIZATION ---
def init_state():
    if 'xp' not in st.session_state: st.session_state.xp = 0
    if 'wins' not in st.session_state: st.session_state.wins = 0
    if 'losses' not in st.session_state: st.session_state.losses = 0
    if 'badges' not in st.session_state: st.session_state.badges = [] 
    
    if 'target' not in st.session_state: st.session_state.target = None
    if 'game_active' not in st.session_state: st.session_state.game_active = False
    if 'game_mode' not in st.session_state: st.session_state.game_mode = "EXPLORE"
    if 'fuel' not in st.session_state: st.session_state.fuel = 100
    if 'game_over' not in st.session_state: st.session_state.game_over = False
    
    if 'msg' not in st.session_state: st.session_state.msg = "Awaiting Input..."
    if 'msg_color' not in st.session_state: st.session_state.msg_color = "#FFFFFF"
    if 'last_diff' not in st.session_state: st.session_state.last_diff = 100
    if 'signal_strength' not in st.session_state: st.session_state.signal_strength = 0.0
    if 'directional_intel' not in st.session_state: st.session_state.directional_intel = "Unknown"
    
    if 'current_guess' not in st.session_state: st.session_state.current_guess = 50

init_state()
current_rank = calculate_rank(st.session_state.xp)

# ==========================================
# 2. SIDEBAR: COMMAND DECK
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ COMMAND DECK")
    
    st.markdown(f"""<div style="border: 2px solid #FFD700; border-radius: 8px; padding: 8px; text-align: center; color: #FFD700; font-weight: bold; background-color: rgba(255, 215, 0, 0.1);">{current_rank}</div>""", unsafe_allow_html=True)
    
    # XP Goals
    if st.session_state.xp < 300: next_goal = 300
    elif st.session_state.xp < 500: next_goal = 500
    elif st.session_state.xp < 1000: next_goal = 1000
    else: next_goal = 2000
    
    prog = st.session_state.xp / next_goal if next_goal > 0 else 1.0
    st.progress(min(prog, 1.0))
    st.caption(f"XP: {st.session_state.xp} / {next_goal}")
    
    st.write("---")
    c1, c2 = st.columns(2)
    with c1: st.metric("WINS", st.session_state.wins)
    with c2: st.metric("LOSSES", st.session_state.losses)
    
    st.write("---")
    st.markdown("###### 🏅 BADGES :")
    if not st.session_state.badges: st.caption("No badges earned yet.")
    for b in st.session_state.badges: st.markdown(f"• {b}")
    
    with st.expander("📄 MODES INFO"):
        st.info("EXPLORE: Standard. 100% Fuel.")
        st.warning("SURVIVAL: Unlocks at 300 XP. 70% Fuel.")
        st.error("QUANTUM: Unlocks at 500 XP. Target Shifts.")

# ==========================================
# 3. MAIN GAME INTERFACE
# ==========================================
st.markdown("<h1 style='text-align: center; color: #00FFFF; letter-spacing: 4px;'>COSMIC COMMAND</h1>", unsafe_allow_html=True)

# --- SCENE 1: THE MENU ---
if not st.session_state.game_active:
    st.markdown("<h3 style='text-align: center;'>SELECT MISSION PROFILE</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    def start_game(mode, fuel, sound=True):
        st.session_state.game_mode = mode
        st.session_state.target = random.randint(1, 100)
        st.session_state.fuel = fuel
        st.session_state.game_active = True
        st.session_state.game_over = False
        st.session_state.msg = f"SYSTEM READY ({mode} MODE)"
        st.session_state.msg_color = "#FFFFFF"
        st.session_state.directional_intel = "❓ Awaiting Scan"
        st.session_state.signal_strength = 0.0
        if sound: play_sound("start")
        st.rerun()

    with col1:
        if st.button("EXPLORE (Lvl 1)", use_container_width=True): start_game("EXPLORE", 100)
    with col2:
        disabled = st.session_state.xp < 300
        # --- SURVIVAL BUFF: Starts with 70 Fuel ---
        if st.button("SURVIVAL (Lvl 2)", disabled=disabled, use_container_width=True): start_game("SURVIVAL", 70)
    with col3:
        disabled = st.session_state.xp < 500
        # --- QUANTUM BUFF: Starts with 90 Fuel ---
        if st.button("QUANTUM (Lvl 3)", disabled=disabled, use_container_width=True): start_game("QUANTUM", 90)

# --- SCENE 2: GAMEPLAY ---
elif not st.session_state.game_over:
    
    st.write("---")
    st.markdown(f"**CURRENT MODE: {st.session_state.game_mode}**")
    
    # 1. DISPLAY VISUAL FEEDBACK
    st.markdown(f"""
    <div class="feedback-box" style="background-color: {st.session_state.msg_color}; box-shadow: 0 0 15px {st.session_state.msg_color};">
        <h2>{st.session_state.msg}</h2>
    </div>
    """, unsafe_allow_html=True)

    # 2. INTEL & SIGNAL STATUS
    ic1, ic2 = st.columns([3, 1])
    with ic1:
        st.markdown(f"**📡 SIGNAL STRENGTH:**")
        st.progress(st.session_state.signal_strength)
    with ic2:
        st.markdown(f"**🧭 INTEL:**")
        st.info(f"{st.session_state.directional_intel}")

    st.write("") 

    # 3. CONTROL PANEL
    st.markdown("### 🎛️ CONTROL PANEL")
    
    def update_guess_from_slider(): st.session_state.current_guess = st.session_state.slider_val
    def update_guess_from_number(): st.session_state.current_guess = st.session_state.num_val
    def adjust_guess(amount): 
        st.session_state.current_guess = max(1, min(100, st.session_state.current_guess + amount))

    input_tab1, input_tab2, input_tab3 = st.tabs(["🎚️ Slider", "🔢 Digital", "🎮 Manual(Recomm)"])
    
    with input_tab1:
        st.slider("Scan Frequency", 1, 100, key="slider_val", value=st.session_state.current_guess, on_change=update_guess_from_slider)
    with input_tab2:
        st.number_input("Precise Frequency Input", 1, 100, key="num_val", value=st.session_state.current_guess, on_change=update_guess_from_number)
    with input_tab3:
        bc1, bc2, bc3 = st.columns([1, 2, 1])
        with bc1: 
            if st.button("➖ 1", use_container_width=True): adjust_guess(-1)
            if st.button("➖ 5", use_container_width=True): adjust_guess(-5)
        with bc2:
            st.markdown(f"<h2 style='text-align: center; border: 1px solid gray; border-radius: 5px;'>{st.session_state.current_guess}</h2>", unsafe_allow_html=True)
        with bc3:
            if st.button("➕ 1", use_container_width=True): adjust_guess(1)
            if st.button("➕ 5", use_container_width=True): adjust_guess(5)

    # 4. ACTION BUTTON
    st.write("---")
    if st.button("🔴 INITIATE SCAN", use_container_width=True, type="primary"):
        play_sound("scan")
        
        # --- COSTS ---
        cost = 5 
        if st.session_state.game_mode == "SURVIVAL": cost = 10
        elif st.session_state.game_mode == "QUANTUM": cost = 5
        
        st.session_state.fuel -= cost
        
        guess = st.session_state.current_guess
        target = st.session_state.target
        diff = abs(guess - target)
        st.session_state.last_diff = diff
        
        # =========================================
        # CRITICAL LOGIC FIX: WIN vs LOSE SEPARATION
        # =========================================
        
        # CHECK 1: DID WE WIN?
        if diff == 0:
            st.session_state.game_over = True
            st.session_state.wins += 1
            play_sound("win")
            
            # REWARDS
            base_xp = 100
            if st.session_state.game_mode == "SURVIVAL": base_xp = 200
            if st.session_state.game_mode == "QUANTUM": base_xp = 300
            
            st.session_state.xp += base_xp
            new_b = check_badges()
            if new_b: st.toast(f"🏆 NEW BADGE: {new_b}!")
            
            st.rerun() # STOP HERE.

        # CHECK 2: DID WE RUN OUT OF FUEL (AND NOT WIN)?
        if st.session_state.fuel <= 0:
            st.session_state.game_over = True
            st.session_state.losses += 1
            # DO NOT ADD XP HERE
            st.rerun() # STOP HERE.

        # CHECK 3: CONTINUE GAME (HINTS)
        if not st.session_state.game_over:
            if st.session_state.game_mode == "QUANTUM":
                shift = random.choice([-2, -1, 1, 2])
                st.session_state.target = max(1, min(100, st.session_state.target + shift))
                st.toast("⚠️ QUANTUM FLUX: Target Shifted slightly!")

            msg, color, strength = get_feedback_data(diff)
            st.session_state.msg = msg
            st.session_state.msg_color = color
            st.session_state.signal_strength = strength
            
            if st.session_state.target > guess:
                st.session_state.directional_intel = "⬆️ HIGHER"
            else:
                st.session_state.directional_intel = "⬇️ LOWER"
            
            st.rerun()

    st.caption(f"HYPERFUEL CELL: {st.session_state.fuel}%")
    st.progress(max(0, st.session_state.fuel) / 100)

# --- SCENE 3: GAME OVER ---
else:
    # Check if we won (fuel doesn't matter if we hit the target, but checking logic)
    # Actually, we rely on the fact that if we are here, game_over is True.
    # The only way to know if we won is checking 'last_diff' or if we didn't lose fuel.
    # BUT easier: Check if last_diff is 0.
    
    if st.session_state.last_diff == 0:
        # VICTORY SCENE
        play_sound("win")
        st.balloons() # <--- RELIABLE CELEBRATION
        
        st.markdown(f"""
        <div style="border: 4px solid #00FF00; box-shadow: 0px 0px 50px #00FF00; background-color: black; border-radius: 10px; padding: 40px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: #00FFFF; font-size: 50px;">🎉 TARGET UNLOCKED! 🎉</h1>
            <h3 style="color: white;">SEQUENCE COMPLETE. TARGET: {st.session_state.target}</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        # DEFEAT SCENE
        st.snow() # <--- RELIABLE DEFEAT EFFECT
        st.markdown(f"""
        <div style="border: 2px solid #FF0000; box-shadow: 0px 0px 20px #FF0000; background-color: black; border-radius: 10px; padding: 40px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: #FF0000;">MISSION FAILED</h1>
            <p style="color: white;">FUEL DEPLETED. TARGET WAS: {st.session_state.target}</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 RETURN TO BASE", type="primary", use_container_width=True):
        play_sound("reset")
        st.session_state.game_active = False
        st.session_state.game_over = False
        st.rerun()