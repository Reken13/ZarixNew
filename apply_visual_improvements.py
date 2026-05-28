#!/usr/bin/env python3
"""Apply visual improvements to all 8 service pages."""

import re, os

BASE = '/home/user/ZarixNew'

# Page-specific data
pages = {
    'criacao-websites-aveiro.html': {
        'stats': ['Em <strong>5 dias</strong> online', '<strong>SEO</strong> incluído', 'Aveiro & Região'],
        'icons': ['🏢', '🍽️', '🎯', '🛒'],
    },
    'websites-para-restaurantes.html': {
        'stats': ['Menu <strong>online</strong>', '<strong>Reservas</strong> integradas', 'SEO para restaurantes'],
        'icons': ['📋', '📅', '📸', '📍', '🗺️', '📱'],
    },
    'suporte-it-restaurantes-aveiro.html': {
        'stats': ['Resposta em <strong>4h</strong>', 'Wi-Fi <strong>profissional</strong>', 'POS & TPAs'],
        'icons': ['📶', '💳', '🖥️', '💾', '🔧', '🚨'],
    },
    'suporte-it-aveiro.html': {
        'stats': ['<strong>+50</strong> empresas', 'Resposta em <strong>4h</strong>', 'Contrato mensal'],
        'icons': ['🏢', '🏪', '🤝', '🍴'],
    },
    'redes-wifi-empresas-aveiro.html': {
        'stats': ['Wi-Fi de <strong>alta potência</strong>', '<strong>Sem</strong> cabos visíveis', 'Gestão remota'],
        'icons': ['🍽️', '🏢', '🏪', '🏨'],
    },
    'ciberseguranca-pme.html': {
        'stats': ['<strong>RGPD</strong> compliant', 'Backups <strong>automáticos</strong>', '24/7 monitorização'],
        'icons': ['🛡️', '💾', '⚖️', '👥', '🔐', '👁️'],
    },
    'chatbots-ia-whatsapp.html': {
        'stats': ['WhatsApp <strong>Business</strong>', '<strong>IA</strong> avançada', 'Sem código'],
        'icons': ['🍽️', '📅', '🏪', '💬'],
    },
    'manutencao-informatica-aveiro.html': {
        'stats': ['Resposta <strong>rápida</strong>', '<strong>Todas</strong> as marcas', 'Aveiro'],
        'icons': ['🔍', '🔧', '⚡', '⬆️'],
    },
}

