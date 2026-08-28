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
        """Generates clean, structured content specifically for Reddit and Pinterest."""
        title = offer["title"]
        desc = offer["description"]
        payout = offer["payout"]
        offer_type = offer["type"]

        if self.client:
            prompt = f"""
            You are an elite digital marketing specialist for US audiences.
            Create clean, ready-to-copy promotion text for:
            - Offer: {title} (${payout} payout, {offer_type})
            - Safe Pre-Lander Link: {safe_bridge_url}

            Output strictly in this JSON format without markdown code fences:
            {{
              "reddit_comment": "A natural 2-3 paragraph casual human response from a 27yo US resident. Helpful advice first, then naturally mentioning [{title}]({safe_bridge_url}) in the second paragraph, ending with casual tip and *(shared via partner link)*. No bold headers or bullet points.",
              "pin_title": "Catchy benefit-driven Pinterest Pin Title under 70 characters",
              "pin_description": "2-3 engaging sentences describing how to claim this reward with hashtags #USDeals #FrugalLiving #SideHustle #FreeGiftCards"
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
            "pin_title": f"How to Claim {title} (US Only)",
            "pin_description": f"Discover how verified consumer reward programs give away digital perks for quick feedback. Check out the step-by-step portal below! #FrugalLiving #USDeals #MoneyHacks #SideIncome #GiftCards"
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
