import os
import requests
import json

class OfferEngine:
    def __init__(self, user_id=None, api_key=None, min_epc=0.10, target_geo="US"):
        self.user_id = user_id or os.getenv("CPAGRIP_USER_ID")
        self.api_key = api_key or os.getenv("CPAGRIP_KEY")
        self.min_epc = float(min_epc or os.getenv("MIN_EPC", 0.10))
        self.target_geo = target_geo or os.getenv("TARGET_GEO", "US")

    def fetch_offers(self):
        """Fetches live offers from CPAGrip API with automatic fallback to sample data."""
        if self.user_id and self.api_key and self.user_id != "your_cpagrip_user_id":
            url = f"https://www.cpagrip.com/common/offer_feed_json.php?user_id={self.user_id}&key={self.api_key}&showall=yes"
            try:
                response = requests.get(url, timeout=20)
                data = response.json()
                raw_offers = data.get("offers", [])
                if raw_offers:
                    print(f"📊 [CPAGrip API] Successfully fetched {len(raw_offers)} total network offers!")
                    return self._filter_and_rank(raw_offers)
            except Exception as e:
                print(f"[!] Warning: Could not fetch live CPAGrip feed ({e}). Using sample offers.")

        # Fallback realistic sample US offers
        return self._get_sample_offers()

    def _filter_and_rank(self, offers):
        """Filters by target country and sorts by EPC / payout descending."""
        filtered = []
        for o in offers:
            geo = o.get("accepted_countries") or o.get("country", "")
            
            # Extract EPC (can be netepc or epc)
            epc_raw = o.get("netepc") or o.get("epc", 0)
            try:
                epc = float(epc_raw)
            except (ValueError, TypeError):
                epc = 0.0

            # Extract Payout
            try:
                payout = float(o.get("payout", 1.50))
            except (ValueError, TypeError):
                payout = 1.50

            if self.target_geo in geo:
                filtered.append({
                    "id": str(o.get("offer_id", "")),
                    "title": o.get("title", "Exclusive US Reward"),
                    "description": o.get("description", "Complete quick entry to qualify."),
                    "payout": f"{payout:.2f}",
                    "epc": f"${epc:.3f}",
                    "epc_val": epc,
                    "payout_val": payout,
                    "country": geo,
                    "type": o.get("category") or o.get("type", "Email/Zip Submit"),
                    "link": o.get("offerlink", "#")
                })

        if not filtered:
            print(f"[!] No {self.target_geo} offers found. Using top global offers.")
            return self._get_sample_offers()

        # Sort primarily by EPC, and secondarily by Payout
        sorted_offers = sorted(filtered, key=lambda x: (x["epc_val"], x["payout_val"]), reverse=True)
        return sorted_offers[:5]

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