# New improved page-specific CSS (minified, replaces old block)
NEW_CSS = (
    '.page-hero{padding:140px 24px 80px;background:linear-gradient(180deg,rgba(56,189,248,.04) 0%,transparent 60%);'
    'text-align:center;border-bottom:1px solid var(--border);position:relative;overflow:hidden}'
    '.page-hero::before{content:\'\';position:absolute;top:-100px;left:50%;transform:translateX(-50%);'
    'width:900px;height:700px;background:radial-gradient(ellipse at center,rgba(56,189,248,.07) 0%,transparent 65%);'
    'pointer-events:none;z-index:0}'
    '.page-hero .wrap{position:relative;z-index:1}'
    '.page-breadcrumb{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--text-3);margin-bottom:20px;justify-content:center}'
    '.page-breadcrumb a{color:var(--text-3);transition:color .2s}'
    '.page-breadcrumb a:hover{color:var(--accent)}'
    '.page-hero h1{font-size:clamp(30px,5vw,52px);font-weight:800;letter-spacing:-.03em;margin-bottom:18px}'
    '.page-hero .intro{font-size:17px;color:var(--text-2);max-width:620px;margin:0 auto 32px;line-height:1.72}'
    '.hero-stats{display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:6px 14px;margin-bottom:28px}'
    '.hero-stat{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:500;color:var(--text-2);'
    'padding:5px 13px;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:50px}'
    '.hero-stat strong{color:var(--text);font-weight:700}'
    '.hero-trust{margin-top:12px;font-size:12px;color:var(--text-3);display:flex;align-items:center;justify-content:center;gap:5px}'
    '.hero-trust::before{content:\'✓\';color:var(--green);font-weight:700;font-size:13px}'
    '.g-text{background:linear-gradient(135deg,var(--accent) 0%,var(--accent-hi) 100%);-webkit-background-clip:text;'
    '-webkit-text-fill-color:transparent;background-clip:text}'
    '.svc-section{padding:var(--sp)}'
    '.svc-section.alt{background:linear-gradient(180deg,transparent,rgba(56,189,248,.022) 40%,rgba(16,185,129,.008) 70%,transparent)}'
    '.feat-list{list-style:none;display:flex;flex-direction:column;gap:12px}'
    '.feat-list li{display:flex;align-items:flex-start;gap:12px;font-size:15px;color:var(--text-2);line-height:1.65}'
    '.feat-list li strong{color:var(--text);font-weight:600}'
    ".feat-list li::before{content:'';flex-shrink:0;width:18px;height:18px;margin-top:2px;border-radius:50%;background:var(--accent-glow);border:1px solid var(--border-a);"
    'background-image:url("data:image/svg+xml,%3Csvg viewBox=%270 0 16 16%27 fill=%27none%27 xmlns=%27http://www.w3.org/2000/svg%27%3E%3Cpath d=%27M3.5 8l3 3 6-6.5%27 stroke=%27%2338bdf8%27 stroke-width=%271.5%27 stroke-linecap=%27round%27 stroke-linejoin=%27round%27/%3E%3C%2Fsvg%3E");'
    'background-repeat:no-repeat;background-size:12px;background-position:center}'
    '.info-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-top:32px}'
    '.info-card{background:var(--bg-s);border:1px solid var(--border);border-radius:var(--r-lg);padding:26px;'
    'transition:border-color .3s,transform .3s var(--ease-out)}'
    '.info-card:hover{border-color:var(--border-a);transform:translateY(-4px)}'
    '.info-icon{width:42px;height:42px;border-radius:10px;background:var(--accent-glow);border:1px solid var(--border-a);'
    'display:flex;align-items:center;justify-content:center;margin-bottom:14px;font-size:22px;line-height:1}'
    '.info-card h3{font-size:15px;font-weight:700;color:var(--text);margin-bottom:8px}'
    '.info-card p{font-size:13.5px;color:var(--text-2);line-height:1.65}'
    '.proc-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:36px;position:relative}'
    ".proc-grid::before{content:'';position:absolute;top:44px;left:calc(33.33% - 4px);right:calc(33.33% - 4px);"
    'height:1px;background:var(--border-a);pointer-events:none;z-index:0}'
    '.proc-card{text-align:center;background:var(--bg-s);border:1px solid var(--border);border-radius:var(--r-lg);'
    'padding:28px 20px;transition:border-color .3s,transform .3s var(--ease-out);position:relative;z-index:1}'
    '.proc-card:hover{border-color:var(--border-a);transform:translateY(-4px)}'
    '.proc-num{width:44px;height:44px;border-radius:50%;background:var(--accent-glow);border:1px solid var(--border-a);'
    'display:flex;align-items:center;justify-content:center;font-size:17px;font-weight:800;color:var(--accent);'
    'margin:0 auto 16px;letter-spacing:0;transition:background .2s,border-color .2s}'
    '.proc-card:hover .proc-num{background:rgba(56,189,248,.2);border-color:var(--accent)}'
    '.proc-card h3{font-size:16px;font-weight:700;color:var(--text);margin-bottom:8px}'
    '.proc-card p{font-size:13.5px;color:var(--text-2);line-height:1.65}'
    '.faq-wrap{max-width:760px;margin:0 auto;display:flex;flex-direction:column;gap:12px}'
    '.faq-item{background:var(--bg-s);border:1px solid var(--border);border-radius:var(--r);overflow:hidden;transition:border-color .2s}'
    '.faq-item.open{border-color:var(--border-a)}'
    '.faq-q{width:100%;text-align:left;padding:18px 22px;background:none;border:none;font-family:var(--font-h);'
    'font-size:15px;font-weight:600;color:var(--text);cursor:pointer;display:flex;align-items:center;'
    'justify-content:space-between;gap:16px;transition:color .2s}'
    '.faq-item.open .faq-q{color:var(--accent)}'
    '.faq-q:hover{color:var(--accent)}'
    '.faq-icon{width:22px;height:22px;border-radius:50%;border:1px solid var(--border-a);display:flex;align-items:center;'
    'justify-content:center;flex-shrink:0;transition:transform .25s,background .2s;color:var(--accent);font-size:16px;line-height:1}'
    '.faq-item.open .faq-icon{transform:rotate(45deg);background:var(--accent-glow)}'
    '.faq-a{max-height:0;overflow:hidden;transition:max-height .35s var(--ease-out)}'
    '.faq-item.open .faq-a{max-height:400px}'
    '.faq-a p{padding:0 22px 18px;font-size:14px;color:var(--text-2);line-height:1.72}'
    '@media(max-width:720px){.proc-grid{grid-template-columns:1fr}.proc-grid::before{display:none}}'
)

