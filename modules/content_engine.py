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
            # Diverse authentic storytelling themes for Medium
            story_themes = [
                "a cozy reflection on balancing a tight household budget and discovering small unexpected perks",
                "a funny and honest recount of a morning routine realization and testing a regional community perk",
                "a relatable story about swapping 5 minutes of phone doomscrolling for something actually worthwhile",
                "a thoughtful essay on how modern digital word-of-mouth helps everyday people find real deals"
            ]
            chosen_theme = random.choice(story_themes)

            prompt = f"""
            You are an authentic, warm, and friendly US essayist writing on Medium.
            Theme: {chosen_theme}
            Location/Background: {chosen_persona}
            Reward Opportunity: {title}
            Direct Resource Link: {safe_bridge_url}

            CRITICAL MEDIUM WRITING & LINK RULES (NO PROMOTIONAL VIBES):
            1. NEVER write numbered tutorials ('Step 1, Step 2, Step 3') or salesy callouts like 'Official Claim Page'. That sounds like an ad!
            2. ORGANIC 'EXPLORE' INVITATION: Weave the link naturally as a casual, no-pressure discovery for fellow readers to explore if they are curious.
               Examples:
               - "If you're curious to explore it yourself, here's the page I checked: {safe_bridge_url}"
               - "I bookmarked the link here in case anyone wants to see if it's active in their area: {safe_bridge_url}"
               - "Feel free to check it out here if you have a couple minutes during your break: {safe_bridge_url}"
            3. DEEP HUMAN CONNECTION: Focus on real emotion, everyday life observations, and why small wins matter when living costs feel high.
            4. COMMUNITY ENGAGEMENT: End with a warm, open-ended question inviting readers to share their own small daily life hacks or coffee routines in the comments.
            5. ZERO BANNED AI WORDS: No 'delve', 'tapestry', 'testament', 'beacon', 'game-changer', 'revolutionize', 'fast-paced', 'moreover', 'furthermore', 'in conclusion'.

            REDDIT WRITING RULES:
            - Comment 1 (Popular): Short 2-3 sentence casual break discovery with [{title}]({safe_bridge_url}).
            - Comment 2 (Money): Short 2-3 sentence smart budgeting tip with [{title}]({safe_bridge_url}).
            - Zero robotic disclaimers.

            Output strictly in this JSON format without markdown code blocks:
            {{
              "reddit_comment_url1": "Short 2-3 sentence casual comment for Popular posts with [{title}]({safe_bridge_url})",
              "reddit_comment_url2": "Short 2-3 sentence money-saving comment for Money posts with [{title}]({safe_bridge_url})",
              "medium_title": "Warm, relatable personal essay title under 75 chars",
              "medium_subtitle": "A reflective one-sentence thought that hooks readers",
              "medium_article": "320-380 word deeply personal, non-promotional story with smooth paragraphs and casual link invitation {safe_bridge_url}",
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
            "medium_title": f"The Small Everyday Habits That Keep My Monthly Budget Sane",
            "medium_subtitle": "Why taking 2 minutes to test regional community perks beats endless doomscrolling.",
            "medium_article": f"Living here in the US and watching our monthly expense totals climb has definitely changed how I look at everyday downtime. Between morning coffee runs and regular grocery trips, small costs have a way of silently piling up before you even realize it.\n\nEarlier this week, instead of losing twenty minutes mindlessly scrolling through social media feeds, I decided to see if word-of-mouth digital perks were actually worth a quick break. A coworker mentioned a regional program where US residents can check their local zip code for active sponsor vouchers.\n\nI was pretty skeptical at first, but it only took about a minute to check eligibility. It won't replace a paycheck, but grabbing a quick win like this helped cover a coffee run without dipping into my account.\n\nIf you're curious to explore it yourself, here is the page I used:\n{safe_bridge_url}\n\nHave you found any neat little routines or habits that help you trim daily expenses? Drop your thoughts below—I'd love to hear how you manage it!",
            "medium_tags": "Life Lessons, Personal Finance, Money, Self Improvement, Frugal Living"
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
