import os

class ContentEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel("gemini-3.6-flash")
            except Exception as e:
                print(f"[!] Warning: Could not initialize Gemini model ({e}). Using offline copy templates.")

    def generate_angles(self, offer, safe_bridge_url):
        """Generates clean, structured content specifically for Reddit and Medium."""
        title = offer["title"]
        desc = offer["description"]
        payout = offer["payout"]
        offer_type = offer["type"]

        if self.client:
            prompt = f"""
            You are an elite digital marketing and SEO writer specializing in US audience conversion.
            Analyze this offer:
            - Title: {title}
            - Reward/Payout: ${payout}
            - Type: {offer_type}
            - Safe Pre-Lander Link: {safe_bridge_url}

            Output strictly in this JSON format without markdown code fences:
            {{
              "reddit_comment": "A natural 2-3 paragraph casual human response from a 27yo US resident. Helpful advice first, then naturally mentioning [{title}]({safe_bridge_url}) in the second paragraph, ending with casual tip and *(shared via partner link)*. No bold headers or corporate lists.",
              "medium_title": "High-CTR, curiosity-driven Medium Story Title under 80 characters (e.g. The 2-Minute Habit Saving US Shoppers Money This Month)",
              "medium_subtitle": "Engaging one-sentence subtitle explaining the benefit",
              "medium_article": "A high-quality 350-450 word Medium article with 2-3 subheadings. Structure: 1. Introduction acknowledging rising US living costs or routine phone habits. 2. Real strategy breakdown. 3. Highlighting [{title}]({safe_bridge_url}) as a verified zero-cost opportunity. 4. Practical takeaway steps and affiliate disclosure *(Note: Contains partner resource links)*.",
              "medium_tags": "Side Hustle, Money, Productivity, Apps, Lifestyle"
            }}
            """
            try:
                res = self.client.generate_content(prompt)
                text = res.text.strip()
                if text.startswith("```json"):
                    text = text[7:]
                if text.startswith("```"):
                    text = text[3:]
                if text.endswith("```"):
                    text = text[:-3]
                
                import json
                data = json.loads(text.strip())
                return data
            except Exception as e:
                print(f"[!] Gemini structured parsing error ({e}). Using clean fallback.")

        # Clean fallback
        return {
            "reddit_comment": f"Honestly, if you're looking for low-effort stuff that actually pays out in the US right now, I usually combine receipt scanning apps with quick consumer panels.\n\nI recently tested the [{title}]({safe_bridge_url}) through a verified rewards hub—it only takes a couple of minutes to complete and is definitely worth checking out while it's active.\n\nJust make sure you use a valid US zip so the reward registers properly! *(shared via partner link)*",
            "medium_title": f"The Smart Way to Test New Apps & Earn Rewards in 2026",
            "medium_subtitle": "How verified micro-reward programs are helping everyday US users earn in their downtime.",
            "medium_article": f"Managing a personal budget in 2026 requires looking for smart, low-friction habits that put extra cash or gift cards in your pocket without demanding hours of your day.\n\n### The Rise of Mobile Micro-Testing\nApp developers spend millions of dollars annually acquiring new test users. Instead of sitting through lengthy questionnaires, modern rewards networks offer micro-tasks where you simply download, test, and engage with trending applications for a couple of minutes.\n\n### Featured US Opportunity: {title}\nOne of the most active campaigns running this month is [{title}]({safe_bridge_url}). Available for US residents, this program allows users to access verified trials and claim instant incentives upon quick onboarding.\n\n### How to Get Started:\n1. Open the [Verified Rewards Portal]({safe_bridge_url}).\n2. Complete the quick 1-minute sponsor check.\n3. Enjoy your digital reward!\n\n*(Disclosure: This article contains verified affiliate partner links).*",
            "medium_tags": "Side Hustle, Money, Productivity, Technology, Lifestyle"
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
