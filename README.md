# 🌌 COSMIC COMMAND: OMEGA

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_DEPLOYMENT_URL_HERE)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![SCT Internship](https://img.shields.io/badge/SCT-Internship_Project-orange)](https://www.skillcrafttechnology.com/)

> **Status:** Mission Active 🟢  
> **Version:** 1.0.0 (Omega Update)

**Cosmic Command** is a gamified, logic-based web application developed to demonstrate advanced state management in Python. It reimagines the classic "Number Guessing Game" as a high-stakes sci-fi survival mission, featuring resource management, dynamic difficulty, and visual feedback systems.

---

## 📑 Table of Contents
- [✨ Key Features](#-key-features)
- [🎮 Gameplay Mechanics](#-gameplay-mechanics)
- [🛠️ Tech Stack & Architecture](#-tech-stack--architecture)
- [🚀 Installation & Setup](#-installation--setup)
- [📂 Project Structure](#-project-structure)
- [🔮 Future Roadmap](#-future-roadmap)
- [🤝 Credits](#-credits)

---

## ✨ Key Features

### 1. Adaptive Difficulty Modes
The system tracks player XP to unlock harder challenges:

* **🔭 Explore Mode (Rookie)**
    * **Clearance:** 0 XP (Unlocked by default)
    * **Description:** Standard training mission. 100% Fuel. Static Target.

* **🔥 Survival Mode (Cadet)**
    * **Clearance:** 300 XP
    * **Description:** **Hardcore.** Fuel reduced to 70%. High risk, high reward.

* **⚛️ Quantum Mode (Commander)**
    * **Clearance:** 500 XP
    * **Description:** **Chaos.** The target moves (±2) after every failed scan.

### 2. Immersive Feedback System
Instead of simple text, the app provides data-driven cues:
* **Thermal Sensors:** Color-coded feedback (Green=Found, Red=Hot, Blue=Cold).
* **Directional Intel:** Automated hints indicating if the target is `HIGHER` or `LOWER`.
* **Audio-Visuals:** Sound effects for actions and Lottie animations for victories.

### 3. Persistent State Management
Uses `st.session_state` to maintain:
* **XP & Rank Progress** (Rookie $\to$ Admiral)
* **Win/Loss Statistics**
* **Earned Badges** (Sniper, Veteran, First Contact)

---

## 🎮 Gameplay Mechanics

### The Mission
Your objective is to locate a specific frequency signal (a number between 1-100) before your **Hyperfuel Cell** is depleted.

### The Controls
1.  **Select Input:** Use the **Slider**, **Digital Input**, or **Manual Buttons** (+/-) to dial in a frequency.
2.  **Initiate Scan:** Click the red button to fire a probe.
3.  **Analyze Data:**
    * **Fuel Cost:** Every scan consumes **5-10% Fuel** (depending on mode).
    * **Proximity:** Watch the message box. "🔥 CRITICAL" means you are within 4 digits.
4.  **Victory:** Match the frequency exactly to trigger the win sequence and earn XP.

---

## 🛠️ Tech Stack & Architecture

This project was built to showcase rapid application development (RAD) principles.

* **Language:** Python 3.x
* **Framework:** [Streamlit](https://streamlit.io/) (Frontend & State)
* **Libraries:**
    * `random`: Procedural target generation.
    * `time`: Latency simulation (optional).
    * `streamlit-lottie`: JSON-based vector animations.
    * `requests`: Asset loading.

**Why Streamlit?**
Streamlit allows for the creation of interactive, data-driven web apps entirely in Python, making it perfect for demonstrating logic algorithms without the overhead of HTML/CSS/JS.

---

## 🚀 Installation & Setup

Follow these steps to deploy the mission control center on your local machine.
```bash
1. Clone the Repository
git clone [https://github.com/threesshad-cpu/cosmic-command.git](https://github.com/threesshad-cpu/cosmic-command.git)
cd cosmic-command
2. Create a Virtual Environment (Optional but Recommended)

Bash

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install Dependencies

Bash

pip install -r requirements.txt
4. Launch the Application

Bash

streamlit run main.py
📂 Project Structure
Plaintext

cosmic-command/
├── main.py                # Core application entry point
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
└── assets/                # (Optional) Static images or icons
🔮 Future Roadmap
[ ] Global Leaderboard: Integrate a database (Firebase/SQLite) to track high scores across all players.

[ ] Time Attack Mode: Find the target in under 30 seconds.

[ ] AI Opponent: A CPU "rival" that tries to find the number faster than you.

🤝 Credits
Developer: Threessha D

Role: Software Development Intern

Organization: SkillCraft Technology

Project ID: SCT_SD_2
