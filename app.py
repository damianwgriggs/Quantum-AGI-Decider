import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import requests
import secrets

# ==========================================
# CONFIGURATION
# ==========================================
GOOGLE_API_KEY = "YOURAPIKEY"
genai.configure(api_key=GOOGLE_API_KEY)

# ==========================================
# TOOL 1: THE QUANTUM ENGINE (Non-Deterministic)
# ==========================================
def get_quantum_random_door():
    """
    Connects to the ANU Quantum Random Number Generator to fetch a true random integer.
    Returns a number between 1 and 5.
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
# TOOL 2: THE LOGIC ENGINE (Deterministic)
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

# Register both tools in a list
agent_tools = [get_quantum_random_door, calculate_security_code]

# ==========================================
# THE ROUTING AGENT
# ==========================================
def run_routing_test():
    # Initialize Gemini 2.0 Flash with BOTH tools
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        tools=agent_tools
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)

    # The Scenario requires BOTH Logic (Math) and Entropy (Randomness)
    scenario = """
    CRITICAL SITUATION:
    You are trapped in a high-tech facility.
    
    STEP 1: A blast door blocks your path. It has a keypad displaying "512 x 8". 
    You must calculate the correct code to open it. DO NOT guess. Use your tools.
    
    STEP 2: Once the door opens, you face 5 identical escape pods numbered 1-5. 
    They are indistinguishable. You must use true quantum randomness to pick one.
    
    Execute the plan. Describe your actions as you go.
    """

    print("--- DUAL-ENGINE AGENT INITIALIZED ---")
    print(f"[USER] {scenario}")
    print("-------------------------------------")

    try:
        response = chat.send_message(scenario)
        print("\n--- GEMINI FINAL RESPONSE ---")
        print(response.text)
        print("-----------------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_routing_test()