OLD_CSS_START = '.page-hero{padding:140px 24px 80px'
OLD_CSS_END   = '@media(max-width:720px){.proc-grid{grid-template-columns:1fr}}'

TRUST_HTML = '      <p class="hero-trust">Resposta em menos de 24h · Orçamento sem compromisso</p>'

# Exact string that marks the end of the hero buttons section
HERO_END_MARKER = '      </div>\n    </div>\n  </section>'

def make_stats_html(stats):
    items = ''.join(f'<span class="hero-stat">{s}</span>' for s in stats)
    return f'      <div class="hero-stats">{items}</div>'

def apply_improvements(filename, data):
    path = os.path.join(BASE, filename)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    original_len = len(html)

    # 1. Replace page-specific CSS block
    start_idx = html.find(OLD_CSS_START)
    end_idx   = html.find(OLD_CSS_END)
    if start_idx == -1 or end_idx == -1:
        print(f'  WARNING: CSS markers not found')
    else:
        end_idx += len(OLD_CSS_END)
        html = html[:start_idx] + NEW_CSS + html[end_idx:]
        print(f'  CSS replaced ✓')

    # 2. proc-num: "Passo 0X" → "0X"
    for i in ('01', '02', '03'):
        html = html.replace(f'<div class="proc-num">Passo {i}</div>', f'<div class="proc-num">{i}</div>')
    print(f'  proc-num updated ✓')

    # 3. Add hero-stats between intro and CTA buttons
    stats_marker = '      <div style="display:flex;gap:14px;justify-content:center;flex-wrap:wrap">'
    if stats_marker in html and '<div class="hero-stats">' not in html:
        stats_html = make_stats_html(data['stats'])
        html = html.replace(stats_marker, stats_html + '\n' + stats_marker, 1)
        print(f'  hero-stats added ✓')
    else:
        print(f'  hero-stats: marker not found or already added')

    # 4. Add trust text after CTA buttons, before end of hero wrap
    if HERO_END_MARKER in html and 'hero-trust' not in html:
        html = html.replace(HERO_END_MARKER, TRUST_HTML + '\n' + HERO_END_MARKER, 1)
        print(f'  hero-trust added ✓')
    else:
        print(f'  hero-trust: marker not found or already added')

    # 5. Add icons to info-cards (sequential, one per card)
    icons = data['icons']
    icon_idx = 0

    def add_icon_to_card(m):
        nonlocal icon_idx
        card_open = m.group(1)   # <div class="info-card r dN">
        nl_indent = m.group(2)   # \n
        h3_tag    = m.group(3)   # <h3>Title</h3>
        icon = icons[icon_idx] if icon_idx < len(icons) else '📌'
        icon_idx += 1
        return f'{card_open}{nl_indent}<div class="info-icon">{icon}</div>{nl_indent}{h3_tag}'

    if '<div class="info-icon">' not in html:
        html = re.sub(
            r'(<div class="info-card[^"]*"[^>]*>)(\n\s+)(<h3>[^<]+</h3>)',
            add_icon_to_card,
            html
        )
        print(f'  info icons added ({icon_idx} icons) ✓')
    else:
        print(f'  info icons: already present')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  Saved ✓ (was {original_len} chars, now {len(html)} chars)')

for filename, data in pages.items():
    print(f'\n{filename}')
    apply_improvements(filename, data)

print('\n=== All done! ===')
