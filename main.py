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
from modules.reddit_poster import RedditPoster
from modules.pinterest_generator import PinterestGenerator

def run_agent():
    print("🤖 [AI Agent] Initializing Autonomous Multi-Platform Traffic Engine...")

    # 1. Initialize Engines
    offer_engine = OfferEngine()
    content_engine = ContentEngine()
    bridge_generator = BridgeGenerator(base_url=os.getenv("BRIDGE_BASE_URL", "https://rahul3427.github.io/rewards-hub/"))
    notifier = Notifier()
    reddit_poster = RedditPoster()
    pin_generator = PinterestGenerator()

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

    # 4. Generate Structured Content with Gemini
    print("✍️ [4/4] Generating High-Converting Reddit & Medium Angles...")
    angles = content_engine.generate_angles(best_offer, safe_bridge_link)
    reddit_comment = angles.get("reddit_comment", "")
    medium_title = angles.get("medium_title", best_offer["title"])
    medium_subtitle = angles.get("medium_subtitle", "Verified US promotional opportunity.")
    medium_article = angles.get("medium_article", "")
    medium_tags = angles.get("medium_tags", "Side Hustle, Money, Productivity, Apps")

    # ==========================================
    # MESSAGE 1: REDDIT ACTION CARD
    # ==========================================
    reddit_message = f"""🔥 *REDDIT ACTION CARD (30-Sec Post)*

📌 *Offer Name:* {best_offer['title']} (${best_offer['payout']})
📍 *Target Geo:* US ({best_offer['type']})

🎯 *Step 1: Click a link below to open recent US questions:*
👉 [Open r/beermoney Discussions](https://www.reddit.com/r/beermoney/search/?q=apps+reward+testing&sort=new)
👉 [Open r/frugal Discussions](https://www.reddit.com/r/frugal/search/?q=save+money+rewards&sort=new)
👉 [Open r/SideHustle Discussions](https://www.reddit.com/r/SideHustle/search/?q=easy+money+apps&sort=new)

📋 *Step 2: Tap COPY CODE below to copy & paste this comment:*
```text
{reddit_comment}
```
"""

    # ==========================================
    # MESSAGE 2: MEDIUM ACTION CARD
    # ==========================================
    medium_message = f"""📝 *MEDIUM ACTION CARD (1-Minute Story)*

🚀 *Step 1: Open Medium Story Creator:*
👉 [Click to Write New Story on Medium](https://medium.com/new-story)

🏷️ *Step 2: Subtitle (Optional):*
```text
{medium_subtitle}
```

📄 *Step 3: Tap COPY CODE below for Full Article Body:*
```text
{medium_article}
```

🏷️ *Step 4: Tap COPY CODE below for 5 Topic Tags:*
```text
{medium_tags}
```
"""

    # ==========================================
    # MESSAGE 3: STANDALONE MEDIUM TITLE (1-TAP FULL COPY)
    # ==========================================
    medium_title_message = f"{medium_title}"

    # Dispatch to Telegram in clean sequence
    notifier.send_notification(reddit_message)
    notifier.send_notification(medium_message)
    notifier.send_notification(medium_title_message)
    print("✨ [AI Agent] Pipeline execution complete. Reddit & Medium cards delivered to Telegram!")

if __name__ == "__main__":
    run_agent()
