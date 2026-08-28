import os
import urllib.parse

class BridgeGenerator:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("BRIDGE_BASE_URL", "https://rahul3427.github.io/rewards-hub/")

    def create_safe_link(self, offer_title, offer_id, direct_cpa_url=None):
        """Creates a clean, short, anti-ban bridge URL using offer ID."""
        safe_title = urllib.parse.quote_plus(offer_title[:25])
        # Short, ultra-clean bridge URL
        if offer_id:
            return f"{self.base_url.rstrip('/')}/?id={offer_id}&title={safe_title}"
        
        encoded_target = urllib.parse.quote_plus(direct_cpa_url or "")
        return f"{self.base_url.rstrip('/')}/?target={encoded_target}&title={safe_title}"

    def generate_safe_url(self, direct_offer_url, offer_title="Special US Reward", offer_id=None):
        return self.create_safe_link(offer_title, offer_id, direct_offer_url)
