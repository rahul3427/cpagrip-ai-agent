import os
import math
from PIL import Image, ImageDraw, ImageFont

class PinterestGenerator:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "..", "generated_pins")
        os.makedirs(self.output_dir, exist_ok=True)

    def create_pin_image(self, offer_title, payout, category="US REWARD"):
        """Generates an ultra-premium, high-converting 1000x1500 Pinterest Pin graphic."""
        width, height = 1000, 1500
        
        # 1. Base Gradient (Deep Indigo to Rich Violet)
        base = Image.new('RGB', (width, height), color=(15, 17, 36))
        draw = ImageDraw.Draw(base, 'RGBA')

        for y in range(height):
            ratio = y / height
            # Smooth transition from Vibrant Royal Blue (26, 54, 138) to Deep Violet (15, 17, 36)
            r = int(26 * (1 - ratio) + 15 * ratio)
            g = int(54 * (1 - ratio) + 17 * ratio)
            b = int(138 * (1 - ratio) + 55 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

        # 2. Glowing Ambient Light Circles (Modern Bokeh Aesthetic)
        draw.ellipse([(-100, -100), (500, 500)], fill=(59, 130, 246, 55))
        draw.ellipse([(width - 400, height - 600), (width + 200, height)], fill=(139, 92, 246, 50))
        draw.ellipse([(100, 600), (900, 1200)], fill=(30, 58, 138, 40))

        # 3. Glassmorphism Hero Card
        card_x1, card_y1 = 60, 100
        card_x2, card_y2 = width - 60, height - 100
        
        # Card shadow
        draw.rounded_rectangle(
            [(card_x1 + 10, card_y1 + 15), (card_x2 + 10, card_y2 + 15)],
            radius=40,
            fill=(0, 0, 0, 90)
        )
        # Card background (Translucent Slate Glass)
        draw.rounded_rectangle(
            [(card_x1, card_y1), (card_x2, card_y2)],
            radius=40,
            fill=(17, 24, 39, 230),
            outline=(99, 102, 241, 160),
            width=3
        )

        # 4. Top Badge: Verified US Program & 5-Star Rating
        badge_w, badge_h = 480, 56
        bx1 = (width - badge_w) // 2
        draw.rounded_rectangle(
            [(bx1, 150), (bx1 + badge_w, 150 + badge_h)],
            radius=28,
            fill=(16, 185, 129, 240),
            outline=(255, 255, 255, 100),
            width=2
        )
        draw.text((bx1 + 45, 165), "★ ★ ★ ★ ★  VERIFIED US PROGRAM", fill=(255, 255, 255, 255))

        # 5. Category / Hook Subheader
        draw.text((100, 260), "EXCLUSIVE OPPORTUNITY • 2026", fill=(56, 189, 248, 255))

        # 6. Big Catchy Benefit Title
        words = offer_title.split()
        lines = []
        curr = []
        for w in words:
            curr.append(w)
            if len(" ".join(curr)) > 15:
                lines.append(" ".join(curr))
                curr = []
        if curr:
            lines.append(" ".join(curr))

        # Render Main Title Box with Glowing Left Accent Bar
        ty = 340
        draw.rounded_rectangle([(90, ty), (98, ty + min(len(lines) * 95, 380))], radius=4, fill=(236, 72, 153, 255))

        for line in lines[:4]:
            draw.text((120, ty), line.upper(), fill=(255, 255, 255, 255))
            ty += 90

        # 7. Visual Perk Cards (Feature Pills)
        perks = [
            ("✔  100% Free Instant Download / Access", (34, 197, 94)),
            ("✔  Fast 2-Minute Setup on Mobile / PC", (56, 189, 248)),
            ("✔  Active for All 50 US States", (168, 85, 247))
        ]
        
        py = 780
        for text, color in perks:
            draw.rounded_rectangle(
                [(100, py), (width - 100, py + 75)],
                radius=20,
                fill=(30, 41, 59, 200),
                outline=(*color, 120),
                width=2
            )
            draw.text((130, py + 24), text, fill=(241, 245, 249, 255))
            py += 95

        # 8. High-Converting Bottom Action Button
        btn_w, btn_h = 720, 115
        btn_x = (width - btn_w) // 2
        btn_y = 1140
        
        # Button Glow / Shadow
        draw.rounded_rectangle(
            [(btn_x, btn_y + 8), (btn_x + btn_w, btn_y + btn_h + 8)],
            radius=30,
            fill=(30, 58, 138, 140)
        )
        # Main Button (Vibrant Coral/Blue Gradient Accent)
        draw.rounded_rectangle(
            [(btn_x, btn_y), (btn_x + btn_w, btn_y + btn_h)],
            radius=30,
            fill=(37, 99, 235, 255),
            outline=(255, 255, 255, 180),
            width=2
        )
        draw.text((btn_x + 140, btn_y + 40), "👉  TAP HERE TO CLAIM ACCESS", fill=(255, 255, 255, 255))

        # Footer Trust Note
        draw.text((width // 2 - 160, 1310), "🔒 Safe & Verified Partner Link", fill=(148, 163, 184, 200))

        # Save Final Image
        safe_filename = "".join([c if c.isalnum() else "_" for c in offer_title[:20]]) + ".png"
        filepath = os.path.join(self.output_dir, safe_filename)
        base.save(filepath, "PNG")
        print(f"🎨 [Pinterest Engine] Generated Premium Pin Graphic: {filepath}")
        return filepath
