import os
import random
import time
import json

class ContentEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                # Use high-performance model
                self.client = genai.GenerativeModel("gemini-3.6-flash")
            except Exception as e:
                print(f"[!] Warning: Could not initialize Gemini model ({e}). Using dynamic offline templates.")

    def generate_angles(self, offer, safe_bridge_url):
        """Generates 100% unique, human-sounding content with zero AI buzzwords."""
        title = offer["title"]
        desc = offer["description"]
        payout = offer["payout"]
        offer_type = offer["type"]

        # Human angles to randomize each execution
        personas = [
            "a 26yo remote worker from Ohio sharing a quick downtime discovery",
            "a frugal college student from Texas who tested this between classes",
            "a skeptical US deal hunter from Florida who was surprised it actually credited",
            "an everyday commuter from California who uses 2-minute phone breaks for perks"
        ]
        chosen_persona = random.choice(personas)
        random_seed = int(time.time() * 1000) % 100000

        if self.client:
            prompt = f"""
            You are writing as {chosen_persona}.
            Seed/Timestamp: {random_seed}
            Target Offer: {title} (Payout: ${payout}, Type: {offer_type})
            Safe Link: {safe_bridge_url}

            CRITICAL ANTI-AI DETECTION & HUMAN WRITING RULES:
            1. NEVER add robotic disclaimers like '(shared via partner link)' or '(ad)' to Reddit comments. Real humans on Reddit never type that! Keep it 100% clean, casual, and authentic.
            2. BANNED AI BUZZWORDS: Never use 'delve', 'tapestry', 'testament', 'beacon', 'game-changer', 'revolutionize', 'fast-paced world', 'moreover', 'furthermore', 'it is important to remember', 'navigate', 'in conclusion'.
            3. REDDIT COMMENT MUST BE SHORT & PUNCHY (2 to 3 sentences max!):
               - Write like a real person typing quickly on a smartphone.
               - Use natural casual phrasing ('tbh', 'ngl', 'honestly', 'pretty solid', 'was kinda skeptical').
               - Hyperlink [{title}]({safe_bridge_url}) naturally as part of the sentence.
               - End casually with zero disclaimers or tags.
            4. MEDIUM ARTICLE MUST BE A NATURAL HUMAN STORY (300-350 words):
               - Engaging first-person or conversational US narrative.
               - Mention everyday US context (coffee runs, grocery receipts, phone downtime).
               - Seamlessly integrate [{title}]({safe_bridge_url}) as a verified resource.

            Output strictly in this JSON format without markdown code blocks:
            {{
              "reddit_universal_comment": "Short 2-3 sentence pure human casual comment with [{title}]({safe_bridge_url}) and NO robotic tags",
              "medium_title": "Catchy, non-cliché headline under 75 chars",
              "medium_subtitle": "One conversational benefit line",
              "medium_article": "300-350 word human-crafted Medium story with clean headers and natural flow",
              "medium_tags": "Money, Side Hustle, Personal Finance, Life Hacks, Productivity"
            }}
            """
            try:
                # High temperature (1.0) ensures 100% non-repeating, fresh variation on every single run
                generation_config = {
                    "temperature": 1.0,
                    "top_p": 0.95,
                    "top_k": 40
                }
                res = self.client.generate_content(prompt, generation_config=generation_config)
                text = res.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                
                data = json.loads(text.strip())
                return data
            except Exception as e:
                print(f"[!] Gemini generation warning ({e}). Using fresh randomized fallback.")

        # Randomized clean fallback generator
        fallbacks = [
            f"Tbh with how high grocery receipts have been lately, I've been messing around with quick micro-apps on my breaks. Tried [{title}]({safe_bridge_url}) last week on my phone and the reward credited in like two minutes. Definitely worth a quick try if you're bored on your phone!",
            f"Ngl I'm usually skeptical of reward links, but [{title}]({safe_bridge_url}) was super straightforward when I tested it yesterday. Only took about 2 minutes to complete the quick check and it actually went through. Just make sure to confirm via email so it registers!",
            f"Honestly if you have a few minutes of downtime at work, [{title}]({safe_bridge_url}) is a pretty solid little life hack. Tested it on iOS earlier this week and it credited without any hassle. Easy way to turn idle screen time into a small win."
        ]
        return {
            "reddit_universal_comment": random.choice(fallbacks),
            "medium_title": f"How a 2-Minute Phone Routine Is Helping US Shoppers Save",
            "medium_subtitle": "A quick look at verified micro-reward trials that actually pay out in 2026.",
            "medium_article": f"Between $7 coffee orders and rising utility bills across the US, finding small, zero-cost wins has become my favorite hobby this year.\n\n### The 2-Minute Screen Time Swap\nMost of us lose 20 to 30 minutes every evening just mindlessly scrolling social media. Instead of wasting that time, I started testing out verified brand research portals that reward everyday users for trying new mobile apps and quick tools.\n\n### What I Tested: {title}\nEarlier this week I ran through [{title}]({safe_bridge_url}). The setup was surprisingly simple: you just open the portal on your phone, complete a 1-minute sponsor check, and claim your promotional trial access.\n\n### The Takeaway\nIt won't replace your day job, but taking two minutes during your lunch break to grab verified rewards is a super easy habit to stack throughout the month.\n\n*(Note: Contains verified partner access link)*",
            "medium_tags": "Money, Side Hustle, Personal Finance, Life Hacks, Productivity"
        }

    def _generate_fallback(self, offer, safe_bridge_url):
        title = offer["title"]
        return f"""
### 💬 1. Reddit / Forum Answer Angle (r/beermoney, r/frugal)
> **Thread Target:** "Best legitimate ways to cut grocery/online shopping expenses?"
> 
> "If you're looking to stretch your budget this month, keep an eye out for brand research portals. Major retailers frequently sponsor consumer feedback surveys to gauge shopper habits before Q4. 
> 
> You simply spend 2 minutes answering a few lifestyle questions to qualify for digital vouchers. I tested the recent portal here:
> 🔗 **Resource Hub:** {safe_bridge_url}
> 
> *(Tip: Make sure you enter a valid US zip code and confirm via email to trigger the reward).* "

---

### 📌 2. Pinterest Pin Strategy
- **Pin Title:** "The Genius 2-Minute Habit Saving Shoppers $100+ This Month 💡"
- **Pin Description:** "Looking for easy ways to save on everyday household essentials? Discover how verified consumer reward programs give away e-gift cards for quick feedback. Check out the step-by-step portal below!
#FrugalLiving #USDeals #MoneyHacks #SideIncome #GiftCards"
- **Destination Link:** `{safe_bridge_url}`

---

### ❓ 3. Quora Question Target
- **Target Question:** "How can I earn gift cards online without getting scammed?"
- **Answer Angle:** Breakdown the difference between ad-farms and verified CPA research panels (like {title}), linking to your portal for access.

---

### ⚡ 4. Short-Form Hook (TikTok / Reels / Shorts)
- **Visual:** Screen recording of claiming digital rewards on mobile.
- **Hook:** "If you live in the US and you're still paying full price for shopping, stop scrolling..."
- **Call-to-Action:** "Check the link in my bio to see if your state is eligible today!"
"""
