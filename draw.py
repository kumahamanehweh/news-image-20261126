#!/usr/bin/env python3
"""Draw the news-image-20261126 front page: a dense one-page newspaper
summing up Thursday 26 November 2026. Run locally at build time only;
the grader never runs this file. It writes entry.png (1024x1024, <=1 MiB)."""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 219)
INK = (17, 17, 17)
RED = (176, 30, 36)
DARKRED = (140, 20, 26)
NAVY = (27, 42, 74)
BLUE = (36, 84, 160)
GOLD = (201, 162, 39)
GREEN = (46, 125, 50)
TEAL = (0, 110, 110)
PURPLE = (98, 60, 140)
ORANGE = (198, 102, 20)
GREY = (90, 84, 70)
LIGHTBLUE = (191, 217, 232)
LAND = (232, 217, 168)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        base = "DejaVuSerif.ttf" if name.startswith("DejaVuSerif") else "DejaVuSans.ttf"
        return ImageFont.truetype(os.path.join(FONT_DIR, base), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: font("DejaVuSans-Oblique.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)


def wrap(text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, fnt, fill, maxw, lh):
    for ln in wrap(text, fnt, maxw):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centre(y, text, fnt, fill):
    d.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def hline(y, fill=INK, wdt=2):
    d.line([(14, y), (1010, y)], fill=fill, width=wdt)


def badge(x, y, label, fill):
    fnt = SANS_B(8)
    tw = d.textlength(label, font=fnt)
    d.rounded_rectangle([x, y, x + tw + 10, y + 12], radius=2, fill=fill)
    d.text((x + 5, y + 1), label, font=fnt, fill=(255, 255, 255))
    return tw + 10


# ---------------------------------------------------------------- top of page
d.text((14, 5), "THE WORLD IN ONE DAY", font=SANS_B(12), fill=RED)
d.text((1010, 5), "THURSDAY EDITION", font=SANS_B(12), fill=INK, anchor="ra")
centre(24, "45 STORIES  ·  4 REGIONS  ·  10 FIELDS  ·  ALL FROM THIS THURSDAY",
       SANS_B(13), RED)
hline(40)
centre(46, "Thursday 26 November 2026", SERIF_B(48), INK)
centre(100, "\u201cAsia steadies after the rout, Seoul hikes rates, and Geneva "
             "plays Game 3 with the score locked 1\u20131.\u201d",
       SERIF_I(15), DARKRED)
hline(120, RED, 2)

# ---------------------------------------------------------------- UTC strip
d.rectangle([14, 124, 1010, 142], fill=(255, 255, 255), outline=INK, width=1)
d.rectangle([14, 124, 150, 142], fill=RED)
d.text((20, 129), "THE DAY IN UTC", font=SANS_B(10), fill=(255, 255, 255))
utc_cells = [
    ("01:00 GMT", "BOK hikes to 3.25%"),
    ("early", "Kospi +2.1% rebound"),
    ("morning", "Oil holds near $95"),
    ("15:00 CET", "Chess Game 3, Geneva"),
    ("23:30 GMT", "Tokyo CPI due"),
]
cx = 156
for when, what in utc_cells:
    d.text((cx, 129), when, font=SANS_B(9), fill=RED)
    d.text((cx + 62, 129), what, font=SANS(9), fill=INK)
    cx += 171

# ---------------------------------------------------------------- big numbers
d.rectangle([14, 146, 1010, 178], fill=NAVY)
bigs = [
    ("+2.1%", "Kospi, early trade"),
    ("3.25%", "Bank of Korea rate"),
    ("1\u20131", "Chess score, Game 3 today"),
    ("~500,000", "Russian dead, own figures"),
    ("$122bn", "Petrobras plan"),
]
bx = 14
for num, lab in bigs:
    centre_bx = bx + 99
    d.text((centre_bx, 150), num, font=SANS_B(17), fill=GOLD, anchor="ma")
    d.text((centre_bx, 168), lab, font=SANS(8), fill=(255, 255, 255), anchor="ma")
    bx += 199

# ---------------------------------------------------------------- region strip
regs = [("ASIA 14", RED, 310), ("AMERICAS 14", BLUE, 300),
        ("EUROPE 9", PURPLE, 200), ("MIDDLE EAST 8", ORANGE, 186)]
rx = 14
for label, col, wd in regs:
    d.rectangle([rx, 182, rx + wd - 2, 196], fill=col)
    d.text((rx + wd // 2, 185), label, font=SANS_B(10),
           fill=(255, 255, 255), anchor="ma")
    rx += wd

# ---------------------------------------------------------------- leads
def lead_art(x, y, w, kind):
    d.rectangle([x, y, x + w, y + 56], outline=INK, width=1)
    if kind == "chart":
        d.rectangle([x, y, x + w, y + 56], fill=(232, 244, 232))
        pts = [(x + 12, y + 44), (x + 55, y + 40), (x + 95, y + 46),
               (x + 140, y + 34), (x + 185, y + 24), (x + 228, y + 12)]
        d.line(pts, fill=GREEN, width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GREEN)
        d.text((x + 8, y + 4), "+2.1% SEOUL", font=SANS_B(9), fill=GREEN)
        d.text((x + w - 8, y + 40), "+1.8% TOKYO", font=SANS_B(9),
               fill=GREEN, anchor="ra")
    elif kind == "bars":
        d.rectangle([x, y, x + w, y + 56], fill=NAVY)
        heights = [18, 24, 30, 38, 46]
        for i, hh in enumerate(heights):
            bx0 = x + 130 + i * 20
            d.rectangle([bx0, y + 52 - hh, bx0 + 14, y + 52], fill=(90, 140, 220))
        d.text((x + 10, y + 6), "3.25%", font=SANS_B(26), fill=GOLD)
        d.text((x + 10, y + 38), "HIGHEST SINCE OCT 2024", font=SANS_B(8),
               fill=(255, 255, 255))
    elif kind == "chess":
        d.rectangle([x, y, x + w, y + 56], fill=(240, 224, 178))
        sq = 7
        ox, oy = x + 150, y + 0
        for r in range(8):
            for c in range(8):
                if (r + c) % 2 == 0:
                    d.rectangle([ox + c * sq, oy + r * sq,
                                 ox + c * sq + sq, oy + r * sq + sq],
                                fill=(120, 80, 40))
        d.ellipse([ox + 2 * sq + 1, oy + 1 * sq + 1, ox + 3 * sq - 1,
                   oy + 2 * sq - 1], fill=INK)
        d.ellipse([ox + 5 * sq + 1, oy + 6 * sq + 1, ox + 6 * sq - 1,
                   oy + 7 * sq - 1], fill=(255, 255, 255), outline=INK)
        d.text((x + 10, y + 6), "1\u20131", font=SANS_B(26), fill=INK)
        d.text((x + 10, y + 38), "SCORE 1\u20131 \u00b7 GAME 3 TODAY",
               font=SANS_B(8), fill=INK)
    else:  # crosses
        d.rectangle([x, y, x + w, y + 56], fill=(30, 30, 34))
        for i in range(9):
            for j in range(4):
                px = x + 130 + i * 12
                py = y + 8 + j * 12
                d.line([(px - 3, py), (px + 3, py)], fill=(200, 200, 200), width=1)
                d.line([(px, py - 3), (px, py + 3)], fill=(200, 200, 200), width=1)
        d.text((x + 10, y + 6), "~500,000", font=SANS_B(22), fill=(255, 255, 255))
        d.text((x + 10, y + 38), "MILITARY DEAD, OWN FIGURES",
               font=SANS_B(8), fill=GOLD)


leads = [
    ("1 \u00b7 ASIA \u00b7 MARKETS", "Asia steadies: Kospi +2.1%, Nikkei +1.8% in early trade",
     "Seoul and Tokyo rebound after Wednesday's rout; Wall Street steadied, "
     "Dow +0.3%.", "chart",
     "SEOUL \u00b7 EARLY TRADE"),
    ("2 \u00b7 KOREA \u00b7 RATES", "Bank of Korea hikes to 3.25%, third rise this year",
     "Seoul lifts its key rate a quarter point, the highest since Oct 2024; "
     "growth up to 3.9%.",
     "bars", "SEOUL \u00b7 THIRD HIKE THIS YEAR"),
    ("3 \u00b7 GENEVA \u00b7 CHESS", "Game 3 today: Sindarov has White, 1\u20131",
     "Game 2 drawn in 20 moves in the London System. 14 games, first to 7\u00bd; "
     "rest day Friday.", "chess",
     "GENEVA \u00b7 $2.5m FUND"),
    ("4 \u00b7 UKRAINE \u00b7 WAR", "Russia's own toll: nearly 500,000 dead",
     "Moscow's own figures show almost half a million dead; with the "
     "missing, over 700,000.",
     "crosses", "UKRAINE WAR \u00b7 BBC"),
]
lx = 14
for kick, head, body, art, foot in leads:
    lead_art(lx, 200, 243, art)
    d.text((lx, 262), kick, font=SANS_B(9), fill=RED)
    para(lx, 276, head, SANS_B(13), INK, 243, 16)
    para(lx, 310, body, SANS(10), INK, 243, 12)
    lx += 251

# ---------------------------------------------------------------- smalls
def glyph(x, y, kind, col):
    d.rectangle([x, y, x + 195, y + 20], fill=col)
    cx, cy = x + 178, y + 10
    if kind == "flame":
        d.polygon([(cx, cy - 7), (cx + 5, cy + 2), (cx + 2, cy + 6),
                   (cx - 2, cy + 6), (cx - 5, cy + 2)], fill=(255, 255, 255))
    elif kind == "flag":
        d.line([(cx - 4, cy - 7), (cx - 4, cy + 7)], fill=(255, 255, 255), width=2)
        d.polygon([(cx - 4, cy - 7), (cx + 6, cy - 4), (cx - 4, cy - 1)],
                  fill=(255, 255, 255))
    elif kind == "scales":
        d.line([(cx, cy - 6), (cx, cy + 6)], fill=(255, 255, 255), width=2)
        d.line([(cx - 7, cy - 6), (cx + 7, cy - 6)], fill=(255, 255, 255), width=2)
        d.ellipse([cx - 9, cy + 1, cx - 4, cy + 6], outline=(255, 255, 255))
        d.ellipse([cx + 4, cy + 1, cx + 9, cy + 6], outline=(255, 255, 255))
    elif kind == "jet":
        d.polygon([(cx - 8, cy), (cx + 8, cy - 3), (cx + 8, cy + 3)],
                  fill=(255, 255, 255))
        d.line([(cx - 2, cy - 6), (cx - 2, cy + 6)], fill=(255, 255, 255), width=2)
    elif kind == "chip":
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=(255, 255, 255), width=2)
        d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 255, 255))
    elif kind == "temple":
        d.polygon([(cx, cy - 7), (cx + 7, cy), (cx - 7, cy)], fill=(255, 255, 255))
        d.rectangle([cx - 6, cy + 1, cx + 6, cy + 6], fill=(255, 255, 255))
    elif kind == "derrick":
        d.line([(cx - 5, cy + 6), (cx, cy - 7), (cx + 5, cy + 6)],
               fill=(255, 255, 255), width=2)
        d.line([(cx - 5, cy + 6), (cx + 5, cy + 6)], fill=(255, 255, 255), width=2)
    elif kind == "coins":
        d.ellipse([cx - 7, cy - 5, cx + 1, cy + 3], outline=(255, 255, 255), width=2)
        d.ellipse([cx - 1, cy - 1, cx + 7, cy + 7], outline=(255, 255, 255), width=2)
    elif kind == "shirt":
        d.polygon([(cx - 6, cy - 5), (cx + 6, cy - 5), (cx + 8, cy + 1),
                   (cx + 4, cy + 1), (cx + 4, cy + 7), (cx - 4, cy + 7),
                   (cx - 4, cy + 1), (cx - 8, cy + 1)], fill=(255, 255, 255))
    else:  # shield
        d.polygon([(cx, cy - 7), (cx + 6, cy - 4), (cx + 6, cy + 2),
                   (cx, cy + 7), (cx - 6, cy + 2), (cx - 6, cy - 4)],
                  fill=(255, 255, 255))


