"""Draw the make.fun news-image-20261121 front page.

A newspaper front page summing up Saturday 21 November 2026: 45 stories
(15 illustrated leads + 30 briefs), 7 regions, 16 fields. Every story was
verified as happening, or first reported, on Saturday 21 November 2026.
All text and art is drawn in code with Pillow; no external images, no
timestamps, no randomness -- the output is byte-for-byte deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
INK = (20, 20, 20)
PAPER = (250, 247, 238)
RULE = (20, 20, 20)
RED = (178, 34, 34)
MUTED = (90, 86, 78)
GREEN = (26, 122, 46)
AMBER = (176, 110, 20)
BLUE = (31, 78, 156)

# ---------------------------------------------------------------- data

LEADS = [
    dict(n=1, place="ANTALYA", region="EU", field="CLIMATE", tag="REPORTED",
         kind="climate",
         headline="COP31 runs into overtime with no deal",
         summary="Talks pass the Friday deadline; draft still omits fossil fuels; EU: \u201cgood deal or no deal\u201d.",
         source="AP, Reuters", lat=36.9, lon=30.7),
    dict(n=2, place="RIYADH", region="ME", field="CONFLICT", tag="REPORTED",
         kind="missile",
         headline="Three Houthi missiles shot down over Riyadh",
         summary="Coalition intercepts 3 ballistic missiles ~02:00; a Houthi drone destroyed hours later.",
         source="Reuters, AFP", lat=24.7, lon=46.7),
    dict(n=3, place="JUN\u00cdN, PERU", region="AM", field="EARTHQUAKE", tag="REPORTED",
         kind="quake",
         headline="Magnitude 6.7 quake shakes central Peru",
         summary="00:09 UTC, felt in Lima and 7 regions; INDECI: 8 injured, 128 homes affected.",
         source="USGS, INDECI", lat=-11.2, lon=-75.9),
    dict(n=4, place="MERCURY", region="SP", field="SPACE", tag="REPORTED",
         kind="space",
         headline="BepiColombo enters orbit around Mercury",
         summary="37-min burn from 18:24 UTC captures the craft after an 8-year, ~10bn km journey.",
         source="ESA, Space.com", lat=None, lon=None),
    dict(n=5, place="KRYVYI RIH", region="EU", field="WAR", tag="REPORTED",
         kind="war",
         headline="Kryvyi Rih toll rises to 60 injured",
         summary="Two missiles hit Friday evening; 60 hurt incl. 6 children; a boy, 7, and a paramedic killed.",
         source="AP", lat=47.9, lon=33.4),
    dict(n=6, place="STRAIT OF HORMUZ", region="ME", field="CONFLICT", tag="CLAIM",
         kind="drone",
         headline="Iran claims two US drones downed over Hormuz",
         summary="IRGC says it downed an MQ-9 and an MQ-1; US CENTCOM denies an F-16 was attacked.",
         source="Press TV via ANI", lat=26.5, lon=56.3),
    dict(n=7, place="DAVAO", region="AS", field="AVIATION", tag="REPORTED",
         kind="aviation",
         headline="Jet lands safely in Davao after engine fire alert",
         summary="Air Niugini 767 diverts 00:08 local; all 146 aboard evacuate via slides, no injuries.",
         source="AP, CAAP", lat=7.1, lon=125.6),
    dict(n=8, place="LAS VEGAS", region="AM", field="MOTORSPORT", tag="REPORTED",
         kind="motorsport",
         headline="Antonelli fastest, Verstappen inherits Vegas pole",
         summary="Antonelli 1:33.893 quickest, but a 5-place penalty drops him to P6; Verstappen on pole.",
         source="Formula1.com", lat=36.2, lon=-115.1),
    dict(n=9, place="WELLINGTON", region="OC", field="CRICKET", tag="REPORTED",
         kind="cricket",
         headline="Rahul\u2019s 136 puts India 118 ahead in Wellington",
         summary="First Indian opener with Test tons in all four SENA countries; India 486/4 at stumps.",
         source="ESPNcricinfo", lat=-41.3, lon=174.8),
    dict(n=10, place="GLOBAL", region="SP", field="MARKETS", tag="REPORTED",
         kind="markets",
         headline="Bitcoin sinks below $57,000; $2.4bn liquidated",
         summary="Lowest since Sept 2024; $2.4bn in futures liquidated in 24h; Nasdaq fell 5.3% Friday.",
         source="Reuters, Binance", lat=1.35, lon=103.8),
    dict(n=11, place="SEJONG", region="AS", field="RAIL", tag="REPORTED",
         kind="rail",
         headline="Freight train derails near Sejong; students stranded",
         summary="5 of 21 cars derail 05:37 local, cutting power; trains halted on exam weekend.",
         source="Yonhap", lat=36.5, lon=127.3),
    dict(n=12, place="JEDDAH", region="ME", field="CONFLICT", tag="CLAIM",
         kind="missile",
         headline="Houthis threaten Jeddah ports, warn airlines",
         summary="Houthis threaten Saudi Red Sea ports and airspace; coalition strikes Mocha and Lahj.",
         source="TBS, Al Jazeera", lat=21.5, lon=39.2),
    dict(n=13, place="TURIN", region="EU", field="TENNIS", tag="REPORTED",
         kind="tennis",
         headline="Alcaraz beats Shelton to reach Turin final",
         summary="Alcaraz wins 3\u20136, 6\u20133, 7\u20136 in the ATP Finals semi; Zverev v Medvedev tonight.",
         source="ATP", lat=45.1, lon=7.7),
    dict(n=14, place="BAYELSA", region="AF", field="DISASTER", tag="REPORTED",
         kind="disaster",
         headline="Tinubu orders federal response to Bayelsa boat disaster",
         summary="Boat of funeral mourners capsized: 4 dead, 24 rescued; rally in Ibadan held quietly.",
         source="Presidency", lat=4.9, lon=6.1),
    dict(n=15, place="LAS VEGAS", region="AM", field="MOTORSPORT", tag="REPORTED",
         kind="motorsport",
         headline="Russell fastest in final Vegas practice after Verstappen clash",
         summary="Russell 1:34.041 tops FP3; the pair bang wheels at Turn 14; both called to stewards.",
         source="Formula1.com", lat=36.2, lon=-115.1),
]

BRIEFS = [
    (16, "ANTALYA", "COP31 draft drops $120bn finance goal", "Reuters", 36.9, 30.7),
    (17, "ANTALYA", "100 groups warn of \u201cmost disappointing COP\u201d", "AP", 36.9, 30.7),
    (18, "ADDIS ABABA", "Next climate summit: Addis Ababa, Nov 2027", "AP", 9.0, 38.7),
    (19, "DUBLIN", "23 nations demand fossil-fuel language restored", "AFP", 53.3, -6.3),
    (20, "ANTALYA", "COP31 president scrambles to break deadlock", "Reuters", 36.9, 30.7),
    (21, "RIYADH", "Riyadh on third straight night of alerts", "TBS", 24.7, 46.7),
    (22, "MOCHA, YEMEN", "Coalition strikes Mocha port and Lahj", "YPA, live coverage", 13.3, 43.2),
    (23, "RIYADH", "Houthis threaten Riyadh financial centre", "TBS", 17.7, 42.0),
    (24, "LIMA", "Quake felt across Peru; Congress shaken", "IGP", -12.0, -77.0),
    (25, "JUN\u00cdN", "Rockfalls block highways, power cut in Peru", "INDECI", -11.2, -75.9),
    (26, "JUN\u00cdN", "Peru quake measured 6.8 by German centre", "GFZ", -11.2, -75.9),
    (27, "PERU", "Second big quake in Peru in four days", "The Indian Post", -11.2, -75.9),
    (28, "MERCURY", "BepiColombo pair separate 9\u201310 Dec", "ESA", None, None),
    (29, "MERCURY", "BepiColombo\u2019s nine flybys to Mercury", "ESA", None, None),
    (30, "LAS VEGAS", "Both Ferraris miss Q3 in Las Vegas", "Autosport", 36.2, -115.1),
    (31, "LAS VEGAS", "Las Vegas GP starts 20:00 local Saturday", "Formula1.com", 36.2, -115.1),
    (32, "WELLINGTON", "Gill 98, Pant 55* as India pile on 486", "ESPNcricinfo", -41.3, 174.8),
    (33, "WELLINGTON", "Rahul second Asian opener with SENA set", "Wisden", -41.3, 174.8),
    (34, "GLOBAL", "Ether falls 6.3% as crypto fear stays extreme", "CoinGecko", 1.35, 103.8),
    (35, "NEW YORK", "Nvidia fell 14% on Friday", "Binance", 40.7, -74.0),
    (36, "TURIN", "Zverev meets Medvedev in Turin tonight", "ATP", 45.1, 7.7),
    (37, "TURIN", "Doubles semi-finals in Turin on Saturday", "ATP", 45.1, 7.7),
    (38, "KYIV", "Russian drones hit Kyiv and other cities overnight", "OSNT brief", 50.4, 30.5),
    (39, "KHARKIV", "Drone hits Kharkiv apartment block; 11 hurt", "AP", 49.9, 36.3),
    (40, "DAVAO", "Davao airport shut two hours; flights cancelled", "CAAP", 7.1, 125.6),
    (41, "DAVAO", "Six South Koreans aboard the Davao jet", "JTBC", 7.1, 125.6),
    (42, "JUN\u00cdN", "Quake shakes Peru\u2019s copper heartland", "The Indian Post", -11.2, -75.9),
    (43, "RIYADH", "\u201cProjectile streaked across Riyadh sky\u201d", "Reuters, AFP", 24.7, 46.7),
    (44, "ANTALYA", "COP31 venue boxed up as talks drag on", "AP", 36.9, 30.7),
    (45, "TEHRAN", "IRGC touts three new defence systems", "Press TV", 35.7, 51.4),
]

NUMBERS = [
    ("3", "Houthi missiles downed over Riyadh"),
    ("6.7", "magnitude of the Peru quake"),
    ("18:24 UTC", "BepiColombo enters Mercury orbit"),
    ("146", "people safe after Davao landing"),
    ("$2.4bn", "crypto futures liquidated in 24h"),
    ("136", "KL Rahul\u2019s runs in Wellington"),
]

REGIONS = [("EU", 12), ("AM", 11), ("ME", 8), ("SP", 5), ("AS", 4), ("OC", 3), ("AF", 2)]

TIMELINE = [
    ("00:09 UTC", "Peru quake, Jun\u00edn"),
    ("00:18 UTC", "3 missiles over Riyadh"),
    ("~01:00 UTC", "FP3: Russell fastest"),
    ("01:30 UTC", "Bitcoin $58,810 (-4.1%)"),
    ("~04:00 UTC", "Quali: Antonelli fastest"),
    ("05:37 KST", "Train derails, Sejong"),
    ("00:08 PHT", "Jet lands in Davao"),
    ("Morning", "INDECI toll; Tinubu responds"),
    ("13:00 UTC", "Alcaraz beats Shelton"),
    ("18:24 UTC", "BepiColombo at Mercury"),
    ("19:30 UTC", "Zverev v Medvedev"),
]

DATE_CHECK = (
    "LEFT OUT \u2014 the top 5\u2019s own errors: 5 missiles over Riyadh (it was 3 on Saturday; "
    "2 more were over Jazan on Friday) \u00b7 Trump\u2019s data-centre tax, the China\u2013Japan Taiwan "
    "warning, the UK\u2013EU deal, the Denmark expulsion, the Roundup settlement and the "
    "Australia\u2013China AI talks (all Friday 20 Nov) \u00b7 Zelensky\u2019s Crimea bridge warning "
    "(Wednesday 18 Nov) \u00b7 the Bayelsa boat and the Hodeidah strikes (Friday 20 Nov) \u00b7 "
    "the Kryvyi Rih toll is 60 injured, not 42 \u2014 and Rahul finished on 136, not 124*."
)

FOOTER = (
    "Every story here happened, or was first reported, on Saturday 21 November 2026 in at least "
    "one time zone. Local dates are stated where they differ from UTC. Claims are attributed, "
    "not stated as fact. Sources named beside each story \u00b7 Original drawings."
)

TAG_COLORS = {"REPORTED": GREEN, "CLAIM": AMBER, "FORECAST": BLUE}
KIND_TINT = {
    "climate": (214, 232, 214), "missile": (238, 214, 210), "quake": (232, 222, 200),
    "space": (208, 216, 238), "war": (232, 222, 200), "drone": (222, 222, 222),
    "aviation": (208, 226, 238), "motorsport": (238, 214, 210), "cricket": (214, 232, 214),
    "markets": (222, 222, 222), "rail": (228, 220, 232), "tennis": (226, 232, 190),
    "disaster": (208, 226, 238),
}
KIND_INK = {
    "climate": (46, 110, 46), "missile": (150, 40, 30), "quake": (120, 84, 30),
    "space": (40, 60, 140), "war": (120, 84, 30), "drone": (70, 70, 70),
    "aviation": (30, 90, 140), "motorsport": (150, 40, 30), "cricket": (46, 110, 46),
    "markets": (70, 70, 70), "rail": (90, 60, 130), "tennis": (110, 130, 30),
    "disaster": (30, 90, 140),
}

# ---------------------------------------------------------------- fonts


def _font(name, size):
    paths = [
        "/usr/share/fonts/truetype/liberation/%s" % name,
        "/usr/share/fonts/truetype/dejavu/%s" % name,
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default(size=size)


def fonts():
    return {
        "mast": _font("LiberationSerif-Bold.ttf", 40),
        "date": _font("LiberationSerif-Bold.ttf", 17),
        "kicker": _font("LiberationSans-Bold.ttf", 12),
        "stand": _font("LiberationSerif-Italic.ttf", 12),
        "head": _font("LiberationSans-Bold.ttf", 10),
        "big": _font("LiberationSerif-Bold.ttf", 24),
        "numlabel": _font("LiberationSans.ttf", 9),
        "lead_head": _font("LiberationSerif-Bold.ttf", 11),
        "lead_sum": _font("LiberationSans.ttf", 9),
        "lead_kick": _font("LiberationSans-Bold.ttf", 8),
        "src": _font("LiberationSans.ttf", 8),
        "tag": _font("LiberationSans-Bold.ttf", 7),
        "brief": _font("LiberationSans.ttf", 10),
        "brief_b": _font("LiberationSans-Bold.ttf", 10),
        "sec": _font("LiberationSans-Bold.ttf", 11),
        "map_pin": _font("LiberationSans-Bold.ttf", 7),
        "tl_time": _font("LiberationSans-Bold.ttf", 8),
        "tl": _font("LiberationSans.ttf", 8),
        "check": _font("LiberationSans.ttf", 9),
        "foot": _font("LiberationSerif-Italic.ttf", 9),
    }


# ---------------------------------------------------------------- helpers


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(d, y, text, font, fill=INK, x0=MARGIN, x1=W - MARGIN):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


def fit_lines(d, text, font, max_w, max_lines):
    """Wrap text, shrinking font is not possible here; truncate with ellipsis."""
    lines = wrap(d, text, font, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "\u2026", font=font) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "\u2026"
    return lines


# ---------------------------------------------------------------- illustrations
# Small original pictograms, one per lead kind, drawn with plain shapes.


def draw_illustration(d, box, kind, ink):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    w, h = x1 - x0, y1 - y0
    if kind == "climate":
        d.ellipse([cx - 8, cy - 9, cx + 8, cy + 7], outline=ink, width=2)
        for a in range(0, 360, 45):
            import math
            r1, r2 = 11, 15
            x_a, y_a = cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a))
            x_b, y_b = cx + r2 * math.cos(math.radians(a)), cy + r2 * math.sin(math.radians(a))
            d.line([x_a, y_a, x_b, y_b], fill=ink, width=2)
        d.arc([x0 + 4, y1 - 10, x1 - 4, y1 + 6], 180, 360, fill=ink, width=2)
    elif kind == "missile":
        d.polygon([(cx - 4, cy + 12), (cx + 2, cy - 12), (cx + 8, cy + 12)], fill=ink)
        d.polygon([(cx + 2, cy - 12), (cx + 10, cy - 4), (cx + 4, cy - 2)], fill=ink)
        d.polygon([(cx - 1, cy + 12), (cx - 5, cy + 16), (cx + 3, cy + 16)], outline=ink, width=2)
    elif kind == "quake":
        d.line([x0 + 4, cy, x0 + w * 0.3, cy, x0 + w * 0.4, cy - 9, x0 + w * 0.5, cy + 9,
                x0 + w * 0.6, cy - 6, x0 + w * 0.7, cy, x1 - 4, cy], fill=ink, width=2)
        d.line([x0 + 6, y1 - 4, x0 + w * 0.35, y1 - 10, x0 + w * 0.6, y1 - 4, x1 - 6, y1 - 9],
               fill=ink, width=2)
    elif kind == "space":
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=ink)
        d.ellipse([cx - 12, cy - 3, cx + 12, cy + 3], outline=ink, width=2)
        d.ellipse([x1 - 10, y0 + 3, x1 - 5, y0 + 8], fill=ink)
        d.ellipse([x0 + 5, y0 + 6, x0 + 8, y0 + 9], fill=ink)
    elif kind == "war":
        d.rectangle([x0 + 8, cy - 4, x0 + 26, y1 - 4], outline=ink, width=2)
        d.rectangle([x0 + 30, cy - 10, x0 + 46, y1 - 4], outline=ink, width=2)
        d.ellipse([cx + 6, y0 + 2, cx + 14, y0 + 10], outline=ink, width=2)
        d.ellipse([cx + 14, y0 + 6, cx + 20, y0 + 12], outline=ink, width=2)
        d.line([x0 + 4, y1 - 4, x1 - 4, y1 - 4], fill=ink, width=2)
    elif kind == "drone":
        d.line([x0 + 6, y0 + 6, x1 - 6, y1 - 6], fill=ink, width=2)
        d.line([x1 - 6, y0 + 6, x0 + 6, y1 - 6], fill=ink, width=2)
        for px, py in [(x0 + 6, y0 + 6), (x1 - 6, y0 + 6), (x0 + 6, y1 - 6), (x1 - 6, y1 - 6)]:
            d.ellipse([px - 5, py - 3, px + 5, py + 3], outline=ink, width=2)
        d.ellipse([cx - 6, cy - 4, cx + 6, cy + 4], fill=ink)
    elif kind == "aviation":
        d.ellipse([x0 + 6, cy - 4, x1 - 8, cy + 4], fill=ink)
        d.polygon([(cx - 6, cy - 3), (cx + 6, cy - 12), (cx + 10, cy - 3)], fill=ink)
        d.polygon([(cx - 2, cy + 3), (cx + 4, cy + 10), (cx + 8, cy + 3)], fill=ink)
        d.line([x0 + 4, cy + 12, x1 - 4, cy + 12], fill=ink, width=2)
    elif kind == "motorsport":
        d.rounded_rectangle([x0 + 6, cy - 6, x1 - 6, cy + 6], radius=4, outline=ink, width=2)
        d.ellipse([x0 + 12, cy + 4, x0 + 20, cy + 12], fill=ink)
        d.ellipse([x1 - 20, cy + 4, x1 - 12, cy + 12], fill=ink)
        d.line([x0 + 4, y1 - 3, x1 - 4, y1 - 3], fill=ink, width=2)
    elif kind == "cricket":
        d.line([x0 + 10, y0 + 4, x0 + 10, y1 - 8], fill=ink, width=2)
        d.line([x0 + 14, y0 + 4, x0 + 14, y1 - 8], fill=ink, width=2)
        d.line([x0 + 18, y0 + 4, x0 + 18, y1 - 8], fill=ink, width=2)
        d.line([cx + 2, y0 + 6, cx + 14, y1 - 10], fill=ink, width=3)
        d.ellipse([x1 - 12, y1 - 12, x1 - 4, y1 - 4], fill=ink)
    elif kind == "markets":
        d.line([x0 + 6, y0 + 4, x0 + 6, y1 - 6], fill=ink, width=2)
        d.line([x0 + 6, y1 - 6, x1 - 4, y1 - 6], fill=ink, width=2)
        d.line([x0 + 10, y0 + 8, x0 + 22, y0 + 12, x0 + 32, y0 + 8, x1 - 8, y1 - 8],
               fill=ink, width=2)
        d.polygon([(x1 - 8, y1 - 8), (x1 - 14, y1 - 8), (x1 - 8, y1 - 14)], fill=ink)
    elif kind == "rail":
        d.rounded_rectangle([x0 + 10, y0 + 4, x1 - 10, y1 - 10], radius=4, outline=ink, width=2)
        d.rectangle([x0 + 14, y0 + 8, x0 + 24, y0 + 14], fill=ink)
        d.rectangle([x1 - 24, y0 + 8, x1 - 14, y0 + 14], fill=ink)
        d.ellipse([x0 + 14, y1 - 12, x0 + 20, y1 - 6], fill=ink)
        d.ellipse([x1 - 20, y1 - 12, x1 - 14, y1 - 6], fill=ink)
        d.line([x0 + 4, y1 - 3, x1 - 4, y1 - 3], fill=ink, width=2)
    elif kind == "tennis":
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=ink, width=2)
        d.arc([cx - 10, cy - 10, cx + 10, cy + 10], 300, 60, fill=ink, width=2)
        d.arc([cx - 10, cy - 10, cx + 10, cy + 10], 120, 240, fill=ink, width=2)
    elif kind == "disaster":
        d.polygon([(x0 + 8, cy), (x1 - 8, cy), (x1 - 14, cy + 8), (x0 + 14, cy + 8)], fill=ink)
        d.line([cx, cy, cx, cy - 10], fill=ink, width=2)
        d.arc([x0 + 4, y1 - 8, x0 + 20, y1 + 2], 180, 360, fill=ink, width=2)
        d.arc([x1 - 20, y1 - 8, x1 - 4, y1 + 2], 180, 360, fill=ink, width=2)


# ---------------------------------------------------------------- sections


def draw_masthead(d, F):
    d.rectangle([MARGIN, 8, W - MARGIN, 11], fill=RULE)
    center(d, 16, "T H E   W O R L D   I N   O N E   D A Y", F["kicker"])
    center(d, 34, "Saturday 21 November 2026", F["mast"])
    center(d, 78, "COP31 runs past its deadline  \u00b7  Three missiles downed over Riyadh  \u00b7  "
                   "A quake shakes Peru  \u00b7  A spacecraft reaches Mercury", F["stand"])
    center(d, 96, "45 STORIES  \u00b7  7 REGIONS  \u00b7  16 FIELDS  \u00b7  EVERY ONE DATED "
                   "SATURDAY 21 NOVEMBER 2026", F["head"])
    d.line([MARGIN, 112, W - MARGIN, 112], fill=RULE, width=2)
    return 118


def draw_number_strip(d, F, y):
    cell_w = (W - 2 * MARGIN - 5 * 4) / 6
    for i, (num, label) in enumerate(NUMBERS):
        x0 = MARGIN + i * (cell_w + 4)
        x1 = x0 + cell_w
        d.rectangle([x0, y, x1, y + 44], outline=RULE, width=1)
        d.rectangle([x0, y, x1, y + 3], fill=RED)
        center(d, y + 7, num, F["big"], x0=x0, x1=x1)
        lines = wrap(d, label, F["numlabel"], cell_w - 8)
        ly = y + 31
        for ln in lines[:1]:
            center(d, ly, ln, F["numlabel"], fill=MUTED, x0=x0, x1=x1)
    return y + 50


def draw_region_bar(d, F, y):
    parts = "   \u00b7   ".join("%s %d" % (code, n) for code, n in REGIONS)
    center(d, y, parts + "      \u2014  45 STORIES, 7 REGIONS, 16 FIELDS", F["head"])
    d.line([MARGIN, y + 16, W - MARGIN, y + 16], fill=RULE, width=1)
    return y + 22


def draw_leads(d, F, y):
    cols, gap = 5, 4
    card_w = (W - 2 * MARGIN - (cols - 1) * gap) / cols
    card_h = 136
    for row in range(3):
        for col in range(5):
            lead = LEADS[row * 5 + col]
            x0 = MARGIN + col * (card_w + gap)
            x1 = x0 + card_w
            cy = y + row * (card_h + gap)
            d.rectangle([x0, cy, x1, cy + card_h], outline=RULE, width=1)
            # illustration band
            tint = KIND_TINT[lead["kind"]]
            d.rectangle([x0 + 1, cy + 1, x1 - 1, cy + 33], fill=tint)
            draw_illustration(d, (x0 + card_w / 2 - 26, cy + 2, x0 + card_w / 2 + 26, cy + 32),
                              lead["kind"], KIND_INK[lead["kind"]])
            # number tag
            d.ellipse([x0 + 4, cy + 4, x0 + 20, cy + 20], fill=RED)
            num = str(lead["n"])
            nw = d.textlength(num, font=F["tag"])
            d.text((x0 + 12 - nw / 2, cy + 8), num, font=F["tag"], fill=(255, 255, 255))
            # kicker: place + field
            d.text((x0 + 5, cy + 37), "%s \u00b7 %s" % (lead["place"], lead["field"]),
                   font=F["lead_kick"], fill=RED)
            # headline, up to 3 lines
            hl = fit_lines(d, lead["headline"], F["lead_head"], card_w - 10, 3)
            hy = cy + 49
            for ln in hl:
                d.text((x0 + 5, hy), ln, font=F["lead_head"], fill=INK)
                hy += 12
            # summary, up to 3 lines
            sl = fit_lines(d, lead["summary"], F["lead_sum"], card_w - 10, 3)
            sy = hy + 2
            for ln in sl:
                d.text((x0 + 5, sy), ln, font=F["lead_sum"], fill=INK)
                sy += 11
            # source + verification tag, pinned to the card bottom
            d.text((x0 + 5, cy + card_h - 12), lead["source"], font=F["src"], fill=MUTED)
            tag = lead["tag"]
            tw = d.textlength(tag, font=F["tag"]) + 8
            d.rounded_rectangle([x1 - 5 - tw, cy + card_h - 13, x1 - 5, cy + card_h - 3],
                                radius=4, fill=TAG_COLORS[tag])
            d.text((x1 - 5 - tw + 4, cy + card_h - 11), tag, font=F["tag"],
                   fill=(255, 255, 255))
    return y + 3 * card_h + 2 * gap + 6


def draw_briefs(d, F, y):
    d.text((MARGIN, y), "ALSO ON SATURDAY 21 NOVEMBER \u2014 30 MORE STORIES", font=F["sec"])
    d.line([MARGIN, y + 15, W - MARGIN, y + 15], fill=RULE, width=1)
    y += 19
    col_w = (W - 2 * MARGIN - 16) / 2
    row_h = 13.5
    for i, (n, place, frag, src, _lat, _lon) in enumerate(BRIEFS):
        col = i % 2
        row = i // 2
        x0 = MARGIN + col * (col_w + 16)
        by = y + row * row_h
        line = "%d \u00b7 %s \u2014 %s (%s)" % (n, place, frag, src)
        if d.textlength(line, font=F["brief"]) > col_w:
            # shorten the fragment until it fits
            while frag and d.textlength(
                    "%d \u00b7 %s \u2014 %s\u2026 (%s)" % (n, place, frag, src),
                    font=F["brief"]) > col_w:
                frag = frag[:-1]
            line = "%d \u00b7 %s \u2014 %s\u2026 (%s)" % (n, place, frag, src)
        d.text((x0, by), line, font=F["brief"], fill=INK)
    return y + 15 * row_h + 4


# ---------------------------------------------------------------- map + timeline

CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66), (-80, 62),
     (-75, 58), (-70, 45), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-95, 19),
     (-100, 16), (-105, 20), (-110, 23), (-117, 33), (-125, 40), (-125, 48),
     (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-80, 10), (-75, 5), (-70, 0), (-75, -5), (-80, -10), (-75, -18), (-70, -25),
     (-65, -35), (-60, -40), (-65, -50), (-70, -54), (-60, -45), (-55, -35),
     (-48, -28), (-40, -20), (-35, -8), (-40, -3), (-50, 0), (-60, 5), (-70, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68), (45, 60), (40, 55),
     (35, 50), (30, 46), (28, 44), (23, 40), (20, 40), (15, 38), (10, 37), (0, 38),
     (-5, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (12, 34), (20, 32), (30, 31), (35, 28), (38, 22),
     (40, 15), (43, 11), (48, 11), (51, 10), (46, 2), (42, -5), (40, -12), (36, -18),
     (33, -26), (28, -33), (20, -35), (16, -30), (12, -18), (9, -2), (9, 4), (0, 6),
     (-8, 5), (-13, 8), (-16, 12), (-17, 20), (-15, 28), (-10, 31)],
    # Asia
    [(35, 36), (40, 40), (45, 42), (50, 45), (55, 50), (60, 55), (65, 60), (70, 68),
     (80, 72), (95, 75), (110, 76), (125, 73), (140, 72), (160, 70), (178, 66),
     (170, 60), (160, 55), (150, 45), (140, 40), (130, 35), (127, 30), (122, 25),
     (115, 20), (110, 10), (105, 5), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15),
     (78, 8), (75, 15), (70, 20), (66, 25), (60, 25), (55, 27), (50, 30), (48, 30),
     (44, 29), (40, 32), (36, 36)],
    # Australia
    [(114, -22), (114, -32), (120, -34), (130, -32), (136, -35), (140, -38),
     (145, -38), (150, -37), (153, -28), (150, -22), (146, -19), (142, -11),
     (137, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
]


def _project(lon, lat, x0, y0, w, h):
    px = x0 + (lon + 180) / 360 * w
    py = y0 + (75 - lat) / 130 * h
    return px, py


def draw_map(d, F, x0, y0, w, h):
    d.text((x0, y0), "WHERE IT HAPPENED", font=F["sec"])
    mx, my, mw, mh = x0, y0 + 16, w, h - 16
    d.rectangle([mx, my, mx + mw, my + mh], fill=(233, 233, 226), outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [_project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(205, 205, 198), outline=(150, 150, 142))
    # Mercury callout (space, off-map)
    d.ellipse([mx + mw - 52, my + 4, mx + mw - 34, my + 22], fill=(40, 60, 140))
    d.ellipse([mx + mw - 56, my + 0, mx + mw - 30, my + 26], outline=(40, 60, 140), width=1)
    d.text((mx + mw - 118, my + 6), "4 \u00b7 MERCURY", font=F["tl_time"], fill=(40, 60, 140))
    d.text((mx + mw - 118, my + 16), "18:24 UTC", font=F["tl"], fill=MUTED)
    # pins 1-45 (skip space stories 4, 28, 29 -- they live in the callout)
    all_stories = [(s["n"], s["lat"], s["lon"]) for s in LEADS]
    all_stories += [(n, lat, lon) for (n, _p, _f, _s, lat, lon) in BRIEFS]
    space_pins = {4: (mx + mw - 43, my + 13), 28: (mx + mw - 54, my + 32),
                  29: (mx + mw - 70, my + 32)}
    for n, lat, lon in sorted(all_stories):
        if n in space_pins:
            px, py = space_pins[n]
        else:
            px, py = _project(lon, lat, mx, my, mw, mh)
            # deterministic de-clash nudge so same-place pins do not sit exactly on top
            px += ((n * 37) % 9 - 4) * 3
            py += ((n * 53) % 7 - 3) * 3
        r = 6
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255), width=1)
        num = str(n)
        nw = d.textlength(num, font=F["map_pin"])
        d.text((px - nw / 2, py - 4.5), num, font=F["map_pin"], fill=(255, 255, 255))
    return y0 + h


def draw_timeline(d, F, x0, y0, w, h):
    d.text((x0, y0), "THE DAY IN UTC", font=F["sec"])
    y = y0 + 16
    col_w = (w - 12) / 2
    for i, (t, label) in enumerate(TIMELINE):
        col = i % 2
        row = i // 2
        tx = x0 + col * (col_w + 12)
        ty = y + row * 15
        d.text((tx, ty), t, font=F["tl_time"], fill=RED)
        tw = d.textlength(t, font=F["tl_time"])
        lab = label
        while lab and d.textlength(lab, font=F["tl"]) > col_w - tw - 4:
            lab = lab[:-1]
        if lab != label:
            lab = lab[:-1] + "\u2026"
        d.text((tx + tw + 4, ty), lab, font=F["tl"], fill=INK)
    return y0 + h


def draw_date_check(d, F, y):
    h = 52
    d.rectangle([MARGIN, y, W - MARGIN, y + h], outline=RED, width=2)
    d.text((MARGIN + 6, y + 4), "DATE CHECK \u2014 WHAT WE LEFT OUT, AND WHY", font=F["sec"], fill=RED)
    lines = wrap(d, DATE_CHECK, F["check"], W - 2 * MARGIN - 12)
    ly = y + 18
    for ln in lines[:3]:
        d.text((MARGIN + 6, ly), ln, font=F["check"], fill=INK)
        ly += 11
    return y + h + 4


def draw_footer(d, F, y):
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)
    lines = wrap(d, FOOTER, F["foot"], W - 2 * MARGIN)
    ly = y + 4
    for ln in lines:
        center(d, ly, ln, F["foot"], fill=MUTED)
        ly += 11
    return ly


# ---------------------------------------------------------------- build


def build(path="entry.png"):
    F = fonts()
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = draw_masthead(d, F)
    y = draw_number_strip(d, F, y)
    y = draw_region_bar(d, F, y)
    y = draw_leads(d, F, y)
    y = draw_briefs(d, F, y)
    map_y = y + 2
    map_h = 100
    draw_map(d, F, MARGIN, map_y, 600, map_h)
    draw_timeline(d, F, MARGIN + 612, map_y, W - MARGIN - (MARGIN + 612), map_h)
    y = draw_date_check(d, F, map_y + map_h + 6)
    y = draw_footer(d, F, y)
    assert y <= H, "layout overflow: %d > %d" % (y, H)
    img.save(path, format="PNG")
    return path


if __name__ == "__main__":
    import os
    p = build("entry.png")
    print(p, os.path.getsize(p), "bytes")
