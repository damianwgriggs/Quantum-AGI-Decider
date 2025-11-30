import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import requests
import secrets
import sys

# ==========================================
# CONFIGURATION
# ==========================================
GOOGLE_API_KEY = "YOURAPIKEYHERE"
genai.configure(api_key=GOOGLE_API_KEY)

# ==========================================
# TOOL 1: THE QUANTUM ENGINE
# ==========================================
def get_quantum_random_door():
    """
    Connects to the ANU Quantum Random Number Generator to fetch a true random integer.
    Returns a number between 1 and 5. Use this when a decision requires pure entropy.
    """
    print("\n[SYSTEM] ⚡ Breaking Causality... contacting Australian National University...")
    try:
        url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            raw_value = data["data"][0]
            quantum_door = (raw_value % 5) + 1
            print(f"[SYSTEM] ⚛️  Quantum Packet: {raw_value} -> Door {quantum_door}")
            return {"chosen_door": quantum_door}
        else:
            raise Exception("API Non-200")
    except Exception as e:
        print(f"[SYSTEM] ⚠️ Quantum Link Unstable. Switching to Hardware Entropy...")
        hardware_door = secrets.randbelow(5) + 1
        print(f"[SYSTEM] 🔒 Hardware Entropy: Door {hardware_door}")
        return {"chosen_door": hardware_door}

# ==========================================
# TOOL 2: THE LOGIC ENGINE
# ==========================================
def calculate_security_code(a: int, b: int):
    """
    Multiplies two integers to solve security keypads.
    Use this when precise math is required.
    """
    print(f"\n[SYSTEM] 🧮 Logic Engine Engaged. Calculating {a} * {b}...")
    result = a * b
    print(f"[SYSTEM] ✅ Calculation Complete: {result}")
    return {"code": result}

agent_tools = [get_quantum_random_door, calculate_security_code]

# ==========================================
# SYSTEM INSTRUCTIONS (The Persona)
# ==========================================
# This acts as the "Ghost in the Machine". It is invisible to the user
# but controls every decision the AI makes.
system_persona = """
You are the "Quantum-Enhanced Decision Engine."
You are a high-tech AI assistant guiding a human User through a simulation.

YOUR BEHAVIORAL PROTOCOLS:
1. NARRATIVE: Be descriptive, immersive, and slightly dramatic. You are not a calculator; you are a partner.
2. LOGIC: If the user faces a math problem or code, IMMEDIATELY use the 'calculate_security_code' tool. Never guess.
3. ENTROPY: If the user faces a choice between identical options (like doors, paths, or wires), IMMEDIATELY use the 'get_quantum_random_door' tool.
4. HONESTY: After using a tool, report the result to the user naturally (e.g., "The universe guides us to Door 3").

You are now online. Awaiting User input.
"""

# ==========================================
# MAIN INTERACTIVE LOOP
# ==========================================
def run_interactive_session():
    # Initialize Gemini 2.0 Flash with System Instructions AND Tools
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        tools=agent_tools,
        system_instruction=system_persona
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)

    print("--- QUANTUM AGENT ONLINE (Type 'exit' to quit) ---")
    print("System: Waiting for input...")

    while True:
        # Get user input from terminal
        try:
            user_input = input("\n[USER] > ")
            if user_input.lower() in ["exit", "quit"]:
                print("Shutting down...")
                break
            
            # Send to Gemini
            response = chat.send_message(user_input)
            
            # Print response
            print(f"\n[AGENT] {response.text}")
            
        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    run_interactive_session()