smalls = [
    ("5 \u00b7 RIYADH \u00b7 ENERGY", "Oil eases after Houthi refinery claim",
     "Brent near $95 after Wednesday's jump to $94.61; Riyadh downed four "
     "drones.", "CLAIM", "Reuters", "flame", GREEN),
    ("6 \u00b7 PYONGYANG \u00b7 DIPLOMACY", "North Korea expels Swiss diplomat",
     "Envoy Astier told to leave in 48 hours; office to close weeks after "
     "reopening.", "CONFIRMED", "KCNA / Reuters",
     "flag", PURPLE),
    ("7 \u00b7 JERUSALEM \u00b7 LAW", "Judges urge dropping gravest Netanyahu charges",
     "Most serious charges \u201cshould go\u201d; court doubts a conviction in "
     "Case 4000.", "REPORTED", "Reuters / CNN",
     "scales", BLUE),
    ("8 \u00b7 KYIV \u00b7 WAR", "Ukraine: five Russian jets hit in airfield strike",
     "Kyiv claims 3 MiG-31s and 2 Su-34s hit at Savasleyka, 300 km east of "
     "Moscow.", "CLAIM", "BBC", "jet", RED),
    ("9 \u00b7 USA \u00b7 TECH", "Nvidia's Huang faces Senate panel",
     "Reinstated chief testifies on AI chips, China and export controls.",
     "REPORTED", "Reports", "chip", NAVY),
    ("10 \u00b7 DELHI \u00b7 INDIA", "India marks Constitution Day; IITs add 6,000 seats",
     "77 years since adoption; new seats in robotics, AI and space tech from "
     "2027.", "OFFICIAL", "Reports", "temple", ORANGE),
    ("11 \u00b7 BRASILIA \u00b7 ENERGY", "Petrobras unveils $122bn investment plan",
     "Brazil expands energy ambitions; $83bn for exploration, output seen at "
     "2.9m bpd.", "CONFIRMED", "Reuters", "derrick", GREEN),
    ("12 \u00b7 CARACAS \u00b7 DEBT", "Venezuela reveals $237.5bn public debt",
     "Government plans historic restructure; debt is 242% of GDP.",
     "REPORTED", "Reuters", "coins", TEAL),
    ("13 \u00b7 DHAKA \u00b7 LABOUR", "Bangladesh raises garment wage 36%",
     "Entry-level minimum wage jumps to 17,000 taka a month after weeks of "
     "protests.", "OFFICIAL", "AP / Reuters", "shirt", PURPLE),
    ("14 \u00b7 WARSAW \u00b7 SECURITY", "Poland raises alarm after airspace violations",
     "Renewed incursions worry Warsaw as NATO watches its eastern flank.",
     "REPORTED", "Reports", "shield", RED),
]
BADGE_COL = {"CONFIRMED": GREEN, "REPORTED": ORANGE, "CLAIM": RED,
             "FORECAST": BLUE, "OFFICIAL": NAVY}
