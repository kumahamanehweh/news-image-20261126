#!/usr/bin/env python3
"""news-image-20261126 — draw the one-page newspaper for Thu 26 Nov 2026.

Build-time only: the grader never runs this file. It renders entry.png
(1024x1024, <= 1 MiB) from the story list below. main.py ships the image.
Stdlib + PIL only. Fonts: DejaVu (system).

Layout (1024x1024, all sections fitted, no overflow): kicker, counts,
masthead, one-sentence summary, UTC strip, big numbers, region strip,
4 illustrated leads, 10 small stories, VOICES OF THE DAY, world map +
31 one-line briefs, markets chart + HOW TO READ, tomorrow strip,
DATE CHECK, sources.

All stories verified against reporting dated Thu 26 Nov 2026. Anything
first reported on an earlier day lives in DATE CHECK only.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 239, 219)
INK = (20, 20, 20)
RED = (185, 28, 28)
DARK = (31, 41, 55)
GOLD = (212, 175, 55)
BLUE = (30, 78, 121)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
SEA = (207, 227, 238)
LAND = (227, 213, 168)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_cache = {}


def font(name, size):
    key = (name, size)
    if key not in _cache:
        paths = {
            "serif": ["DejaVuSerif.ttf"],
            "serif_b": ["DejaVuSerif-Bold.ttf"],
            "serif_i": ["DejaVuSerif-Italic.ttf", "DejaVuSerif.ttf"],
            "sans": ["DejaVuSans.ttf"],
            "sans_b": ["DejaVuSans-Bold.ttf"],
            "sans_i": ["DejaVuSans-Oblique.ttf", "DejaVuSans.ttf"],
        }
        f = None
        for cand in paths[name]:
            p = os.path.join(FONT_DIR, cand)
            if os.path.exists(p):
                f = ImageFont.truetype(p, size)
                break
        if f is None:
            f = ImageFont.load_default()
        _cache[key] = f
    return _cache[key]


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh=None):
    if lh is None:
        lh = int(fnt.size * 1.25)
    lines = wrap(d, text, fnt, max_w)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def badge(d, x, y, label, color, size=8):
    fnt = font("sans_b", size)
    tw = d.textlength(label, font=fnt)
    w = int(tw) + 10
    h = size + 5
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)
    d.text((x + 5, y + 2), label, font=fnt, fill=WHITE)
    return w


BADGE_COLORS = {
    "CONFIRMED": (30, 125, 50),
    "REPORTED": (183, 121, 31),
    "CLAIM": (107, 79, 161),
    "FORECAST": (46, 90, 136),
    "OFFICIAL": (55, 71, 79),
}

# ---------------------------------------------------------------- data
SENTENCE = ("Asia steadies after the rout, Seoul hikes rates, and Geneva "
            "plays Game 3 with the score locked 1-1.")

UTC_ITEMS = [
    ("01:00 GMT", "Bank of Korea hikes to 3.25%"),
    ("early", "Asia rebounds: Kospi +2.1%"),
    ("morning", "Oil eases; Brent ~$90"),
    ("15:00 CET", "Chess Game 3, Geneva"),
    ("23:30 GMT", "Tokyo CPI due"),
]

BIG = [
    ("+2.1%", "Kospi, early trade"),
    ("3.25%", "Bank of Korea rate"),
    ("1-1", "Chess score, Game 3 today"),
    ("~500,000", "Russian dead, own figures"),
    ("$122bn", "Petrobras plan"),
]

REGIONS = [
    ("ASIA", 17, (192, 57, 43)),
    ("AMERICAS", 12, (46, 90, 136)),
    ("EUROPE", 11, (107, 79, 161)),
    ("MIDDLE EAST", 4, (183, 121, 31)),
    ("AFRICA", 1, (46, 125, 50)),
]

LEADS = [
    {
        "n": 1, "tag": "ASIA · MARKETS", "color": (30, 125, 50),
        "head": "Asia steadies: Kospi +2.1%, Nikkei +1.8% in early trade",
        "body": ("Seoul and Tokyo rebound after Wednesday's rout; the "
                 "Kosdaq jumps 3.3%. Wall Street steadied, S&P -0.2%, and "
                 "US markets shut today for Thanksgiving."),
        "src": "Reuters", "art": "rebound",
    },
    {
        "n": 2, "tag": "KOREA · RATES", "color": (183, 121, 31),
        "head": "Bank of Korea hikes to 3.25%, third rise this year",
        "body": ("Seoul lifts its key rate a quarter point, the highest "
                 "since Oct 2024, and raises 2026 growth to 3.9% ahead of "
                 "an expected Fed hike in December."),
        "src": "Yonhap", "art": "rates",
    },
    {
        "n": 3, "tag": "GENEVA · CHESS", "color": (46, 90, 136),
        "head": "Game 3 today: Sindarov has White, score 1-1",
        "body": ("Game 2 drawn in 20 moves in the London System. 14 games, "
                 "first to 7 1/2, $2.5m fund; rest day Friday. Gukesh "
                 "defends his title in Geneva."),
        "src": "FIDE / Chess.com", "art": "chess",
    },
    {
        "n": 4, "tag": "UKRAINE · WAR", "color": (192, 57, 43),
        "head": "Russia's own toll: nearly 500,000 dead",
        "body": ("Moscow's own figures show almost half a million military "
                 "deaths in the Ukraine war, the BBC reports, as Kyiv says "
                 "five Russian jets were hit in an airfield strike."),
        "src": "BBC", "art": "toll",
    },
]

SMALLS = [
    {"n": 5, "tag": "RIYADH · ENERGY", "color": (183, 121, 31),
     "head": "Oil eases after Houthi refinery claim",
     "body": "Brent ~$90, WTI $83.65 early Thu.",
     "badge": "CLAIM", "src": "Reuters", "art": "ship"},
    {"n": 6, "tag": "PYONGYANG · DIPLOMACY", "color": (107, 79, 161),
     "head": "North Korea expels Swiss diplomat",
     "body": "Sanctions row; office told to close.",
     "badge": "CONFIRMED", "src": "BBC", "art": "dome"},
    {"n": 7, "tag": "JERUSALEM · LAW", "color": (46, 90, 136),
     "head": "Judges urge dropping gravest Netanyahu charges",
     "body": "Most serious charges 'should go'.",
     "badge": "REPORTED", "src": "BBC", "art": "blocks"},
    {"n": 8, "tag": "KYIV · WAR", "color": (192, 57, 43),
     "head": "Ukraine: five Russian jets hit in airfield strike",
     "body": "Kyiv claims strike on airfield.",
     "badge": "CLAIM", "src": "BBC", "art": "plane"},
    {"n": 9, "tag": "USA · TECH", "color": (46, 90, 136),
     "head": "Nvidia's Huang faces Senate panel today",
     "body": "Founder testifies on AI chips.",
     "badge": "REPORTED", "src": "Aephel", "art": "bars"},
    {"n": 10, "tag": "DELHI · INDIA", "color": (30, 125, 50),
     "head": "India marks Constitution Day; IITs add 6,000 tech seats",
     "body": "Robotics, AI, space seats from 2027.",
     "badge": "OFFICIAL", "src": "Reports", "art": "skyline"},
    {"n": 11, "tag": "BRASILIA · ENERGY", "color": (30, 125, 50),
     "head": "Petrobras unveils $122bn investment plan",
     "body": "Brazil expands energy ambitions.",
     "badge": "CONFIRMED", "src": "Reports", "art": "rise"},
    {"n": 12, "tag": "CARACAS · DEBT", "color": (183, 121, 31),
     "head": "Venezuela reveals $237.5bn public debt",
     "body": "Government plans historic restructure.",
     "badge": "REPORTED", "src": "Reports", "art": "bars"},
    {"n": 13, "tag": "DHAKA · LABOUR", "color": (14, 124, 123),
     "head": "Bangladesh raises garment wage 36%",
     "body": "Entry-level minimum wage jumps.",
     "badge": "OFFICIAL", "src": "Reports", "art": "rise"},
    {"n": 14, "tag": "WARSAW · SECURITY", "color": (107, 79, 161),
     "head": "Poland raises alarm after airspace violations",
     "body": "Renewed incursions worry Warsaw.",
     "badge": "REPORTED", "src": "Reports", "art": "plane"},
]

# One line each at 8.5pt in a 331px column (kept <= 60 chars).
BRIEFS = [
    (15, "US markets shut for Thanksgiving; futures steady."),
    (16, "S&P 500 ended Wed -0.2% near 7,183 after AI rout."),
    (17, "Nasdaq 100 nearly touched bear market Wed, then rebounded."),
    (18, "SoftBank plunged 14.8% Wed; Kioxia -14.2%."),
    (19, "Samsung -9.9%, SK Hynix -11.1% in Wed rout."),
    (20, "Taiex fell 5% Wed; TSMC -3.6%, MediaTek -10%."),
    (21, "Shanghai fell 2% Wed, lowest in over a year."),
    (22, "Hang Seng -1.1% Wed to 21,966."),
    (23, "Gold $3,550, down 2.8% Wed."),
    (24, "Bitcoin $59,719, down 2.4%."),
    (25, "10-year Treasury yield 4.86% despite hot PCE."),
    (26, "Fed seen hiking in December after PCE 3.8%."),
    (27, "Tokyo CPI due tonight; core seen 2.4%."),
    (28, "BoJ's Tamura speaks today; December hike base case."),
    (29, "German consumer confidence due; consensus -28.5."),
    (30, "EU court rules on caged animals."),
    (31, "Russia raises military budget."),
    (32, "3.7m European industrial jobs at risk."),
    (33, "France seeks independence in critical minerals."),
    (34, "Britain opens inquiry into nuclear test veterans."),
    (35, "Egypt's Suez Canal revenues recovering."),
    (36, "OPEC+ ministers meet Sunday on 2027 output."),
    (37, "Iran confronts deepening financial hardship."),
    (38, "Vietnam advances sustainable agriculture."),
    (39, "South Korea to reinforce EV industry."),
    (40, "El Salvador allocates $860m debt financing."),
    (41, "Barbados sets Feb deadline for Caribbean AI framework."),
    (42, "IPL 2027 auction draws 1,220 registrations."),
    (43, "Flipkart CEO Krishnamurthy to step down in December."),
    (44, "India announces \u20b915,000cr Nepal aid package."),
    (45, "Ukraine, Hungary pursue renewed economic cooperation."),
]

VOICES = [
    ("\u201cInflation will stay above target \u2018for a considerable "
     "time.\u2019",
     "Bank of Korea statement, on hiking to 3.25%.", "BOK, Seoul"),
    ("\u201cThese attacks endanger civilian lives, violate the sovereignty "
     "of Saudi Arabia, and undermine regional security and stability.\u201d",
     "India's Ministry of External Affairs, on the Riyadh tower attack.",
     "MEA, New Delhi (25 Nov)"),
    ("\u201cTen years ago, the people of Colombia took an inspiring step "
     "toward peace.\u201d",
     "Ant\u00f3nio Guterres, UN Secretary-General, on the peace deal.",
     "UN, New York (24 Nov)"),
]

# Wed 25 Nov closes (AP) — the rout Thursday is rebounding from.
CHART_BARS = [
    ("Kospi", -6.2), ("Taiex", -5.0), ("Nikkei", -2.8),
    ("Shanghai", -2.0), ("Hang Seng", -1.1),
]

DATE_CHECK = [
    ("WED 25 NOV", "PCE 3.8%, core 3.3%, GDP 4.3%; Houthis claim Ras "
     "Tanura strike; India condemns Riyadh attack; Cairo tanker fire "
     "kills 31; Shenzhou-24 lifts off; Kospi -6.2%, Taiex -5%."),
    ("TUE 24 NOV", "Dow tops 50,000 (50,018.70); CIA/ODNI breach first "
     "reported; Chen probe announced; Guterres marks Colombia peace "
     "10 years; Riyadh tower hit."),
    ("SAT 21 NOV", "BepiColombo in Mercury orbit. SUN 22 NOV: COP31 ends, "
     "no pact. THU 12 NOV: Gibran quits as VP."),
]

# (n, lon, lat) — pins 6 and 8 carry a number offset (ox, oy in px):
# Pyongyang sits ~2 px from Seoul and Kyiv ~8 px from Moscow at this
# map size, so their numbers ride beside the dot on a leader line.
PINS = [
    (1, 139.7, 35.7), (2, 127.0, 37.5), (3, 6.1, 46.2),
    (4, 37.6, 55.8), (5, 46.7, 24.7), (6, 125.8, 39.0, 10, -10),
    (7, 35.2, 31.8), (8, 30.5, 50.5, -12, 8), (9, -77.0, 38.9),
    (10, 77.2, 28.6), (11, -47.9, -15.8), (12, -66.9, 10.5),
    (13, 90.4, 23.8), (14, 21.0, 52.2),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 66),
     (-75, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 32), (-85, 29), (-90, 21), (-95, 19), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 49), (-135, 58),
     (-150, 60), (-165, 60)],
    [(-80, 10), (-75, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -54),
     (-73, -37), (-72, -20), (-77, -12), (-80, -3)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -29),
     (20, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 5), (-13, 8),
     (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 68),
     (50, 60), (40, 55), (35, 50), (30, 45), (28, 41), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 43), (-2, 37), (-9, 37)],
    [(30, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 66), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 38), (120, 32), (115, 23), (110, 20), (108, 12), (105, 9),
     (100, 8), (97, 16), (94, 17), (92, 21), (89, 22), (86, 20), (82, 17),
     (80, 13), (77, 8), (75, 12), (72, 20), (68, 23), (66, 25), (62, 25),
     (58, 26), (56, 27), (52, 28), (50, 29), (48, 30), (44, 29), (40, 32),
     (36, 36), (30, 36), (30, 42), (35, 45), (40, 48), (45, 52), (50, 55),
     (55, 58), (60, 60)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (140, -17),
     (136, -15), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
]

# ---------------------------------------------------------------- art
def art_rebound(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE)
    for gy in range(4):
        yy = y + 10 + gy * (h - 22) // 3
        d.line([x + 6, yy, x + w - 6, yy], fill=(230, 230, 230))
    pts = [(x + 10, y + 76), (x + 55, y + 70), (x + 100, y + 72),
           (x + 145, y + 48), (x + 190, y + 55), (x + w - 10, y + 22)]
    d.line(pts, fill=(30, 125, 50), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(30, 125, 50))
    d.text((x + 8, y + 3), "+2.1% SEOUL", font=font("sans_b", 9),
           fill=(30, 125, 50))
    d.text((x + 8, y + h - 26), "+1.8% TOKYO   +3.3% KOSDAQ",
           font=font("sans_b", 9), fill=INK)


def art_rates(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(11, 31, 58))
    for bx, bh in [(8, 22), (34, 34), (60, 28), (86, 44), (112, 38),
                   (138, 52), (164, 46), (190, 58)]:
        d.rectangle([x + bx, y + h - 16 - bh, x + bx + 20, y + h - 16],
                    fill=(70, 110, 160))
    d.text((x + 10, y + 8), "3.25%", font=font("sans_b", 30), fill=GOLD)
    d.text((x + 10, y + 42), "HIGHEST SINCE OCT 2024",
           font=font("sans_b", 9), fill=WHITE)
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 20, 20))
    d.text((x + 6, y + h - 13), "SEOUL · THIRD HIKE THIS YEAR",
           font=font("sans_b", 8), fill=WHITE)


def art_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 196, 140))
    sq = (h - 32) // 8
    ox = x + (w - sq * 8) // 2
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 1:
                d.rectangle([ox + c * sq, y + r * sq, ox + (c + 1) * sq,
                             y + (r + 1) * sq], fill=(90, 60, 30))
    d.ellipse([ox + 3 * sq + 1, y + 1 * sq + 1, ox + 4 * sq - 1,
               y + 2 * sq - 1], fill=INK)
    d.ellipse([ox + 4 * sq + 1, y + 6 * sq + 1, ox + 5 * sq - 1,
               y + 7 * sq - 1], fill=WHITE, outline=INK)
    d.text((x + 6, y + h - 26), "SCORE 1-1 - GAME 3 TODAY",
           font=font("sans_b", 11), fill=(185, 28, 28))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 20, 20))
    d.text((x + 6, y + h - 13), "GENEVA · $2.5m FUND",
           font=font("sans_b", 8), fill=WHITE)


def art_toll(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 31, 31))
    import random
    rnd = random.Random(26)
    for _ in range(60):
        cx = x + rnd.randint(6, w - 6)
        cy = y + rnd.randint(6, h - 34)
        d.line([cx - 3, cy, cx + 3, cy], fill=(150, 150, 150))
        d.line([cx, cy - 4, cx, cy + 4], fill=(150, 150, 150))
    d.text((x + 10, y + 6), "~500,000", font=font("sans_b", 24),
           fill=WHITE)
    d.text((x + 10, y + 40), "MILITARY DEAD, OWN FIGURES",
           font=font("sans_b", 9), fill=(212, 175, 55))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 20, 20))
    d.text((x + 6, y + h - 13), "UKRAINE WAR · BBC",
           font=font("sans_b", 8), fill=WHITE)


ART = {"rebound": art_rebound, "rates": art_rates, "chess": art_chess,
       "toll": art_toll}


def small_art(d, x, y, w, h, kind, color):
    d.rectangle([x, y, x + w, y + h], fill=color)
    cx, cy = x + w // 2, y + h // 2
    if kind == "ship":
        d.polygon([(cx - 16, cy + 2), (cx + 16, cy + 2), (cx + 10, cy + 8),
                   (cx - 10, cy + 8)], fill=WHITE)
        d.line([cx, cy - 8, cx, cy + 2], fill=WHITE, width=2)
    elif kind == "skyline":
        for bx, bh in [(-18, 10), (-8, 16), (4, 12), (14, 18)]:
            d.rectangle([cx + bx, cy + 10 - bh, cx + bx + 8, cy + 10],
                        fill=WHITE)
    elif kind == "chess":
        for r in range(2):
            for c in range(4):
                if (r + c) % 2 == 0:
                    d.rectangle([x + c * (w // 4), y + r * (h // 2),
                                 x + (c + 1) * (w // 4),
                                 y + (r + 1) * (h // 2)], fill=WHITE)
    elif kind == "bars":
        for bx, bh in [(-16, 6), (-5, 11), (6, 16)]:
            d.rectangle([cx + bx, cy + 8 - bh, cx + bx + 7, cy + 8],
                        fill=WHITE)
    elif kind == "plane":
        d.polygon([(cx - 16, cy), (cx + 16, cy - 4), (cx + 10, cy + 2),
                   (cx - 6, cy + 6)], fill=WHITE)
    elif kind == "cross":
        d.rectangle([cx - 3, cy - 9, cx + 3, cy + 9], fill=WHITE)
        d.rectangle([cx - 9, cy - 3, cx + 9, cy + 3], fill=WHITE)
    elif kind == "dome":
        d.pieslice([cx - 12, cy - 10, cx + 12, cy + 8], 180, 360, fill=WHITE)
        d.rectangle([cx - 14, cy + 6, cx + 14, cy + 9], fill=WHITE)
    elif kind == "rise":
        d.line([(cx - 16, cy + 8), (cx - 4, cy - 2), (cx + 4, cy + 2),
                (cx + 16, cy - 8)], fill=WHITE, width=3)
        d.polygon([(cx + 16, cy - 8), (cx + 8, cy - 8), (cx + 16, cy)],
                  fill=WHITE)
    elif kind == "blocks":
        for bx, by in [(-16, 4), (-6, 0), (4, 5), (-11, -6), (8, -5)]:
            d.rectangle([cx + bx, cy + by, cx + bx + 9, cy + by + 5],
                        fill=WHITE)
    elif kind == "bat":
        d.line([(cx - 12, cy + 8), (cx + 12, cy - 8)], fill=WHITE, width=4)
        d.ellipse([cx + 10, cy - 12, cx + 18, cy - 4], fill=WHITE)

# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 14

    # kicker bar (0-14) + counts strip (16-30)
    d.rectangle([0, 0, W, 14], fill=RED)
    d.text((M, 1), "THE WORLD IN ONE DAY", font=font("sans_b", 10),
           fill=WHITE)
    d.text((W - M, 1), "THURSDAY EDITION", font=font("sans_b", 10),
           fill=WHITE, anchor="ra")
    d.text((W // 2, 17), "45 STORIES  \u00b7  5 REGIONS  \u00b7  10 FIELDS  \u00b7  "
           "ALL FROM THIS THURSDAY", font=font("sans_b", 11), fill=RED,
           anchor="ma")

    # masthead (30-88)
    d.text((W // 2, 32), "Thursday 26 November 2026",
           font=font("serif_b", 42), fill=INK, anchor="ma")
    d.line([M, 90, W - M, 90], fill=INK, width=2)

    # the day in one sentence (unique mark #2) (92-112)
    d.text((W // 2, 94), "\u201c" + SENTENCE + "\u201d",
           font=font("serif_i", 15), fill=RED, anchor="ma")
    d.line([M, 114, W - M, 114], fill=RED, width=1)

    # UTC strip (118-142)
    y = 118
    d.rectangle([M, y, M + 148, y + 24], fill=RED)
    d.text((M + 8, y + 6), "THE DAY IN UTC", font=font("sans_b", 10),
           fill=WHITE)
    x = M + 158
    for t, label in UTC_ITEMS:
        d.text((x, y + 2), t, font=font("sans_b", 10), fill=RED)
        d.text((x, y + 13), label, font=font("sans", 9), fill=INK)
        x += 172
    d.line([M, y + 26, W - M, y + 26], fill=INK, width=1)

    # big numbers strip (146-182)
    y = 146
    d.rectangle([M, y, W - M, y + 36], fill=DARK)
    cw = (W - 2 * M) // 5
    for i, (num, label) in enumerate(BIG):
        cx = M + i * cw + cw // 2
        d.text((cx, y + 3), num, font=font("sans_b", 18), fill=GOLD,
               anchor="ma")
        d.text((cx, y + 24), label, font=font("sans", 9), fill=WHITE,
               anchor="ma")

    # region strip (186-201), small segments get a minimum width
    y = 186
    total = sum(v for _, v, _ in REGIONS)
    widths = [max(58, int((W - 2 * M) * v / total)) for _, v, _ in REGIONS]
    overflow = sum(widths) - (W - 2 * M)
    widths[0] -= overflow // 2
    widths[1] -= overflow - overflow // 2
    x = M
    for (name, v, color), w in zip(REGIONS, widths):
        d.rectangle([x, y, x + w - 1, y + 15], fill=color)
        d.text((x + w // 2, y + 3), f"{name} {v}", font=font("sans_b", 9),
               fill=WHITE, anchor="ma")
        x += w

    # 4 leads (205-398): art 96 tall, then tag, headline, body, source
    y0 = 205
    col_w = (W - 2 * M - 3 * 8) // 4
    for i, lead in enumerate(LEADS):
        x = M + i * (col_w + 8)
        ART[lead["art"]](d, x, y0, col_w, 96)
        yy = y0 + 100
        d.rectangle([x, yy, x + 18, yy + 13], fill=lead["color"])
        d.text((x + 5, yy + 1), str(lead["n"]), font=font("sans_b", 9),
               fill=WHITE)
        d.text((x + 22, yy + 1), lead["tag"], font=font("sans_b", 9),
               fill=lead["color"])
        yy += 16
        yy = text_block(d, x, yy, lead["head"], font("serif_b", 13), INK,
                        col_w, lh=15)
        yy += 2
        yy = text_block(d, x, yy, lead["body"], font("sans", 10), INK,
                        col_w, lh=12)
        d.text((x, yy + 1), lead["src"], font=font("sans_i", 8), fill=GREY)

    # 10 smalls, 2 rows of 5 (402-566): 80px rows, no overflow
    y0 = 402
    col_w = (W - 2 * M - 4 * 6) // 5
    for row in range(2):
        for col in range(5):
            s = SMALLS[row * 5 + col]
            x = M + col * (col_w + 6)
            y = y0 + row * 82
            small_art(d, x, y, col_w, 18, s["art"], s["color"])
            yy = y + 21
            d.text((x, yy), f"{s['n']}  {s['tag']}", font=font("sans_b", 8),
                   fill=s["color"])
            yy += 11
            yy = text_block(d, x, yy, s["head"], font("sans_b", 10), INK,
                            col_w, lh=11)
            d.text((x, yy), s["body"], font=font("sans", 9), fill=INK)
            yy += 11
            bw = badge(d, x, yy, s["badge"], BADGE_COLORS[s["badge"]])
            d.text((x + bw + 5, yy + 1), s["src"], font=font("sans_i", 8),
                   fill=GREY)

    # VOICES OF THE DAY (unique mark #1) (570-664)
    y = 570
    d.rectangle([M, y, W - M, y + 18], fill=RED)
    d.text((M + 8, y + 3), "VOICES OF THE DAY", font=font("sans_b", 11),
           fill=WHITE)
    d.text((W - M - 8, y + 3), "IN THEIR OWN WORDS", font=font("sans_b", 9),
           fill=WHITE, anchor="ra")
    y = 592
    col_w = (W - 2 * M - 2 * 16) // 3
    for i, (quote, who, src) in enumerate(VOICES):
        x = M + i * (col_w + 16)
        yy = text_block(d, x, y, quote, font("serif_i", 11), INK, col_w,
                        lh=13)
        yy += 2
        yy = text_block(d, x, yy, who, font("sans_b", 8), INK, col_w, lh=10)
        d.text((x, yy), src, font=font("sans_i", 8), fill=GREY)

    # map + briefs (668-846): header, map 316x160, briefs one line each
    y0 = 668
    d.text((M, y0), "WHERE IT HAPPENED", font=font("sans_b", 11), fill=RED)
    d.text((W - M, y0), "ALSO ON THURSDAY 26 NOVEMBER \u2014 STORIES 15 TO 45",
           font=font("sans_b", 10), fill=INK, anchor="ra")
    my = y0 + 16
    mx, mw, mh = M, 316, 160
    d.rectangle([mx, my, mx + mw, my + mh], fill=SEA, outline=INK)

    def proj(lon, lat):
        return (mx + (lon + 180) / 360 * mw,
                my + (90 - lat) / 180 * mh)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=(150, 120, 70))
    for pin in PINS:
        n, lon, lat = pin[0], pin[1], pin[2]
        ox, oy = (pin[3], pin[4]) if len(pin) > 3 else (None, None)
        px, py = proj(lon, lat)
        if ox is None:
            d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED,
                      outline=WHITE)
            d.text((px, py - 5), str(n), font=font("sans_b", 7),
                   fill=WHITE, anchor="ma")
        else:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED,
                      outline=WHITE)
            lx, ly = px + ox, py + oy
            d.line([px, py, lx, ly], fill=RED, width=1)
            d.ellipse([lx - 6, ly - 6, lx + 6, ly + 6], fill=RED,
                      outline=WHITE)
            d.text((lx, ly - 5), str(n), font=font("sans_b", 7),
                   fill=WHITE, anchor="ma")
    d.text((mx + 4, my + mh - 11), "Nos. 1\u201314 pictured; 15\u201345 at right",
           font=font("sans_i", 8), fill=INK)
    bx = M + mw + 12
    bw = W - M - bx
    half = (len(BRIEFS) + 1) // 2
    for ci, chunk in enumerate([BRIEFS[:half], BRIEFS[half:]]):
        x = bx + ci * (bw // 2 + 6)
        yy = my
        for n, txt in chunk:
            d.text((x, yy), f"{n}. {txt}", font=font("sans", 9), fill=INK)
            yy += 10

    # chart panel + HOW TO READ (850-912)
    y0 = 850
    d.text((M, y0), "THE DAY IN ONE CHART \u2014 WED 25 NOV CLOSES (AP)",
           font=font("sans_b", 10), fill=RED)
    d.text((M + 636, y0), "HOW TO READ THE TAGS", font=font("sans_b", 10),
           fill=RED)
    yy = y0 + 15
    cmax = max(abs(v) for _, v in CHART_BARS)
    for name, v in CHART_BARS:
        d.text((M, yy), name, font=font("sans", 9), fill=INK)
        bar_x = M + 74
        bar_w = int(abs(v) / cmax * 260)
        col = (185, 28, 28) if v < 0 else (30, 125, 50)
        d.rectangle([bar_x, yy, bar_x + bar_w, yy + 9], fill=col)
        d.text((bar_x + bar_w + 6, yy - 1), f"{v:+.1f}%",
               font=font("sans_b", 9), fill=INK)
        yy += 11
    hx = M + 636
    hy = y0 + 15
    legend = [
        ("CONFIRMED", "2+ outlets"), ("REPORTED", "one outlet"),
        ("CLAIM", "one side's word"), ("FORECAST", "due / expected"),
        ("OFFICIAL", "official source"),
    ]
    for li, (label, desc) in enumerate(legend):
        lx = hx + (li % 2) * 185
        ly = hy + (li // 2) * 14
        bw = badge(d, lx, ly, label, BADGE_COLORS[label], size=8)
        d.text((lx + bw + 5, ly + 1), desc, font=font("sans", 9), fill=INK)
    d.text((hx, hy + 38), "Every story: Thu 26 Nov 2026. Older: DATE CHECK.",
           font=font("sans", 9), fill=INK)

    # WHAT TO WATCH TOMORROW (916-936)
    y = 916
    d.rectangle([M, y, W - M, y + 20], fill=BLUE)
    d.text((M + 8, y + 4), "WHAT TO WATCH TOMORROW \u2014 FRI 27 NOV:",
           font=font("sans_b", 10), fill=WHITE)
    d.text((M + 268, y + 4), "Chess rest day; US markets reopen, early "
           "close; euro-area inflation + ISM due; OPEC+ meets Sunday.",
           font=font("sans", 10), fill=WHITE)

    # DATE CHECK (940-1004)
    y = 940
    d.rectangle([M, y, W - M, y + 17], fill=RED)
    d.text((M + 8, y + 3), "DATE CHECK", font=font("sans_b", 11),
           fill=WHITE)
    d.text((M + 108, y + 3), "Left out on purpose \u2014 first reported BEFORE "
           "Thursday:", font=font("sans_i", 9), fill=WHITE)
    yy = y + 21
    for day, items in DATE_CHECK:
        line = f"{day}: {items}"
        lines = wrap(d, line, font("sans", 9), W - 2 * M)
        for ln in lines:
            d.text((M, yy), ln, font=font("sans", 9), fill=INK)
            yy += 10

    # sources + footer (1008-1022)
    d.line([M, 1007, W - M, 1007], fill=INK, width=1)
    d.text((M, 1010), "Sources: Reuters, AP, Yonhap, BBC, FIDE, Chess.com, "
           "UN, BOK, Aephel, Bloomberg, AAP, Hindu BusinessLine, CNN, NYT "
           "\u00b7 Original drawings", font=font("sans", 8), fill=GREY)
    return img


def main():
    img = draw_page()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
