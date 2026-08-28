import os

class ContentEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                print(f"[!] Warning: Could not initialize Gemini model ({e}). Using offline copy templates.")

    def generate_angles(self, offer, safe_bridge_url):
        """Generates high-converting angles for US communities."""
        title = offer["title"]
        desc = offer["description"]
        payout = offer["payout"]
        offer_type = offer["type"]

        if self.client:
            prompt = f"""
            You are an elite digital marketing strategist specializing in viral organic traffic for US audiences.
            You are writing helpful, non-spammy promotion angles for this incentive opportunity:
            
            - Title: {title}
            - Description: {desc}
            - Action Type: {offer_type}
            - Payout: ${payout}
            - Safe Pre-Lander Link: {safe_bridge_url}

            Generate 4 distinct, ready-to-copy marketing angles formatted in clean Markdown:

            1. 💬 **Reddit/Forum Value Answer**:
               - Target Subreddits: (e.g. r/beermoney, r/frugal, r/deals, r/sidehustle)
               - Context: Answering someone asking how to get free gift cards, save on groceries, or test apps.
               - Body: 2-3 short, authentic paragraphs providing genuine tips first, then subtly recommending checking out the verified resource page at `{safe_bridge_url}`.

            2. 📌 **Pinterest Pin Title & SEO Description**:
               - Pin Title: Click-worthy and benefit-driven (under 80 chars).
               - Description: 300-word SEO-optimized pin description with 5 viral hashtags (#USDeals #FrugalLiving #SideHustle #FreeGiftCards #BudgetingHacks).

            3. ❓ **Quora Thoughtful Response**:
               - Question to target: e.g. "What are the most legitimate ways to earn gift cards or test apps in the US in 2026?"
               - Detailed 3-step structured breakdown highlighting this program.

            4. ⚡ **Short-Form Hook (TikTok / Reels / Twitter)**:
               - Hook + 15-second voiceover script leading users to click the link in bio.

            Strict Rules:
            - Never use spammy buzzwords like "FREE MONEY FAST".
            - Keep tone helpful, relatable, and compliant with FTC guidelines (include a subtle `#ad` or "Verified Partner" note).
            """
            try:
                res = self.client.generate_content(prompt)
                return res.text
            except Exception as e:
                print(f"[!] Gemini generation error ({e}). Using fallback template.")

        # Fallback offline template
        return self._generate_fallback(offer, safe_bridge_url)

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