row_y = [342, 436]
for idx, sm in enumerate(smalls):
    kick, head, body, tag, src, gk, col = sm
    x = 14 + (idx % 5) * 200
    y = row_y[idx // 5]
    glyph(x, y, gk, col)
    d.text((x + 4, y + 5), kick, font=SANS_B(8), fill=(255, 255, 255))
    para(x, y + 24, head, SANS_B(10), INK, 195, 12)
    para(x, y + 50, body, SANS(9), INK, 195, 11)
    bw = badge(x, y + 76, tag, BADGE_COL[tag])
    d.text((x + bw + 5, y + 78), src, font=SANS(8), fill=GREY)

# ---------------------------------------------------------------- voices
d.rectangle([14, 530, 1010, 548], fill=RED)
d.text((20, 534), "VOICES OF THE DAY", font=SANS_B(11), fill=(255, 255, 255))
d.text((1004, 534), "IN THEIR OWN WORDS", font=SANS_B(9),
       fill=(255, 255, 255), anchor="ra")
voices = [
    ("\u201cInflation will stay above target for a considerable time.\u201d",
     "Bank of Korea statement, on hiking to 3.25%. BOK, Seoul."),
    ("\u201cThe bribery charge presents considerable difficulties.\u201d",
     "Judge Rivka Friedman-Feldman, Jerusalem District Court, on Case 4000."),
    ("\u201cStop complaining.\u201d",
     "Ukraine's government, to Vladimir Putin, on strikes inside Russia."),
]
vx = 14
for quote, attr in voices:
    para(vx, 554, quote, SERIF_I(10), INK, 322, 13)
    para(vx, 582, attr, SANS(8), GREY, 322, 10)
    vx += 333

# ---------------------------------------------------------------- map + briefs
d.rectangle([14, 608, 1010, 626], fill=NAVY)
d.text((20, 612), "WHERE IT HAPPENED", font=SANS_B(11), fill=(255, 255, 255))
d.text((1004, 612), "ALSO ON THURSDAY 26 NOVEMBER \u2014 STORIES 15 TO 45",
       font=SANS_B(10), fill=(255, 255, 255), anchor="ra")
d.rectangle([14, 630, 320, 860], fill=LIGHTBLUE, outline=INK, width=1)
continents = [
    [(34, 66), (120, 58), (128, 96), (104, 128), (66, 132), (36, 100)],
    [(108, 150), (140, 152), (138, 196), (116, 214), (100, 176)],
    [(160, 62), (196, 56), (200, 84), (168, 92)],
    [(162, 106), (206, 110), (200, 168), (172, 176), (158, 140)],
    [(206, 56), (300, 48), (306, 96), (262, 116), (214, 104), (204, 78)],
    [(258, 196), (296, 194), (292, 218), (260, 216)],
]
for poly in continents:
    d.polygon([(px + 14, py + 630) for px, py in poly], fill=LAND,
              outline=(120, 100, 60))
pins = {
    1: (266, 74), 2: (282, 88), 3: (174, 76), 4: (198, 72), 5: (216, 122),
    6: (290, 66), 7: (206, 116), 8: (210, 56), 9: (58, 92), 10: (242, 108),
    11: (118, 178), 12: (104, 158), 13: (252, 100), 14: (188, 62),
}
for n, (px, py) in pins.items():
    px, py = px + 14, py + 630
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255))
    d.text((px, py - 5), str(n), font=SANS_B(8), fill=(255, 255, 255), anchor="ma")
