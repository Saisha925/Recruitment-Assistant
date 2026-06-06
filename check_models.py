import os
from dotenv import load_dotenv
from google import genai

# Load your API key from the .env file
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("🔍 Asking Google what models your key is allowed to use...")
print("-" * 50)

try:
    # This fetches the live list of models directly from Google's servers
    for model in client.models.list():
        # We only want models that support text generation
        if "generateContent" in model.supported_actions:
            print(f"✅ {model.name}")
except Exception as e:
    print(f"❌ Failed to fetch models: {e}")
    
print("-" * 50)