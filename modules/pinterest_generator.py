import os
from PIL import Image, ImageDraw, ImageFont

class PinterestGenerator:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "..", "generated_pins")
        os.makedirs(self.output_dir, exist_ok=True)

    def create_pin_image(self, offer_title, payout, category="US REWARD"):
        """Generates a professional 1000x1500 Pinterest Pin image."""
        width, height = 1000, 1500
        
        # Create gradient background
        base = Image.new('RGB', (width, height), color=(15, 23, 42))
        draw = ImageDraw.Draw(base)

        # Draw smooth modern dark-blue/violet gradient
        for y in range(height):
            r = int(15 + (45 - 15) * (y / height))
            g = int(23 + (25 - 23) * (y / height))
            b = int(42 + (80 - 42) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Draw decorative card container
        card_margin = 60
        card_radius = 40
        draw.rounded_rectangle(
            [(card_margin, 120), (width - card_margin, height - 140)],
            radius=card_radius,
            fill=(30, 41, 59),
            outline=(59, 130, 246),
            width=4
        )

        # Top Badge
        badge_w, badge_h = 420, 60
        badge_x = (width - badge_w) // 2
        draw.rounded_rectangle(
            [(badge_x, 180), (badge_x + badge_w, 180 + badge_h)],
            radius=30,
            fill=(16, 185, 129)
        )
        draw.text((badge_x + 35, 195), "⭐ VERIFIED US PROGRAM 2026", fill=(255, 255, 255))

        # Main Headline
        draw.text((100, 320), "MONEY HACK", fill=(56, 189, 248))
        
        # Format offer title with line wrapping
        words = offer_title.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 18:
                lines.append(" ".join(current_line))
                current_line = []
        if current_line:
            lines.append(" ".join(current_line))

        y_text = 420
        for line in lines[:4]:
            draw.text((100, y_text), line.upper(), fill=(255, 255, 255))
            y_text += 90

        # Subtitle / Perk
        draw.text((100, 840), "✨ 2-Minute Quick Setup", fill=(148, 163, 184))
        draw.text((100, 910), "📱 Compatible with iOS & Android", fill=(148, 163, 184))
        draw.text((100, 980), "🇺🇸 Available for All 50 US States", fill=(148, 163, 184))

        # Big CTA Button
        btn_y = 1100
        btn_w, btn_h = 700, 110
        btn_x = (width - btn_w) // 2
        draw.rounded_rectangle(
            [(btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h)],
            radius=25,
            fill=(37, 99, 235)
        )
        draw.text((btn_x + 120, btn_y + 35), "TAP TO CLAIM ACCESS ➔", fill=(255, 255, 255))

        # Save image
        safe_filename = "".join([c if c.isalnum() else "_" for c in offer_title[:20]]) + ".png"
        filepath = os.path.join(self.output_dir, safe_filename)
        base.save(filepath, "PNG")
        print(f"🎨 [Pinterest Engine] Generated Pin Graphic: {filepath}")
        return filepath