d.text((167, 842), "Nos. 1\u201314 pictured; 15\u201345 at right",
       font=SANS(8), fill=INK, anchor="ma")

briefs = [
    "Dow +0.3% Wed to 50,182.95; S&P -0.25%, Nasdaq -0.62%.",
    "S&P futures +0.3%, Nasdaq 100 +0.1% in early trade.",
    "Samsung +0.9%, SK Hynix +2.0% as Seoul chips rebound.",
    "Kioxia +11%, SoftBank +5.3% lead Tokyo's rebound.",
    "Brent $94.61, WTI $83.68 after Wednesday's rally.",
    "Gold holds near $3,550, close to a 14-month low.",
    "Tokyo CPI due 23:30 GMT; US markets shut today.",
    "OPEC+ ministers meet Sunday to set 2027 output.",
    "Chess rest day Friday; Game 4 on Saturday.",
    "Russia silent on the Savasleyka strike claim.",
    "65% of Russians 18-24 who died in 2025 died in war.",
    "Venezuela bonds jump 4 cents after debt disclosure.",
    "Venezuela GDP seen doubling to $200.9bn in 5 years.",
    "Bangladesh wage starts Dec 1; higher pay from Jan.",
    "Workers wanted 18,000 taka; board voted 4-2 for 17,000.",
    "Swiss office reopened only last month by FM Cassis.",
    "Swiss sanctions targeted the Songdowon camp.",
    "Case 4000: favours to Bezeq said worth 1.8bn shekels.",
    "Case 2000: judges doubt the conduct was a crime.",
    "Case 1000, the gifts case: judges urge a deal.",
    "Huang reinstated as Nvidia chief executive Monday.",
    "Huang faces House panels behind closed doors Dec 1.",
    "Nvidia to stop selling H200 chips in China.",
    "Petrobras: $83bn for exploration; nine new systems.",
    "Petrobras pays extra R$15.6bn dividend on Dec 23.",
    "India marks 77 years since its Constitution adopted.",
    "IIT seats focus on robotics, physical AI, space tech.",
    "BOK sees inflation at 2.7% in 2026, 2.4% in 2027.",
    "BOK growth outlook raised to 3.9% for 2026, 4.1% in 2027.",
    "Game 2 ended in 20 moves by repetition, in the London.",
    "First to 7\u00bd points takes the $2.5m world crown.",
]
for i, b in enumerate(briefs):
    n = 15 + i
    col = 0 if i < 16 else 1
    bx = 330 + col * 345
    by = 636 + (i % 16) * 14
    d.text((bx, by), f"{n}. {b}", font=SANS(10), fill=INK)

