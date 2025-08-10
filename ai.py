import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIInsightGenerator:
    def generate_insight(self, symbol, recent_prices):
        prompt = (
            f"Analyze the recent prices of {symbol}: "
            f"{', '.join(map(str, recent_prices))}. "
            "Give a brief trading insight."
        )
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )
        return response.choices[0].message.content.strip()
