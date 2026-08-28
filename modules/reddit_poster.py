import os
import json
import time
import random

class RedditPoster:
    def __init__(self, client_id=None, client_secret=None, username=None, password=None, user_agent=None):
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
        self.username = username or os.getenv("REDDIT_USERNAME")
        self.password = password or os.getenv("REDDIT_PASSWORD")
        self.user_agent = user_agent or os.getenv("REDDIT_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) US-Deals-Scanner/1.0")
        
        self.reddit = None
        self.history_file = os.path.join(os.path.dirname(__file__), "commented_posts.json")
        self.commented_ids = self._load_history()

        if self.client_id and self.client_secret and self.username and self.password:
            if self.client_id != "your_reddit_client_id":
                try:
                    import praw
                    self.reddit = praw.Reddit(
                        client_id=self.client_id,
                        client_secret=self.client_secret,
                        username=self.username,
                        password=self.password,
                        user_agent=self.user_agent
                    )
                    print(f"✅ [Reddit Engine] Connected as u/{self.username}")
                except Exception as e:
                    print(f"[!] Warning: Could not authenticate with Reddit ({e}).")

    def _load_history(self):
        """Loads list of post IDs already commented on to prevent duplicates."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return set(json.load(f))
            except Exception:
                return set()
        return set()

    def _save_history(self, post_id):
        """Records a commented post ID."""
        self.commented_ids.add(post_id)
        try:
            with open(self.history_file, "w") as f:
                json.dump(list(self.commented_ids), f)
        except Exception:
            pass

    def find_best_thread(self, subreddits=None, keywords=None):
        """Finds the most relevant, recent US question thread to answer."""
        if not subreddits:
            subreddits = ["beermoney", "frugal", "SideHustle", "freebies", "deals", "povertyfinance"]
        if not keywords:
            keywords = ["apps", "rewards", "grocery", "gift card", "survey", "save", "extra money", "side cash"]

        if not self.reddit:
            # Fallback simulated live post for demonstration when API keys aren't added yet
            return {
                "id": "sim_12345",
                "subreddit": "beermoney",
                "title": "Any legitimate apps or micro-surveys worth testing this month for US users?",
                "selftext": "Looking for some low effort reward apps or consumer panels while I have downtime at work. Let me know what is actually working and tracking properly right now.",
                "url": "https://www.reddit.com/r/beermoney/comments/sample_post/",
                "is_simulation": True
            }

        try:
            chosen_sub = random.choice(subreddits)
            subreddit = self.reddit.subreddit(chosen_sub)
            
            # Look at newest 15 submissions
            for submission in subreddit.new(limit=15):
                if submission.id in self.commented_ids or submission.archived or submission.locked:
                    continue

                full_text = (submission.title + " " + submission.selftext).lower()
                if any(kw in full_text for kw in keywords):
                    return {
                        "id": submission.id,
                        "subreddit": chosen_sub,
                        "title": submission.title,
                        "selftext": submission.selftext[:500],
                        "url": f"https://www.reddit.com{submission.permalink}",
                        "submission_obj": submission,
                        "is_simulation": False
                    }
        except Exception as e:
            print(f"[!] Reddit search warning ({e})")
            
        return None

    def generate_human_comment(self, gemini_model, post_info, offer, bridge_url):
        """Generates an ultra-realistic, natural human comment specifically tailored to the Reddit post."""
        prompt = f"""
        You are a regular 27-year-old Reddit user living in the US who frequently participates in r/beermoney and r/frugal.
        You are replying to this specific Reddit post:
        
        Subreddit: r/{post_info['subreddit']}
        Post Title: {post_info['title']}
        Post Body: {post_info['selftext']}
        
        Offer to subtly recommend:
        - Offer Name: {offer['title']}
        - Safe Resource Link: {bridge_url}
        
        Strict Rules for Ultra-Human Realism:
        1. Write in a completely natural, casual, human tone (use contractions like "I've", "didn't", "kinda", "honestly").
        2. DO NOT use markdown headers, bold bullet lists, or corporate formatting. Real Redditors write in 2 to 3 short natural paragraphs.
        3. Directly answer the user's question first with genuine general advice (e.g. mention receipt apps like Fetch or general testing tips).
        4. In the second paragraph, mention the specific opportunity you found recently and include the link naturally in a sentence: [{offer['title']}]({bridge_url}).
        5. Add a casual sign-off or small tip at the end (e.g., "Hope this helps!", "Just make sure to confirm via email so it tracks").
        6. Include a subtle disclaimer at the bottom: `*(shared via verified partner link)*`
        
        Output ONLY the raw comment text.
        """
        try:
            res = gemini_model.generate_content(prompt)
            return res.text.strip()
        except Exception as e:
            # Fallback human comment
            return f"Honestly, if you're looking for low-effort stuff that actually pays out in the US right now, I usually combine receipt scanning apps with quick consumer panels.\n\nI recently tested the [{offer['title']}]({bridge_url}) through a verified rewards hub—it only takes a couple of minutes to complete and is definitely worth checking out while it's active.\n\nJust make sure you use a valid US zip so the reward registers properly! *(shared via partner link)*"

    def post_comment(self, post_info, comment_text):
        """Posts the comment on Reddit automatically."""
        if post_info.get("is_simulation"):
            print(f"🤖 [Reddit Auto-Poster] (Simulated Mode) Would post to: {post_info['url']}")
            return {
                "success": True,
                "url": post_info["url"],
                "simulated": True
            }

        try:
            submission = post_info.get("submission_obj")
            if submission:
                comment = submission.reply(comment_text)
                self._save_history(post_info["id"])
                comment_url = f"https://www.reddit.com{comment.permalink}"
                print(f"✅ [Reddit Auto-Poster] Successfully posted comment live: {comment_url}")
                return {
                    "success": True,
                    "url": comment_url,
                    "simulated": False
                }
        except Exception as e:
            print(f"[!] Error posting comment on Reddit: {e}")
            return {
                "success": False,
                "error": str(e)
            }