# ---------------------------------------------------------------- chart + how to read
d.rectangle([14, 864, 640, 936], outline=INK, width=1)
d.text((20, 868), "THE DAY IN ONE CHART \u2014 WED 25 NOV CLOSES",
       font=SANS_B(10), fill=RED)
chart = [("Kospi", -6.2), ("Taiex", -8.2), ("Nikkei", -3.3),
         ("Shanghai", -1.0), ("Hang Seng", +1.0)]
cy = 886
for name, val in chart:
    d.text((20, cy), name, font=SANS(9), fill=INK)
    barw = abs(val) * 20
    col = RED if val < 0 else GREEN
    d.rectangle([92, cy + 1, 92 + barw, cy + 9], fill=col)
    d.text((96 + barw, cy), f"{val:+.1f}%", font=SANS_B(9), fill=INK)
    cy += 10
d.rectangle([650, 864, 1010, 936], outline=INK, width=1)
d.text((658, 868), "HOW TO READ THE TAGS", font=SANS_B(10), fill=RED)
legend = [
    ("CONFIRMED", "2+ outlets", GREEN), ("REPORTED", "one outlet", ORANGE),
    ("CLAIM", "one side's word", RED), ("FORECAST", "due / expected", BLUE),
    ("OFFICIAL", "official source", NAVY),
]
ly = 879
for tag, meaning, col in legend:
    badge(658, ly, tag, col)
    d.text((760, ly + 1), meaning, font=SANS(9), fill=INK)
    ly += 11

