# groq_agent.py
import os
from dotenv import load_dotenv
from groq import Client
from retriever import prepare_context

# -------------------------
# Load API key from .env
# -------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------
# Initialize Groq client
# -------------------------
groq_client = Client(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# -------------------------
# Thresholds for fish safety
# -------------------------
SAFE_TEMPERATURE = (20, 30)  # °C
SAFE_PH = (6.5, 8.5)
SAFE_DO = 5.0  # mg/L minimum dissolved oxygen

# -------------------------
# Water Safety Evaluation
# -------------------------
def evaluate_safety(temperature: float, ph: float, dissolved_oxygen: float) -> str:
    """
    Evaluate if the water conditions are safe for fish.

    Returns:
        str: "SAFE" or "UNSAFE"
    """
    if not (SAFE_TEMPERATURE[0] <= temperature <= SAFE_TEMPERATURE[1]):
        return "UNSAFE"
    if not (SAFE_PH[0] <= ph <= SAFE_PH[1]):
        return "UNSAFE"
    if dissolved_oxygen < SAFE_DO:
        return "UNSAFE"
    return "SAFE"

# -------------------------
# Ask Groq AI
# -------------------------
def ask_groq(query: str) -> str:
    """
    Combines real sensor context with Groq-powered reasoning.

    Parameters:
        query (str): User question about the fish pond.

    Returns:
        str: AI-generated answer including safety evaluation.
    """
    if not groq_client:
        return "⚠️ Groq API key not configured. AI response unavailable."

    context = prepare_context()

    prompt = f"""
You are AquaTrack AI — an intelligent aquaculture assistant.
Use the following live sensor context to answer user questions clearly.

Context:
{context}

User question:
{query}

Check if the water is SAFE or UNSAFE for fish based on temperature, pH, and dissolved oxygen.
Provide a concise, helpful answer and recommend actions if needed.
"""

    try:
        completion = groq_client.chat.completions.create(
            model="groq/compound",  # Change to your desired model if needed
            messages=[
                {"role": "system", "content": "You are AquaTrack, an expert aquaculture AI assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Groq API request failed: {e}")
        return "⚠️ Unable to generate AI response."

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    question = "Is the pond safe for fish today?"
    answer = ask_groq(question)
    print(answer)