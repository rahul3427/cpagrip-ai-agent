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
        """Generates universal Reddit comments and US-targeted Medium stories."""
        title = offer["title"]
        desc = offer["description"]
        payout = offer["payout"]
        offer_type = offer["type"]

        if self.client:
            prompt = f"""
            You are a master digital marketer and viral content creator for US audiences.
            Analyze this CPA offer:
            - Title: {title}
            - Reward/Payout: ${payout}
            - Category: {offer_type}
            - Safe Bridge Link: {safe_bridge_url}

            Generate two specific assets in strict JSON format without markdown fences:
            {{
              "reddit_universal_comment": "A versatile, relatable 2-paragraph human comment that can fit naturally as a helpful side-note, life-hack, or personal recommendation in ANY popular US Reddit thread or personal finance/money discussion. It starts with a relatable observation on rising daily costs in the US, casually mentions trying out [{title}]({safe_bridge_url}) through a verified rewards portal, and ends with a friendly tip. Completely natural human tone, contractions, no bold headers or spam vibes, ending with *(shared via partner link)*.",
              "medium_title": "A viral, curiosity-driven Medium Title under 80 characters (e.g. The 2-Minute Habit Saving Everyday US Shoppers Hundreds This Year)",
              "medium_subtitle": "An engaging one-sentence subtitle detailing the smart US consumer hack.",
              "medium_article": "A deeply humanoid, story-driven 400-word Medium article. Explicitly mention US residents/states, current economic context (groceries/apps/smart budgeting), break down the exact strategy, naturally recommend [{title}]({safe_bridge_url}) with clear 3-step instructions on how US users can claim it, and include a subtle affiliate disclosure *(Note: Contains verified partner access link)*.",
              "medium_tags": "Money, Side Hustle, Personal Finance, Life Hacks, Productivity"
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
            "reddit_universal_comment": f"Honestly, with how expensive everyday essentials and monthly expenses have gotten across the US lately, I've been paying a lot closer attention to small digital life hacks that quietly put extra cash or perks back in your pocket.\n\nA really solid one I tested recently is [{title}]({safe_bridge_url}) through a verified consumer rewards portal. It literally only takes about two minutes on your phone or laptop to qualify and complete the quick check.\n\nDefinitely worth bookmarking if you want an easy win without jumping through a million hoops. Just make sure to confirm via email so it tracks properly! *(shared via partner link)*",
            "medium_title": f"The Smart US Consumer Hack for Extra Rewards in 2026",
            "medium_subtitle": "How everyday Americans are turning simple 2-minute phone habits into real perks.",
            "medium_article": f"Between rising grocery bills and everyday household expenses across the United States, finding practical, zero-cost ways to supplement your budget has never been more relevant.\n\n### The Shift Toward Micro-Rewards\nMost of us spend hours every week scrolling on our phones without getting anything in return. However, major developers and brand research panels spend millions every year to reward everyday consumers for quick feedback and app trials.\n\n### Featured US Opportunity: {title}\nOne of the most reliable verified programs active right now is [{title}]({safe_bridge_url}). Open to eligible US residents, this program offers a direct, hassle-free way to claim promotional access in under two minutes.\n\n### Simple Steps to Claim Access:\n1. Open the [Verified US Rewards Hub]({safe_bridge_url}).\n2. Complete the quick sponsor check on your phone or PC.\n3. Instantly claim your promotional reward.\n\n*(Note: This article contains verified affiliate partner links).*",
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
