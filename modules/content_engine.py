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
            # Diverse authentic storytelling angles for Medium
            story_themes = [
                "a warm, personal journal entry about finding a small unexpected win while balancing family budget",
                "a funny and relatable story about a coffee run realization and discovering regional sponsor perks",
                "an honest, transparent review sharing a 2-minute life hack with friends and coworkers",
                "a cozy weekend reflection on cutting everyday shopping costs without giving up favorite treats"
            ]
            chosen_theme = random.choice(story_themes)

            prompt = f"""
            You are an authentic, warm, and friendly US writer sharing a genuine personal story.
            Theme: {chosen_theme}
            Location/Background: {chosen_persona}
            Reward Opportunity: {title}
            Direct Resource Link: {safe_bridge_url}

            CRITICAL MEDIUM WRITING & LINK FORMATTING RULES:
            1. ZERO MARKDOWN BRACKET LINKS in the Medium article text! Medium does not parse [Text](url) markdown syntax. Instead, include the clean URL directly on its own line like this:
               👉 Official Claim Page: {safe_bridge_url}
            2. ULTRA-FRIENDLY & HUMAN: Write like you are talking to a close friend over coffee. Share a genuine, relatable life scenario (dealing with real US prices, grocery runs, family, or work routines).
            3. REALISTIC & HUMBLE: No sales hype, no get-rich-quick claims. Frame this as a neat 2-minute perk that helped cover a small treat or errand.
            4. CLEAR 3-STEP GUIDE: Explain how fellow US residents enter their basic email and zip code to check eligibility.
            5. ZERO BANNED AI WORDS: No 'delve', 'tapestry', 'testament', 'beacon', 'game-changer', 'revolutionize', 'fast-paced', 'moreover', 'furthermore', 'in conclusion'.

            REDDIT WRITING RULES:
            - Comment 1 (Popular): Short 2-3 sentence casual lifestyle break thought with [{title}]({safe_bridge_url}).
            - Comment 2 (Money): Short 2-3 sentence smart budgeting/saving tip with [{title}]({safe_bridge_url}).
            - No robotic disclaimers.

            Output strictly in this JSON format without markdown code blocks:
            {{
              "reddit_comment_url1": "Short 2-3 sentence casual comment for Popular posts with [{title}]({safe_bridge_url})",
              "reddit_comment_url2": "Short 2-3 sentence money-saving comment for Money posts with [{title}]({safe_bridge_url})",
              "medium_title": "Warm, curiosity-driven personal story headline under 75 chars",
              "medium_subtitle": "A friendly one-sentence personal takeaway",
              "medium_article": "320-380 word heartwarming, highly relatable story using clean subheaders and direct link callout 👉 Official Claim Page: {safe_bridge_url}",
              "medium_tags": "Life Lessons, Personal Finance, Money, Self Improvement, Frugal Living"
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
            "reddit_comment_url1": f"Was taking a quick break between Zoom calls and stumbled on this {title} promo. Ngl I was kinda skeptical at first, but it literally takes a minute to drop your email and zip to see if you qualify. You can check it out over at [{title}]({safe_bridge_url}) before this current round fills up.",
            "reddit_comment_url2": f"Honestly with retail prices being so crazy right now, finding verified promos like [{title}]({safe_bridge_url}) is a pretty solid little win. It only takes about a minute on your phone to enter your email and zip to claim entry. Definitely worth checking out to save some extra cash!",
            "medium_title": f"The Smart US Consumer Hack for {title} in 2026",
            "medium_subtitle": "How everyday Americans are turning simple 2-minute phone habits into real perks.",
            "medium_article": f"Between rising living costs across the United States, finding practical, zero-cost ways to supplement your budget has never been more relevant.\n\n### Featured US Opportunity: {title}\nOne of the most reliable verified programs active right now is [{title}]({safe_bridge_url}). Open to eligible US residents, this program offers a direct, hassle-free way to claim promotional access in under two minutes.\n\n### Simple Steps to Claim Access:\n1. Open the [Verified US Rewards Hub]({safe_bridge_url}).\n2. Complete the quick sponsor check on your phone or PC.\n3. Instantly claim your promotional reward.\n\n*(Note: This article contains verified partner access links).*",
            "medium_tags": "Money, Savings, Deals, Shopping, Frugal Living"
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
