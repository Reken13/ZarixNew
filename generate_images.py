#!/usr/bin/env python3
"""Generate og-image.png, favicon.ico, favicon-192.png, apple-touch-icon.png for Zarix."""

from PIL import Image, ImageDraw, ImageFont
import math, os

FONT_BOLD    = '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
FONT_REGULAR = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
OUT = '/home/user/ZarixNew'

# ─── colours ────────────────────────────────────────────────────────────────
BG      = (9, 9, 15)
ACCENT  = (56, 189, 248)
ACCENT2 = (125, 211, 252)
GREEN   = (16, 185, 129)
TEXT    = (241, 245, 249)
TEXT2   = (148, 163, 184)
TEXT3   = (71, 85, 105)
BORDER  = (255, 255, 255, 18)

# ─── helpers ────────────────────────────────────────────────────────────────
def rounded_rect(draw, xy, radius, fill, outline=None, outline_width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill,
                           outline=outline, width=outline_width)

def draw_glow(img, cx, cy, r, color, alpha=40):
    """Radial glow painted directly onto img."""
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    for i in range(6, 0, -1):
        a = int(alpha * (i / 6) ** 2)
        cr = int(r * i / 6)
        d = ImageDraw.Draw(overlay)
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr],
                  fill=(*color, a))
    img.alpha_composite(overlay)

# ════════════════════════════════════════════════════════════════════════════
# 1. OG IMAGE  1200 × 630
# ════════════════════════════════════════════════════════════════════════════
W, H = 1200, 630
img = Image.new('RGBA', (W, H), (*BG, 255))

# Background grid lines
grid = ImageDraw.Draw(img)
for x in range(0, W, 60):
    grid.line([(x, 0), (x, H)], fill=(255, 255, 255, 6), width=1)
for y in range(0, H, 60):
    grid.line([(0, y), (W, y)], fill=(255, 255, 255, 6), width=1)

# Top-left glow (accent blue)
draw_glow(img, int(W * 0.18), int(H * 0.22), 380, ACCENT, alpha=28)
# Bottom-right glow (green)
draw_glow(img, int(W * 0.82), int(H * 0.78), 260, GREEN, alpha=18)

d = ImageDraw.Draw(img)

# ── left accent bar ──────────────────────────────────────────────────────────
bar_x = 96
for i, color in enumerate([(*ACCENT, 255), (*ACCENT2, 180), (*GREEN, 120)]):
    d.rectangle([bar_x, 160 + i * 18, bar_x + 4, 160 + i * 18 + 10], fill=color)

# ── "Zarix" logotype ─────────────────────────────────────────────────────────
logo_font = ImageFont.truetype(FONT_BOLD, 112)
logo_x, logo_y = 112, 142

# Draw "Zari" in white, "x" in accent
zari = "Zari"
x_char = "x"
bbox_zari = logo_font.getbbox(zari)
w_zari = bbox_zari[2] - bbox_zari[0]

d.text((logo_x, logo_y), zari, font=logo_font, fill=TEXT)
d.text((logo_x + w_zari, logo_y), x_char, font=logo_font, fill=ACCENT)

# ── tagline ──────────────────────────────────────────────────────────────────
tag_font = ImageFont.truetype(FONT_REGULAR, 28)
d.text((114, logo_y + 120), "Suporte IT e Websites para PMEs em Aveiro",
       font=tag_font, fill=TEXT2)

# ── service pills ────────────────────────────────────────────────────────────
pill_font = ImageFont.truetype(FONT_BOLD, 16)
services = ["Redes Wi-Fi", "Cibersegurança", "Chatbots IA", "Websites", "Suporte IT"]
px = 114
py = logo_y + 180
for svc in services:
    bbox = pill_font.getbbox(svc)
    tw = bbox[2] - bbox[0]
    pad = 14
    pill_w = tw + pad * 2
    pill_h = 34
    rounded_rect(d, [px, py, px + pill_w, py + pill_h],
                 radius=17,
                 fill=(56, 189, 248, 18),
                 outline=(*ACCENT, 55),
                 outline_width=1)
    d.text((px + pad, py + 9), svc, font=pill_font, fill=ACCENT2)
    px += pill_w + 10

