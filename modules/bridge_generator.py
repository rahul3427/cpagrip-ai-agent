import os
import urllib.parse

class BridgeGenerator:
    def __init__(self, base_url="https://rahul3427.github.io/rewards-hub/"):
        self.base_url = base_url.rstrip("/") + "/"

    def generate_safe_url(self, direct_offer_url, offer_title="Special US Reward"):
        """Generates a clean bridge URL with encoded parameters."""
        encoded_target = urllib.parse.quote(direct_offer_url, safe="")
        encoded_title = urllib.parse.quote(offer_title, safe="")
        return f"{self.base_url}?target={encoded_target}&title={encoded_title}"
