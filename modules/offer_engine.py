import os
import requests
import json

class OfferEngine:
    def __init__(self, user_id=None, api_key=None, min_epc=0.0, target_geo="US", target_category="Email/Zip Submit"):
        self.user_id = user_id or os.getenv("CPAGRIP_USER_ID")
        self.api_key = api_key or os.getenv("CPAGRIP_KEY")
        self.target_geo = target_geo or os.getenv("TARGET_GEO", "US")
        self.target_category = target_category
        self.history_file = os.path.join(os.path.dirname(__file__), "used_offers.json")
        self.used_offer_ids = self._load_used_offers()

    def _load_used_offers(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_used_offer(self, offer_id):
        self.used_offer_ids.append(offer_id)
        # Keep last 15 offers in history
        self.used_offer_ids = self.used_offer_ids[-15:]
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.used_offer_ids, f)
        except Exception:
            pass

    def fetch_offers(self):
        """Fetches and rotates high-payout US Email/Zip Submit offers."""
        if self.user_id and self.api_key and self.user_id != "your_cpagrip_user_id":
            url = f"https://www.cpagrip.com/common/offer_feed_json.php?user_id={self.user_id}&key={self.api_key}&showall=yes"
            try:
                response = requests.get(url, timeout=20)
                data = response.json()
                raw_offers = data.get("offers", [])
                if raw_offers:
                    return self._filter_and_rank(raw_offers)
            except Exception as e:
                print(f"[!] Warning: Could not fetch live CPAGrip feed ({e}). Using sample offers.")

        # Fallback realistic sample US Email/Zip offers
        return self._get_sample_offers()

    def _filter_and_rank(self, offers):
        """Filters strictly for US Email/Zip Submit and ranks by highest payout."""
        filtered = []
        for o in offers:
            geo = o.get("accepted_countries") or o.get("country", "")
            cat = o.get("category") or o.get("type", "")
            
            # Extract Payout
            try:
                payout = float(o.get("payout", 0))
            except (ValueError, TypeError):
                payout = 0.0

            # Extract EPC
            epc_raw = o.get("netepc") or o.get("epc", 0)
            try:
                epc = float(epc_raw)
            except (ValueError, TypeError):
                epc = 0.0

            # Strictly match US and Email/Zip Submit
            if self.target_geo in geo and "Email" in cat:
                filtered.append({
                    "id": str(o.get("offer_id", "")),
                    "title": o.get("title", "Exclusive US Reward"),
                    "description": o.get("description", "Enter your email & zip to qualify."),
                    "payout": f"{payout:.2f}",
                    "payout_val": payout,
                    "epc": f"${epc:.3f}",
                    "epc_val": epc,
                    "country": geo,
                    "type": "Email/Zip Submit",
                    "link": o.get("offerlink", "#")
                })

        if not filtered:
            print("[!] No US Email/Zip Submit offers found. Checking global fallbacks.")
            return self._get_sample_offers()

        # Sort by HIGHEST PAYOUT first, then by EPC
        sorted_offers = sorted(filtered, key=lambda x: (x["payout_val"], x["epc_val"]), reverse=True)
        
        # Pick the top offer that hasn't been used recently for daily variety
        for candidate in sorted_offers:
            if candidate["id"] not in self.used_offer_ids:
                self._save_used_offer(candidate["id"])
                print(f"🎯 [Offer Engine] Selected Fresh High-Payout US Email/Zip Offer: '{candidate['title']}' (${candidate['payout']})")
                return [candidate]

        # If all were used, reset history and pick the highest payout offer
        self.used_offer_ids = []
        best = sorted_offers[0]
        self._save_used_offer(best["id"])
        print(f"🎯 [Offer Engine] Selected Top High-Payout US Email/Zip Offer: '{best['title']}' (${best['payout']})")
        return [best]

    def _get_sample_offers(self):
        """Realistic sample offers for testing."""
        return [
            {
                "id": "10492",
                "title": "Claim a $100 Walmart eGift Card (US Only)",
                "description": "Enter your email & answer 3 shopping habit questions to enter.",
                "payout": "2.40",
                "epc": "$0.38",
                "epc_val": 0.38,
                "country": "US",
                "type": "Email Submit / Survey",
                "link": "https://www.cpagrip.com/show.php?l=0&u=demo&id=10492"
            },
            {
                "id": "10811",
                "title": "Playtester: Test New Mobile Games on iOS/Android",
                "description": "Download and reach level 5 to earn rewards points.",
                "payout": "3.80",
                "epc": "$0.29",
                "epc_val": 0.29,
                "country": "US",
                "type": "App Install / Rewards",
                "link": "https://www.cpagrip.com/show.php?l=0&u=demo&id=10811"
            },
            {
                "id": "10123",
                "title": "Get a $50 DoorDash Voucher with Survey",
                "description": "Valid for US food delivery enthusiasts.",
                "payout": "1.95",
                "epc": "$0.22",
                "epc_val": 0.22,
                "country": "US",
                "type": "Pin / Email Submit",
                "link": "https://www.cpagrip.com/show.php?l=0&u=demo&id=10123"
            }
        ]
