import os
import sys
from dotenv import load_dotenv

# Ensure utf-8 encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load local environment variables if available
load_dotenv()

from modules.offer_engine import OfferEngine
from modules.content_engine import ContentEngine
from modules.bridge_generator import BridgeGenerator
from modules.notifier import Notifier

def run_agent():
    print("🤖 [AI Agent] Initializing Autonomous CPA Traffic Engine...")

    # 1. Initialize Engines
    offer_engine = OfferEngine()
    content_engine = ContentEngine()
    bridge_generator = BridgeGenerator(base_url=os.getenv("BRIDGE_BASE_URL", "https://rahul3427.github.io/rewards-hub/"))
    notifier = Notifier()

    # 2. Fetch & Evaluate Best US Offers
    print("🔎 [1/4] Scanning CPAGrip for highest EPC US offers...")
    top_offers = offer_engine.fetch_offers()
    if not top_offers:
        print("❌ No qualifying US offers found.")
        return

    best_offer = top_offers[0]
    print(f"🎯 [2/4] Selected Top Offer: '{best_offer['title']}' (EPC: {best_offer['epc']} | Payout: ${best_offer['payout']})")

    # 3. Generate Anti-Ban Safe Bridge Link
    safe_bridge_link = bridge_generator.generate_safe_url(best_offer["link"], best_offer["title"])
    print(f"🛡️ [3/4] Generated Safe Pre-Lander Link: {safe_bridge_link}")

    # 4. Generate Viral Marketing Angles
    print("✍️ [4/4] Generating US Audience Psychological Hooks with Gemini Flash...")
    marketing_angles = content_engine.generate_angles(best_offer, safe_bridge_link)

    # 5. Format & Dispatch Notification
    tg_briefing = f"""🚀 *TOP CPAGRIP US OFFER DETECTED*

📌 *Offer:* {best_offer['title']}
💰 *Payout:* ${best_offer['payout']} | *EPC:* {best_offer['epc']}
📍 *Target Geo:* {best_offer['country']} ({best_offer['type']})

🛡️ *Your Safe Pre-Lander Link:*
`{safe_bridge_link}`

---
{marketing_angles}
"""

    notifier.send_notification(tg_briefing)
    print("✨ [AI Agent] Pipeline execution complete.")

if __name__ == "__main__":
    run_agent()