# ── bottom strip ─────────────────────────────────────────────────────────────
strip_y = H - 72
d.rectangle([0, strip_y, W, H], fill=(255, 255, 255, 8))
strip_font = ImageFont.truetype(FONT_REGULAR, 18)
d.text((114, strip_y + 22), "zarix.site  ·  Aveiro, Portugal  ·  +351 967 608 772",
       font=strip_font, fill=TEXT3)

# ── right decorative block ───────────────────────────────────────────────────
dec_x = 860
dec_font_big  = ImageFont.truetype(FONT_BOLD, 52)
dec_font_small = ImageFont.truetype(FONT_REGULAR, 16)

for i, (val, label, color) in enumerate([
    ("5★", "Avaliação média", ACCENT),
    ("24h", "Resposta garantida", GREEN),
    ("+50", "Empresas servidas", ACCENT2),
]):
    card_y = 120 + i * 140
    rounded_rect(d, [dec_x, card_y, dec_x + 220, card_y + 110],
                 radius=12,
                 fill=(255, 255, 255, 6),
                 outline=(255, 255, 255, 15),
                 outline_width=1)
    d.text((dec_x + 22, card_y + 14), val, font=dec_font_big, fill=color)
    d.text((dec_x + 22, card_y + 74), label, font=dec_font_small, fill=TEXT3)

# save
og_path = os.path.join(OUT, 'og-image.png')
img.convert('RGB').save(og_path, 'PNG', optimize=True)
print(f'✓ og-image.png saved ({W}×{H}px)')


# ════════════════════════════════════════════════════════════════════════════
# 2. FAVICON BASE  512 × 512  →  resize to needed sizes
# ════════════════════════════════════════════════════════════════════════════
SZ = 512
fav = Image.new('RGBA', (SZ, SZ), (0, 0, 0, 0))

# rounded-square background
fd = ImageDraw.Draw(fav)
fd.rounded_rectangle([0, 0, SZ, SZ], radius=int(SZ * 0.22), fill=(*BG, 255))

# subtle inner glow
draw_glow(fav, SZ // 2, SZ // 2, int(SZ * 0.6), ACCENT, alpha=35)

# "Z" lettermark — drawn as thick stroked path
fd = ImageDraw.Draw(fav)
z_font = ImageFont.truetype(FONT_BOLD, int(SZ * 0.64))
bbox = z_font.getbbox("Z")
zw = bbox[2] - bbox[0]
zh = bbox[3] - bbox[1]
zx = (SZ - zw) // 2 - bbox[0]
zy = (SZ - zh) // 2 - bbox[1]

# shadow / glow pass
for offset in range(8, 0, -2):
    a = int(100 * (offset / 8) ** 2)
    fd.text((zx + offset, zy + offset), "Z", font=z_font, fill=(*ACCENT, a))
# main Z
fd.text((zx, zy), "Z", font=z_font, fill=(*ACCENT, 255))

# green dot  (like the logo-i dot in the site)
dot_r = int(SZ * 0.055)
dot_cx = int(SZ * 0.64)
dot_cy = int(SZ * 0.18)
fd.ellipse([dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
           fill=(*GREEN, 255))

# ── save at required sizes ─────────────────────────────────────────────────
def save_favicon(size, filename):
    resized = fav.resize((size, size), Image.LANCZOS)
    path = os.path.join(OUT, filename)
    resized.save(path, 'PNG')
    print(f'✓ {filename} saved ({size}×{size}px)')

save_favicon(32,  'favicon-32.png')
save_favicon(192, 'favicon-192.png')
save_favicon(180, 'apple-touch-icon.png')

# favicon.ico  (multi-size: 16, 32, 48)
ico_sizes = [(16, 16), (32, 32), (48, 48)]
ico_images = [fav.resize(s, Image.LANCZOS).convert('RGBA') for s in ico_sizes]
ico_path = os.path.join(OUT, 'favicon.ico')
ico_images[0].save(ico_path, format='ICO',
                   sizes=ico_sizes,
                   append_images=ico_images[1:])
print(f'✓ favicon.ico saved (16/32/48px multi-size)')

print('\nAll images generated successfully!')
