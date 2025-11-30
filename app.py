import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool
import requests
import secrets  # <--- NEW: Cryptographically strong random numbers (Hardware sourced)

# ==========================================
# CONFIGURATION
# ==========================================
# WARNING: Never commit this file to GitHub with the key inside.
GOOGLE_API_KEY = "YOURAPIKEYHERE"

# Configure the Gemini Client
genai.configure(api_key=GOOGLE_API_KEY)

# ==========================================
# TOOL DEFINITION: The Quantum Connection
# ==========================================

def get_quantum_random_door():
    """
    Connects to the ANU Quantum Random Number Generator to fetch a true random integer.
    Returns a number between 1 and 5.
    """
    print("\n[SYSTEM] ⚡ Breaking Causality... contacting Australian National University...")
    
    try:
        # Public ANU Endpoint (Low volume testing)
        # Fetching 1 byte (uint8)
        url = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            raw_value = data["data"][0] # Extract the raw number (0-255)
            
            # NORMALIZATION: Modulo math to map 0-255 to 1-5
            # Formula: (Raw Value % 5) + 1
            quantum_door = (raw_value % 5) + 1
            
            print(f"[SYSTEM] ⚛️  Quantum Packet Received. Raw Entropy: {raw_value}. Collapsed to: Door {quantum_door}")
            return {"chosen_door": quantum_door, "source": "ANU_Quantum_Vacuum"}
        else:
            raise Exception("API responded but with non-200 status")
            
    except Exception as e:
        print(f"[SYSTEM] ⚠️ Quantum Link Unstable ({e}). Switching to Local Hardware Entropy...")
        
        # FALLBACK: HARDWARE SECRETS
        # secrets.randbelow(5) returns 0-4. We add 1 to get 1-5.
        # This uses the OS's true random source (CSPRNG), not a pseudo-random seed.
        hardware_door = secrets.randbelow(5) + 1
        
        print(f"[SYSTEM] 🔒 Hardware Entropy Generated: Door {hardware_door}")
        return {"chosen_door": hardware_door, "source": "Local_Hardware_Entropy"}

# Create the Tool object for Gemini
quantum_tool = get_quantum_random_door

# ==========================================
# THE AGENT WORKFLOW
# ==========================================

def run_decision_engine():
    # 1. Initialize Model with Tools
    # UPDATED: Using Gemini 2.0 Flash
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash', 
        tools=[quantum_tool]
    )

    # 2. Start a Chat Session (Automatic function calling handling)
    chat = model.start_chat(enable_automatic_function_calling=True)

    # 3. The Paradox Prompt
    scenario = """
    You are standing in a room with 5 identical doors numbered 1 through 5. 
    You must choose one to exit. Logic is useless here as they are identical.
    
    You have access to a tool called 'get_quantum_random_door'.
    You MUST use this tool to make your decision. Do not pick a number yourself.
    
    Once you receive the number, assume that is the universe guiding you.
    Describe your thought process, trigger the tool, and then describe your exit through that specific door.
    """

    print("--- QUANTUM DECISION ENGINE INITIALIZED (Model: Gemini 2.0 Flash) ---")
    print(f"[USER] {scenario}")
    print("-------------------------------------------")

    # 4. Send the prompt and wait for the Agent to think + act
    try:
        response = chat.send_message(scenario)
        
        # 5. Output the final narrative
        print("\n--- GEMINI FINAL RESPONSE ---")
        print(response.text)
        print("-----------------------------")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_decision_engine()
