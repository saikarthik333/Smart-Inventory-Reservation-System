import os
from app.storage import store

try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    client = None


class AIInsightService:
    """
    Optional AI-powered inventory insights.
    Never part of the transaction path.
    """

    def generate_inventory_insight(self, sku: str):
        inventory = store.get_inventory(sku)
        waitlist_size = len(store.get_waitlist(sku))

        # If AI not configured, return safe fallback
        if client is None:
            return {
                "sku": sku,
                "ai_enabled": False,
                "summary": "AI insights not configured"
            }

        prompt = f"""
        SKU: {sku}
        Available inventory: {inventory}
        Waitlist size: {waitlist_size}

        Explain the inventory situation in simple business terms.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                "sku": sku,
                "ai_enabled": True,
                "summary": response.choices[0].message.content
            }

        except Exception:
            return {
                "sku": sku,
                "ai_enabled": False,
                "summary": "AI service temporarily unavailable"
            }
