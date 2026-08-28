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
        """Fetches offers from CPAGrip API with automatic fallback to high-value mock data for testing."""
        if self.user_id and self.api_key and self.user_id != "your_cpagrip_user_id":
            url = f"https://www.cpagrip.com/common/offer_feed_json.php?user_id={self.user_id}&key={self.api_key}&country=US&showall=yes&tracking_id="
            try:
                response = requests.get(url, timeout=15)
                data = response.json()
                raw_offers = data.get("offers", [])
                if raw_offers:
                    print(f"📊 [CPAGrip API] Found {len(raw_offers)} live offers from your account!")
                    return self._filter_and_rank(raw_offers)
                else:
                    print(f"[!] CPAGrip returned 0 offers. Checking without filters...")
                    url_all = f"https://www.cpagrip.com/common/offer_feed_json.php?user_id={self.user_id}&key={self.api_key}&showall=yes"
                    data_all = requests.get(url_all, timeout=15).json()
                    raw_all = data_all.get("offers", [])
                    if raw_all:
                        return self._filter_and_rank(raw_all)
            except Exception as e:
                print(f"[!] Warning: Could not fetch live CPAGrip feed ({e}). Using sample offers.")

        # Fallback realistic sample US offers for instant testing
        return self._get_sample_offers()

    def _filter_and_rank(self, offers):
        """Filters by target country and sorts by EPC descending."""
        filtered = []
        for o in offers:
            geo = o.get("country", "")
            try:
                epc = float(o.get("epc", 0))
            except (ValueError, TypeError):
                epc = 0.0

            if self.target_geo in geo and epc >= self.min_epc:
                filtered.append({
                    "id": o.get("offer_id", ""),
                    "title": o.get("title", "Exclusive US Reward"),
                    "description": o.get("description", "Complete short survey to qualify."),
                    "payout": str(o.get("payout", "1.75")),
                    "epc": f"${epc:.2f}",
                    "epc_val": epc,
                    "country": geo,
                    "type": o.get("type", "Email/Zip Submit"),
                    "link": o.get("offerlink", "#")
                })

        sorted_offers = sorted(filtered, key=lambda x: x["epc_val"], reverse=True)
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