# ---------------------------------------------------------------- watch / date check / sources
d.rectangle([14, 940, 1010, 962], fill=NAVY)
d.text((20, 945), "WHAT TO WATCH TOMORROW \u2014 FRI 27 NOV:",
       font=SANS_B(10), fill=GOLD)
d.text((308, 945), "Chess rest day; US markets reopen, early close; "
                   "euro-area inflation due; OPEC+ meets Sunday.",
       font=SANS(10), fill=(255, 255, 255))
d.rectangle([14, 966, 1010, 982], fill=RED)
d.text((20, 970), "DATE CHECK \u2014 LEFT OUT ON PURPOSE: FIRST REPORTED BEFORE THURSDAY",
       font=SANS_B(10), fill=(255, 255, 255))
para(14, 986, "WED 25 NOV: PCE + GDP results; Houthi claim on Ras Tanura; "
               "Shenzhou-24 lifts off; Cairo tanker fire kills 31. TUE 24 NOV: Dow "
               "tops 50,000; CIA breach first reported; Chen probe announced. "
               "SAT 21 NOV: BepiColombo flies by Mercury. SUN 22 NOV: COP31 ends, "
               "no pact. THU 12 NOV: Gibran quits as VP.",
     SANS(9), INK, 996, 11)
d.text((14, 1010), "Sources: Reuters, AP, Yonhap, BBC, FIDE, Chess.com, BOK, "
                   "Bloomberg, AAP, Hindu BusinessLine, CNN, NYT \u00b7 Original drawings",
       font=SANS(8), fill=GREY)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out_path, "PNG", optimize=True)
size = os.path.getsize(out_path)
print(f"entry.png {img.size[0]}x{img.size[1]} {size} bytes")
