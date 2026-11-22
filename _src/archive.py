"""아유타 커피랩 아카이브 생성기: 섬 페이지 + 산지 사전 페이지 + 메인 + sitemap"""
import json, re, sys, html, os
from common import *
from lab import NOTES, SERIES
from glossary_data import GLOSS
from archive_contact import contact_link
from i18n_en import ISLANDS_EN, ORIGINS_EN, SPEC_KEYS, KIND, NOTES_EN

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
RAW = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "origins.json")))

MAP_SRC = ("Natural Earth(지형), Badan Pusat Statistik(BPS), ICCRI·World Coffee Research(품종), Specialty Coffee Indonesia, "
           "Sweet Maria's, Mercanta, 1Zpresso, AEKI-AICE, Inaexport 등 공개 자료 및 산지 스펙시트 정리")

ISLANDS = [
 dict(slug="sumatra", kr="수마트라", en="Sumatra", color="#5e7338",
      line="세계에서 여섯 번째로 큰 섬. 묵직하고 흙내음 나는 '인도네시아 커피'의 이미지가 여기서 나왔어요.",
      facts=["커피 산지 대부분이 화산을 따라 이어지는 <b>부킷바리산 산맥</b> 위에 있어요.",
             "북수마트라의 <b>토바호</b>는 거대한 화산 폭발로 생긴, 세계에서 가장 큰 화산 호수예요. 린통 산지가 이 호수 남서쪽에 있어요.",
             "수마트라 커피 하면 떠오르는 독특한 풍미는 <b>길링 바사(웻헐)</b>라는 인도네시아 특유의 가공법에서 와요."],
      wiki="https://en.wikipedia.org/wiki/Sumatra"),
 dict(slug="java", kr="자바", en="Java", color="#b5651d",
      line="세계에서 사람이 가장 많이 사는 섬. 영어로 커피를 '자바'라고 부르게 된 바로 그 섬이에요.",
      facts=["1690년대 네덜란드가 이 섬에 커피를 심으면서 <b>인도네시아 커피의 역사</b>가 시작됐어요.",
             "섬 한가운데를 화산이 줄지어 지나가요. 중부 자바의 <b>메라피</b>는 인도네시아에서 가장 활발한 화산 가운데 하나예요.",
             "족자카르타의 길거리 커피 <a href='lab-coffee-001.html'>코피 조스</a>처럼, 커피가 일상 문화에 깊이 들어와 있어요."],
      wiki="https://en.wikipedia.org/wiki/Java"),
 dict(slug="bali", kr="발리", en="Bali", color="#a8862e",
      line="힌두 문화가 살아 있는 '신들의 섬'. 해변만큼 고원 커피도 유명해요.",
      facts=["논에 물을 나누는 전통 관개 제도 <b>수박(Subak)</b>은 유네스코 세계유산이에요.",
             "킨타마니 고원은 <b>바투르 화산</b> 둘레에 있고, 인도네시아에서 처음으로 커피 지리적 표시(GI)를 받았어요.",
             "관광객이 가장 많이 찾는 섬이라, 커피 농장 체험도 여행 코스로 많이 들어가요."],
      wiki="https://en.wikipedia.org/wiki/Bali"),
 dict(slug="sulawesi", kr="술라웨시", en="Sulawesi", color="#8b1e3f",
      line="알파벳 K처럼 생긴 섬. 토라자 커피와 토라자 사람들의 문화로 알려져 있어요.",
      facts=["남술라웨시 산간의 <b>토라자</b> 사람들은 배 모양 지붕의 전통 가옥 <b>통코난</b>과 성대한 장례 의식으로 유명해요.",
             "토라자의 커피는 <b>17세기 네덜란드</b> 시기부터 재배된 것으로 전해져요.",
             "고도가 높아 산미와 단맛이 또렷한 편이에요."],
      wiki="https://en.wikipedia.org/wiki/Sulawesi"),
 dict(slug="nusa-tenggara", kr="누사틍가라", en="Nusa Tenggara", color="#3c7a74",
      line="발리 동쪽으로 이어지는 섬들. 롬복, 숨바와, 플로레스, 숨바, 티모르가 여기에 속해요.",
      facts=["롬복의 <b>린자니 화산</b>은 인도네시아에서 두 번째로 높은 화산이에요.",
             "플로레스 서쪽의 <b>코모도 국립공원</b>은 코모도왕도마뱀이 사는 유네스코 세계유산이에요.",
             "플로레스 바자와는 2012년 커피 지리적 표시(GI)를 받았어요. 소코리아에서는 커피를 카카오·정향·바닐라와 함께 길러요."],
      wiki="https://en.wikipedia.org/wiki/Lesser_Sunda_Islands"),
 dict(slug="papua", kr="파푸아", en="Papua", color="#4d6a8a",
      line="뉴기니섬의 서쪽 절반. 인도네시아에서 가장 높은 곳에서 커피가 자라요.",
      facts=["커피 산지 <b>발리엠 계곡</b>은 해발 1,500m가 넘는 고원 분지예요.",
             "계곡에 사는 <b>다니족</b>을 비롯한 원주민 문화가 지금도 이어지고 있어요.",
             "화학비료를 거의 쓰지 않는 소농 재배가 많아요."],
      wiki="https://en.wikipedia.org/wiki/Western_New_Guinea"),
]
IS = {i["slug"]: i for i in ISLANDS}

META = {
 1: ("gayo", "sumatra", "가요 커피", "가요"),
 2: ("sidikalang", "sumatra", "시디칼랑 커피", "시디칼랑"),
 3: ("lintong", "sumatra", "린통 커피", "린통"),
 4: ("mandheling", "sumatra", "만델링 커피", "만델링"),
 5: ("solok", "sumatra", "솔록 커피", "솔록"),
 6: ("kerinci", "sumatra", "케린치 커피", "케린치"),
 7: ("lampung", "sumatra", "람풍 로부스타", "람풍"),
 8: ("west-java", "java", "서부 자바 프리앙거 커피", "서부 자바 · 프리앙거"),
 9: ("temanggung", "java", "테망궁 로부스타", "중부 자바 · 테망궁"),
 10: ("ijen", "java", "이젠 커피", "동부 자바 · 이젠"),
 11: ("bali-kintamani", "bali", "발리 킨타마니 커피", "발리 · 킨타마니/불렐렝"),
 12: ("lombok", "nusa-tenggara", "롬복 린자니 커피", "롬복 · 린자니"),
 13: ("toraja", "sulawesi", "토라자 커피", "술라웨시 · 토라자"),
 14: ("flores-bajawa", "nusa-tenggara", "플로레스 바자와 커피", "플로레스 · 바자와"),
 15: ("flores-sokoria", "nusa-tenggara", "플로레스 소코리아 커피", "플로레스 · 소코리아"),
 16: ("papua-wamena", "papua", "파푸아 와메나 커피", "파푸아 · 와메나"),
}

ORIGINS = []
for r in RAW:
    slug, isl, title, short = META[r["no"]]
    kind = "로부스타" if "로부스타" in r["kr"] else "아라비카"
    ext = r["extra"]
    ayuta = None
    m = re.search(r'<span class="t">(.*?)</span>', ext)
    if m:
        note = re.search(r'<span class="afl">거래 농장 노트</span>(.*?)</div>', ext, re.S)
        ayuta = dict(lot=m.group(1), note=note.group(1).strip() if note else "")
    ORIGINS.append(dict(no=r["no"], slug="origin-" + slug, island=isl, title=title, short=short, en=r["en"].split(" · ")[0],
                        kind=kind, chips=r["chips"], specs=r["specs"], memo=r["memo"], ayuta=ayuta))
for i in ISLANDS:
    i["origins"] = [o for o in ORIGINS if o["island"] == i["slug"]]

NOTE_ISLAND = {"lab-coffee-001": ["java"]}

CSS = BASE_CSS + """
  .wrap{max-width:720px}
  .crumb{font-size:12.5px;color:var(--mud);margin-top:20px;font-weight:600}
  .crumb a{color:var(--mud);text-decoration:none} .crumb a:hover{color:var(--green-deep)}
  .crumb span{margin:0 6px;opacity:.6}
  header{text-align:left;padding:18px 0 0}
  .eyebrow{justify-content:flex-start;color:var(--ic)} .eyebrow::before{display:none}
  h1{font-size:clamp(26px,6.6vw,34px)}
  .en{font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:var(--mud);margin-top:-2px}
  .lead{font-size:16px;color:var(--ink-soft);line-height:1.8;margin:14px 0 0}
  .kind{display:inline-block;font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.08em;color:#fff;background:var(--ic);border-radius:20px;padding:3px 9px;vertical-align:middle;margin-left:6px;position:relative;top:-3px}
  .tbl{margin-top:14px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
  .tr{display:flex;gap:14px;padding:12px 16px} .tr+.tr{border-top:1px solid var(--line-soft)}
  .tr .k{flex:none;width:72px;font-size:12.5px;color:var(--mud);font-weight:700;padding-top:1px}
  .tr .v{font-size:14.5px;font-weight:600;line-height:1.55}
  .chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}
  .chips span{font-size:13px;font-weight:700;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:20px;padding:6px 12px}
  .facts{margin:14px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:9px}
  .facts li{background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 15px 13px 38px;font-size:14.5px;line-height:1.75;color:var(--ink-soft);position:relative}
  .facts li::before{content:"";position:absolute;left:16px;top:21px;width:8px;height:8px;border-radius:50%;background:var(--ic)}
  .facts li b{color:var(--ink)} .facts a{color:var(--green-deep);font-weight:700}
  .ayuta{margin-top:14px;border:1.5px solid #8b1e3f;border-radius:14px;padding:15px 16px;background:#fffafb}
  .ayuta .h{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.14em;color:#8b1e3f}
  .ayuta .lot{font-size:15px;font-weight:800;margin-top:5px}
  .ayuta p{font-size:13.5px;color:var(--ink-soft);line-height:1.75;margin:7px 0 0}
  .ayuta a{display:inline-block;margin-top:10px;font-size:13px;font-weight:700;color:#8b1e3f;text-decoration:none}
  .ayuta a:hover{text-decoration:underline}
  .olist{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-top:14px}
  @media(max-width:560px){.olist{grid-template-columns:1fr}}
  .oc{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--ic);border-radius:13px;padding:13px 15px;text-decoration:none;color:inherit;transition:transform .15s,border-color .15s}
  .oc:hover{transform:translateY(-2px);border-color:var(--roast)}
  .oc .t{font-size:15.5px;font-weight:800;letter-spacing:-.01em}
  .oc .t small{font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.06em;color:var(--ic);margin-left:6px}
  .oc .d{font-size:12.5px;color:var(--ink-soft);margin-top:4px;line-height:1.5}
  .oc.cur{opacity:.55;pointer-events:none}
  .btnrow{display:flex;flex-wrap:wrap;gap:9px;margin-top:16px}
  .lb{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:700;text-decoration:none;color:var(--ink);background:var(--card);border:1.5px solid var(--line);border-radius:12px;padding:10px 15px}
  .lb:hover{border-color:var(--roast)}
  .src{font-size:11.5px;color:var(--mud);line-height:1.75;margin-top:26px;padding-top:14px;border-top:1px solid var(--line)}
  .src a{color:var(--mud)}
  .foot{margin-top:30px}
  @media(prefers-reduced-motion:reduce){.oc{transition:none}.oc:hover{transform:none}}
"""


UI = {
 "ko": dict(site="아유타 커피랩", flavor="향미", flavor_note="※ 향미는 일반적인 경향이에요. 로트와 가공에 따라 달라져요.",
            info="산지 정보", lot_l="아유타가 들여오는 로트", lot_b="아유타커피에서 보기 →", others="{}의 다른 산지",
            isl_story="{} 섬 이야기 →", on_map="지도에서 보기 →", map="산지 지도 열기 →", origin_n="{} · 커피 산지 {:02d}",
            src="출처: {} · 아유타 로트·거래 농장 노트는 아유타 직접 거래처 정보", isl_eye="인도네시아의 섬", origins="커피 산지 · {}",
            facts="알아 두면 좋은 것", related="관련 이야기", other_isl="다른 섬", isl_src="출처: {} · 산지 자료: {}",
            yt="유튜브에서 쇼츠 보기", yt_s="주 3회, 인도네시아 커피·바닐라 이야기",
            foot='<div class="foot"><b>아유타 커피랩</b> · AYUTA COFFEE LAB<br>인도네시아 커피와 바닐라 아카이브</div>',
            o_title="{} · {} 커피 산지 | 아유타 커피랩", i_title="{} 커피와 문화 · 인도네시아 {} | 아유타 커피랩", ko_only=""),
 "en": dict(site="AYUTA COFFEE LAB", flavor="Flavor", flavor_note="※ Flavor notes describe the general tendency and vary by lot and process.",
            info="Origin profile", lot_l="Ayuta's lot from this origin", lot_b="See Ayuta Coffee →", others="More origins in {}",
            isl_story="About {} →", on_map="See on the map (Korean) →", map="Open the origin map (Korean) →", origin_n="{} · Coffee origin {:02d}",
            src="Sources: {} · Ayuta lot and farm notes come from Ayuta's direct suppliers.", isl_eye="Islands of Indonesia", origins="Coffee origins · {}",
            facts="Good to know", related="Related story", other_isl="Other islands", isl_src="Sources: {} · Origin data: {}",
            yt="Watch our Shorts on YouTube", yt_s="Three new stories a week (in Korean)",
            foot='<div class="foot"><b>AYUTA COFFEE LAB</b><br>Indonesian Coffee &amp; Vanilla Archive</div>',
            o_title="{} · {} Coffee Origin | AYUTA COFFEE LAB", i_title="{} Coffee & Culture, Indonesia | AYUTA COFFEE LAB", ko_only=" (Korean)"),
}
MAP_SRC_EN = ("Natural Earth (terrain), Badan Pusat Statistik (BPS), ICCRI & World Coffee Research (varieties), Specialty Coffee Indonesia, "
              "Sweet Maria's, Mercanta, 1Zpresso, AEKI-AICE, Inaexport and other public sources and origin spec sheets")


def I(isl, lang):
    if lang == "ko":
        return isl
    d = dict(isl); e = ISLANDS_EN[isl["slug"]]
    d.update(kr=e["kr"], line=e["line"], facts=e["facts"]); return d


def O(o, lang):
    if lang == "ko":
        return o
    e = ORIGINS_EN[o["no"]]; d = dict(o)
    d.update(title=e["title"], short=e["short"], memo=e["memo"], chips=e["chips"], kind=KIND[o["kind"]],
             specs=[(SPEC_KEYS.get(k, k), v) for (k, _), v in zip(o["specs"], e["specs"])])
    if o["ayuta"]:
        d["ayuta"] = dict(lot=e.get("lot", o["ayuta"]["lot"]), note=e.get("note", ""))
    return d


def page(title, desc, path, body, ic="#465828", lang="ko", file=""):
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{meta(title, desc, path, lang=lang)}
<style>{CSS}
  :root{{--ic:{ic}}}
  .crumbbar{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:20px}}
  .crumbbar .crumb{{margin-top:0}}
</style>
</head>
<body>
<div class="wrap">
{body.replace("%%LANG%%", lang_switch(file, lang))}
{UI[lang]["foot"]}
</div>
</body>
</html>
"""


def spec_rows(o, lang):
    isl = I(IS[o["island"]], lang)
    k_isl, k_kind = ("섬", "종류") if lang == "ko" else ("Island", "Species")
    rows = [(k_isl, f'<a href="island-{o["island"]}.html" style="color:inherit">{isl["kr"]}</a>'), (k_kind, o["kind"])] + list(o["specs"])
    return "".join(f'<div class="tr"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows)


def ocard(o, lang, cur=None):
    o = O(o, lang)
    c = " cur" if cur and cur["slug"] == o["slug"] else ""
    small = f'<small>{"로부스타" if lang == "ko" else "Robusta"}</small>' if o["kind"] in ("로부스타", "Robusta") else ""
    return f'<a class="oc{c}" style="--ic:{IS[o["island"]]["color"]}" href="{o["slug"]}.html"><div class="t">{o["short"]}{small}</div><div class="d">{" · ".join(o["chips"][:3])}</div></a>'


def origin_page(o0, lang="ko"):
    u = UI[lang]; P = "../" if lang == "en" else ""
    o = O(o0, lang); isl = I(IS[o["island"]], lang)
    alt = re.sub(r"\s*\(.*?\)", "", o["specs"][1][1])
    if lang == "ko":
        desc = f'{o["title"]} 산지 정보: {isl["kr"]} {o["specs"][0][1]}, 고도 {alt}, {o["specs"][2][1]}. 향미 {", ".join(o["chips"][:3])}.'
    else:
        desc = f'{o["title"]}, {isl["kr"]}, Indonesia: {o["specs"][0][1]}, {alt}, {o["specs"][2][1]}. Flavor: {", ".join(o["chips"][:3])}.'
    desc = html.escape(re.sub("<[^>]+>", "", desc), quote=True)
    ay = ""
    if o["ayuta"]:
        note = f'<p>{o["ayuta"]["note"]}</p>' if o["ayuta"]["note"] else ""
        ay = f'''<div class="label">{u["lot_l"]}</div>
  <div class="ayuta"><div class="h">AYUTA LOT</div><div class="lot">{o["ayuta"]["lot"]}</div>{note}
  <a href="https://www.ayutacoffee.com/" target="_blank" rel="noopener">{u["lot_b"]}</a></div>'''
    others = [x for x in IS[o["island"]]["origins"] if x["slug"] != o["slug"]]
    sib = (f'<div class="label">{u["others"].format(isl["kr"])}</div><div class="olist">' + "".join(ocard(x, lang) for x in others) + "</div>") if others else ""
    src = u["src"].format(MAP_SRC if lang == "ko" else MAP_SRC_EN)
    body = f'''  <div class="crumbbar"><div class="crumb"><a href="index.html">{u["site"]}</a><span>›</span><a href="island-{isl["slug"]}.html">{isl["kr"]}</a><span>›</span>{o["short"].split(" · ")[-1]}</div>%%LANG%%</div>
  <header>
    <div class="eyebrow">{u["origin_n"].format(isl["kr"], o["no"])}</div>
    <h1>{o["title"]}<span class="kind">{o["kind"]}</span></h1>
    <div class="en">{o0["en"]} · {IS[o["island"]]["en"]}, Indonesia</div>
    <p class="lead">{o["memo"]}</p>
  </header>

  <div class="label">{u["flavor"]}</div>
  <div class="chips">{"".join(f"<span>{c}</span>" for c in o["chips"])}</div>
  <p class="note">{u["flavor_note"]}</p>

  <div class="label">{u["info"]}</div>
  <div class="tbl">{spec_rows(o, lang)}</div>

  {ay}

  {sib}
  <div class="btnrow">
    <a class="lb" href="island-{isl["slug"]}.html">{u["isl_story"].format(isl["kr"])}</a>
    <a class="lb" href="{P}indonesia_origin_map.html#r-{o["no"]}">{u["on_map"]}</a>
  </div>

  <p class="src">{src}</p>'''
    return page(u["o_title"].format(o["title"], isl["kr"]), desc, o["slug"], body, IS[o["island"]]["color"], lang, o["slug"] + ".html")


def island_page(isl0, lang="ko"):
    u = UI[lang]; P = "../" if lang == "en" else ""
    isl = I(isl0, lang)
    ol = "".join(ocard(o, lang) for o in isl0["origins"])
    notes = [n for n in NOTES if isl0["slug"] in NOTE_ISLAND.get(n["slug"], [])]
    nb = ""
    if notes:
        nb = f'<div class="label">{u["related"]}</div><div class="olist">' + "".join(
            f'<a class="oc" style="--ic:{SERIES[n["series"]]}" href="{n["slug"]}.html"><div class="t">{(NOTES_EN[n["slug"]]["title"] if lang == "en" else n["title"])}</div><div class="d">{n["series"]} LAB {n["no"]}</div></a>' for n in notes) + "</div>"
    others = "".join(f'<a class="lb" href="island-{x["slug"]}.html">{I(x, lang)["kr"]}</a>' for x in ISLANDS if x is not isl0)
    names = ", ".join(O(o, lang)["short"].split(" · ")[-1] for o in isl0["origins"])
    if lang == "ko":
        desc = f'인도네시아 {isl["kr"]}({isl0["en"]}) 커피 산지와 문화 정리. {names}. {isl["line"]}'
    else:
        desc = f'Coffee origins and culture of {isl["kr"]}, Indonesia: {names}. {isl["line"]}'
    desc = html.escape(re.sub("<[^>]+>", "", desc), quote=True)
    body = f'''  <div class="crumbbar"><div class="crumb"><a href="index.html">{u["site"]}</a><span>›</span>{isl["kr"]}</div>%%LANG%%</div>
  <header>
    <div class="eyebrow">{u["isl_eye"]}</div>
    <h1>{isl["kr"]}</h1>
    <div class="en">{isl0["en"]}, Indonesia</div>
    <p class="lead">{isl["line"]}</p>
  </header>

  <div class="label">{u["origins"].format(len(isl0["origins"]))}</div>
  <div class="olist">{ol}</div>

  <div class="label">{u["facts"]}</div>
  <ul class="facts">{"".join(f"<li>{f}</li>" for f in isl["facts"])}</ul>

  {nb}

  <div class="label">{u["other_isl"]}</div>
  <div class="btnrow">{others}</div>
  <div class="btnrow"><a class="lb" href="{P}indonesia_origin_map.html">{u["map"]}</a></div>

  <p class="src">{u["isl_src"].format(f'<a href="{isl0["wiki"]}" target="_blank" rel="noopener">{isl0["en"]} (Wikipedia)</a>', MAP_SRC if lang == "ko" else MAP_SRC_EN)}</p>'''
    return page(u["i_title"].format(isl["kr"], isl["kr"]) if lang == "ko" else u["i_title"].format(isl["kr"]), desc, "island-" + isl0["slug"], body, isl0["color"], lang, "island-" + isl0["slug"] + ".html")


HOME_CSS = BASE_CSS + """
  .wrap{max-width:760px}
  .top{display:flex;align-items:center;justify-content:space-between;padding:18px 0 0}
  .brand{display:inline-flex;align-items:center;gap:9px;font-family:var(--mono);font-size:11.5px;letter-spacing:.26em;color:var(--green-deep);font-weight:700}
  .brand svg{width:16px;height:16px}
  .top a{font-size:12.5px;font-weight:700;color:var(--mud);text-decoration:none}
  header{padding:40px 0 0}
  h1{font-size:clamp(28px,7vw,40px);line-height:1.22}
  h1 .g{color:var(--green-deep)} h1 .r{color:var(--roast)}
  .sub{font-size:15px;max-width:520px;margin:12px auto 0}
  .search{position:relative;max-width:520px;margin:24px auto 0}
  .search input{width:100%;font:inherit;font-size:16px;padding:14px 16px 14px 44px;border-radius:14px;border:1.5px solid var(--line);background:#fff;color:var(--ink)}
  .search input:focus{outline:none;border-color:var(--roast)}
  .search svg{position:absolute;left:15px;top:50%;transform:translateY(-50%);width:18px;height:18px;stroke:var(--mud);fill:none;stroke-width:2}
  .res{max-width:520px;margin:8px auto 0;display:none;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;text-align:left}
  .res a{display:flex;justify-content:space-between;gap:10px;padding:11px 15px;text-decoration:none;color:var(--ink);font-size:14.5px;font-weight:700}
  .res a+a{border-top:1px solid var(--line-soft)}
  .res a:hover,.res a:focus{background:var(--card);outline:none}
  .res small{font-size:11.5px;color:var(--mud);font-weight:600;white-space:nowrap}
  .res .rt{min-width:0}.res em{display:block;font-style:normal;font-weight:500;font-size:12.5px;line-height:1.5;color:var(--ink-soft);margin-top:3px}
  .res .none{padding:12px 15px;font-size:13.5px;color:var(--mud)}
  .count{font-family:var(--mono);font-size:11px;color:var(--mud);letter-spacing:.08em;margin-top:12px}
  .count a{color:var(--green-deep);font-weight:700;text-decoration:underline;text-underline-offset:3px}
  .sech{text-align:center;font-size:20px;font-weight:800;letter-spacing:-.02em;margin:10px 0 0}
  .label{justify-content:center;margin-top:46px} .label::before{content:"";flex:none;width:30px;height:1px;background:var(--line)} .label::after{flex:none;width:30px}
  .isl{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:18px}
  @media(max-width:640px){.isl{grid-template-columns:1fr 1fr}}
  .ic{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c);border-radius:15px;padding:15px 15px 13px;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s}
  .ic:hover{transform:translateY(-2px);box-shadow:0 10px 24px -14px rgba(36,28,23,.4)}
  .ic .n{font-size:19px;font-weight:800;letter-spacing:-.02em}
  .ic .e{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;color:var(--mud);text-transform:uppercase}
  .ic .o{font-size:12.5px;color:var(--ink-soft);margin-top:9px;line-height:1.55;flex:1}
  .ic .c{font-family:var(--mono);font-size:10.5px;font-weight:700;color:var(--c);margin-top:10px}
  .notes{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px auto 0;max-width:660px}
  @media(max-width:640px){.notes{grid-template-columns:1fr}}
  .nc{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-top:4px solid var(--sc);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit}
  .nc img{display:block;width:100%;aspect-ratio:9/16;height:auto;object-fit:contain;background:#efe6da;border-bottom:1px solid var(--line-soft)}
  .nc .nb{padding:12px 14px 14px}
  @media(max-width:640px){.nc{flex-direction:row}.nc img{width:96px;flex:none;aspect-ratio:9/16;height:auto;border-bottom:0;border-right:1px solid var(--line-soft)}.nc .nb{align-self:center}}
  .nc:hover{border-color:var(--roast)}
  .nc .c{font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.12em;color:var(--sc)}
  .nc .t{font-size:15px;font-weight:800;letter-spacing:-.01em;line-height:1.4;margin-top:5px}
  .more{text-align:center;margin-top:12px} .more a{font-size:13px;font-weight:700;color:var(--green-deep);text-decoration:none}
  .tools{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:18px}
  @media(max-width:640px){.tools{grid-template-columns:1fr 1fr}}
  .tl{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit;transition:transform .15s,border-color .15s}
  .tl:hover{border-color:var(--tc);transform:translateY(-2px)}
  .tl .ti{display:flex;align-items:center;justify-content:center;height:92px;background:color-mix(in srgb,var(--tc) 13%,#fbf7f1);border-bottom:1px solid var(--line-soft);color:var(--tc)}
  .tl .ti svg{width:56px;height:56px;transition:transform .2s}
  .tl:hover .ti svg{transform:scale(1.08) rotate(-3deg)}
  .tl .tb{padding:12px 14px 14px}
  .tl .h{font-size:14.5px;font-weight:800} .tl .h::after{content:" →";color:var(--tc)}
  .yt{display:flex;align-items:center;gap:13px;max-width:660px;margin:16px auto 0;padding:13px 16px;background:var(--card);border:1px solid var(--line);border-radius:14px;text-decoration:none;color:inherit}
  .yt:hover{border-color:#c4302b}
  .yt .yp{flex:none;display:flex;align-items:center;justify-content:center;width:42px;height:30px;border-radius:9px;background:#c4302b}
  .yt .yp svg{width:20px;height:20px}
  .yt b{display:block;font-size:14.5px;font-weight:800}.yt small{display:block;font-size:12px;color:var(--ink-soft);margin-top:2px}
  .yt .ya{margin-left:auto;color:#c4302b;font-weight:800}
  .yt.ig{margin-top:9px}.yt.ig:hover{border-color:#c13584}.yt.ig .yp{width:30px;background:linear-gradient(45deg,#f9a13a,#e1306c 50%,#833ab4)}.yt.ig .ya{color:#c13584}
  .yt.ig .yp{margin:0 6px}
  .tl .d{font-size:12px;color:var(--ink-soft);margin-top:3px;line-height:1.45}
  .maker{margin-top:46px;border-top:1px solid var(--line);padding-top:22px;text-align:center}
  .maker p{font-size:13.5px;color:var(--ink-soft);margin:0;line-height:1.75}
  .maker p b{color:#8b1e3f}
  .mk{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin-top:12px}
  .mk a{font-size:13px;font-weight:700;text-decoration:none;color:var(--ink);border:1.5px solid var(--line);border-radius:20px;padding:7px 13px;background:var(--card)}
  .mk a.buy{background:#8b1e3f;border-color:#8b1e3f;color:#fff}
  .mk a:hover{border-color:var(--roast)}
  .imap{position:relative;margin-top:16px;background:#e7eef0;border:1px solid var(--line);border-radius:18px;overflow:hidden;
        background-image:radial-gradient(rgba(77,106,138,.12) 1px,transparent 1px);background-size:14px 14px}
  .imap svg{display:block;width:100%;aspect-ratio:960/352.7;--k:1}
  @media(max-width:600px){.imap svg{aspect-ratio:4/3}}
  .imap .off{fill:#d8cdb9;transition:opacity .3s}
  .isg{cursor:pointer;outline:none}
  .isg path{fill:var(--c);stroke:#fff;stroke-width:calc(1px*var(--k));transition:opacity .3s,filter .15s}
  .isg:hover path,.isg:focus-visible path{filter:brightness(1.12)}
  .isg:focus-visible path{stroke:var(--ink);stroke-width:calc(2px*var(--k))}
  .zoomed .isg path,.zoomed .off{opacity:.28} .zoomed .isg.on path{opacity:1;stroke:var(--ink);stroke-width:calc(1.2px*var(--k))}
  .imap .dot{fill:#fff;stroke:var(--ink);stroke-width:1.2;pointer-events:none;transition:opacity .3s}
  .zoomed .dot{opacity:0}
  .lbl text{font-family:var(--kr);font-size:17px;font-weight:800;fill:var(--ink);text-anchor:middle;pointer-events:none;paint-order:stroke;stroke:#e7eef0;stroke-width:4px;transition:opacity .3s}
  .lbl text.offt{font-size:13px;font-weight:600;fill:#9a8a70}
  @media(max-width:600px){.lbl text{font-size:24px;stroke-width:5px}.lbl text.offt{font-size:18px}}
  .zoomed .lbl text{opacity:0}
  .op{display:none}
  .zoomed .op.on{display:inline}
  .op circle{fill:#fff;stroke:var(--ink);stroke-width:2}
  .op text{font-family:var(--kr);font-size:14px;font-weight:800;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:4px;stroke-linejoin:round}
  .op:hover circle,.op:focus circle{fill:var(--roast)}
  .op:hover text,.op:focus text{fill:var(--roast)}
  @media(max-width:600px){.op text{font-size:15px}}
  .back{position:absolute;left:10px;bottom:10px;display:none;font:inherit;font-size:12.5px;font-weight:700;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:20px;padding:6px 12px;cursor:pointer;box-shadow:0 2px 8px rgba(36,28,23,.12)}
  .zoomed .back{display:block}
  .ichips{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;margin-top:12px}
  .chip{font:inherit;font-size:13.5px;font-weight:700;border:1.5px solid var(--c);color:var(--c);background:var(--card);border-radius:20px;padding:6px 13px;cursor:pointer}
  .chip.on,.chip:hover{background:var(--c);color:#fff}
  .ipanel{margin-top:12px;background:var(--card);border:1px solid var(--line);border-top:5px solid var(--c,var(--line));border-radius:16px;padding:16px 18px;min-height:64px}
  .ipanel .hint{text-align:center;color:var(--mud);font-size:13.5px;padding-top:6px}
  .ph{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
  .pn{font-size:21px;font-weight:800;letter-spacing:-.02em;color:var(--c)}
  .pe{font-family:var(--mono);font-size:10px;letter-spacing:.12em;color:var(--mud);text-transform:uppercase}
  .pg{flex:none;font-size:13px;font-weight:700;color:#fff;background:var(--c);border-radius:10px;padding:8px 12px;text-decoration:none}
  .pl{font-size:14px;color:var(--ink-soft);line-height:1.7;margin:8px 0 0}
  .pk{font-family:var(--mono);font-size:10px;letter-spacing:.16em;color:var(--mud);font-weight:700;margin-top:12px}
  .po{display:flex;flex-wrap:wrap;gap:7px;margin-top:8px}
  .po a{font-size:14px;font-weight:700;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:8px 12px;text-decoration:none}
  .po a:hover{border-color:var(--c)}
  .po small{font-family:var(--mono);font-size:9px;font-weight:700;color:var(--c);margin-left:5px}
  @media(prefers-reduced-motion:reduce){.ic{transition:none}.ic:hover{transform:none}.isg path{transition:none}}
"""


GEO = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapgeo.json")))


def classify(r):
    cx, cy = r["cx"], r["cy"]
    if cx < 285 and cy < 245: return "sumatra"
    if cx >= 750: return "papua"
    if 200 <= cx < 404 and cy >= 245: return "java"
    if 404 <= cx < 432 and cy >= 280: return "bali"
    if 432 <= cx < 645 and cy >= 280: return "nusa-tenggara"
    if 490 <= cx < 645: return "sulawesi"
    if 645 <= cx < 750: return "maluku"
    return "kalimantan"


MAP_UI = {
 "ko": dict(zoom="확대", kal="칼리만탄", mal="말루쿠", aria="인도네시아 섬 지도. 섬을 누르면 확대돼요", back="← 전체 지도", pick="섬 고르기",
            hint="지도에서 섬을 눌러 보세요. 그 섬의 커피 산지가 보여요.", story="섬 이야기 →", origins="커피 산지", rob="로부스타"),
 "en": dict(zoom="zoom in", kal="Kalimantan", mal="Maluku", aria="Map of the islands of Indonesia. Tap an island to zoom in", back="← Full map", pick="Choose an island",
            hint="Tap an island on the map to see its coffee origins.", story="About the island →", origins="Coffee origins", rob="Robusta"),
}


def island_map(lang="ko"):
    T = MAP_UI[lang]
    groups = {}
    for r in GEO["subs"]:
        groups.setdefault(classify(r), []).append(r["d"])

    def bbox(ds):
        pts = [tuple(map(float, p)) for d in ds for p in re.findall(r"(-?[\d.]+),(-?[\d.]+)", d)]
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        return min(xs), min(ys), max(xs), max(ys)

    g = []
    for k in ["kalimantan", "maluku"]:
        g.append(f'<path class="off" d="{" ".join(groups.get(k, []))}"/>')
    for i in ISLANDS:
        g.append(f'<g class="isg" data-i="{i["slug"]}" tabindex="0" role="button" aria-label="{I(i, lang)["kr"]} {T["zoom"]}" style="--c:{i["color"]}"><path d="{" ".join(groups[i["slug"]])}"/></g>')
    # 산지 핀: 섬을 고르면 이름과 함께 나타남. 겹치지 않게 좌우를 번갈아 둠
    pins = []
    for i in ISLANDS:
        for n, o in enumerate(i["origins"]):
            x, y = GEO["pins"][str(o["no"])]
            side = {8: -1, 9: 1, 10: 1}.get(o["no"], 1 if n % 2 == 0 else -1)
            name = O(o, lang)["short"].split(" · ")[-1].split("/")[0]
            anchor = "start" if side > 0 else "end"
            pins.append(f'<a class="op" data-i="{i["slug"]}" href="{o["slug"]}.html" transform="translate({x} {y})" aria-label="{O(o, lang)["title"]}">'
                        f'<g class="sc"><circle r="5"/><text x="{9*side}" y="4.5" text-anchor="{anchor}">{name}</text></g></a>')
    dots = "".join(f'<circle class="dot" cx="{x}" cy="{y}" r="3.2"/>' for x, y in GEO["pins"].values())
    labels = {"sumatra": (95, 205), "java": (300, 330), "bali": (418, 340), "sulawesi": (668, 160), "nusa-tenggara": (560, 345), "papua": (845, 160)}
    lab = "".join(f'<text x="{x}" y="{y}">{I(IS[k], lang)["kr"]}</text>' for k, (x, y) in labels.items())
    lab += f'<text class="offt" x="380" y="120">{T["kal"]}</text><text class="offt" x="712" y="250">{T["mal"]}</text>'
    data = {}
    for i in ISLANDS:
        x0, y0, x1, y1 = bbox(groups[i["slug"]] if i["slug"] != "papua" else groups[i["slug"]])
        if i["slug"] == "papua":  # 인도네시아 쪽(서쪽 절반) 위주로
            x1 = min(x1, 945)
        pad = max(x1 - x0, y1 - y0) * 0.18 + 14
        li = I(i, lang)
        data[i["slug"]] = dict(kr=li["kr"], en=(i["en"] if lang == "ko" else "Indonesia"), c=i["color"], line=li["line"], box=[round(x0 - pad, 1), round(y0 - pad, 1), round(x1 - x0 + 2 * pad, 1), round(y1 - y0 + 2 * pad, 1)],
                               o=[dict(t=O(o, lang)["short"].split(" · ")[-1], u=o["slug"] + ".html", r=o["kind"] == "로부스타") for o in i["origins"]])
    chips = "".join(f'<button type="button" class="chip" data-i="{i["slug"]}" style="--c:{i["color"]}">{I(i, lang)["kr"]}</button>' for i in ISLANDS)
    return f"""<div class="imap" id="imap">
    <svg id="isvg" viewBox="0 0 960 352.7" role="group" aria-label="{T["aria"]}">{"".join(g)}{dots}<g class="lbl">{lab}</g>{"".join(pins)}</svg>
    <button type="button" class="back" id="iback">{T["back"]}</button>
  </div>
  <div class="ichips" role="group" aria-label="{T["pick"]}">{chips}</div>
  <div class="ipanel" id="ip" aria-live="polite"><div class="hint">{T["hint"]}</div></div>
  <script>
  (function(){{
    var D={json.dumps(data, ensure_ascii=False)},ip=document.getElementById('ip'),svg=document.getElementById('isvg'),
        wrap=document.getElementById('imap'),FULL=[0,0,960,352.7],cur=FULL.slice(),raf=0,
        SC=document.querySelectorAll('#isvg .sc'),reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function setVB(v){{cur=v;svg.setAttribute('viewBox',v.join(' '));
      var r=svg.getBoundingClientRect();if(!r.width)return;var k=Math.max(v[2]/r.width,v[3]/r.height);
      svg.style.setProperty('--k',k);for(var i=0;i<SC.length;i++)SC[i].setAttribute('transform','scale('+k+')');}}
    function fit(b){{var r=svg.getBoundingClientRect(),ar=r.width/r.height,w=b[2],h=b[3],cx=b[0]+w/2,cy=b[1]+h/2;
      if(w/h<ar)w=h*ar;else h=w/ar;return [cx-w/2,cy-h/2,w,h];}}
    function go(t){{cancelAnimationFrame(raf);var s=cur.slice(),t0=performance.now(),D0=reduce?1:520;
      (function step(n){{var p=Math.min(1,(n-t0)/D0),e=1-Math.pow(1-p,3);
        setVB(s.map(function(v,i){{return v+(t[i]-v)*e;}}));if(p<1)raf=requestAnimationFrame(step);}})(t0);}}
    function pick(k){{
      var d=D[k]; if(!d) return;
      document.querySelectorAll('.isg,.chip,.op').forEach(function(el){{el.classList.toggle('on',el.dataset.i===k);}});
      wrap.classList.add('zoomed');go(fit(d.box));
      ip.style.setProperty('--c',d.c);
      ip.innerHTML='<div class="ph"><div><div class="pn">'+d.kr+'</div><div class="pe">'+d.en+'</div></div><a class="pg" href="island-'+k+'.html">{T["story"]}</a></div>'
        +'<p class="pl">'+d.line+'</p><div class="pk">{T["origins"]} · '+d.o.length+'</div><div class="po">'
        +d.o.map(function(o){{return '<a href="'+o.u+'">'+o.t+(o.r?'<small>{T["rob"]}</small>':'')+'</a>';}}).join('')+'</div>';
    }}
    function reset(){{wrap.classList.remove('zoomed');document.querySelectorAll('.on').forEach(function(el){{el.classList.remove('on');}});
      go(FULL);ip.style.removeProperty('--c');ip.innerHTML='<div class="hint">{T["hint"]}</div>';}}
    document.querySelectorAll('.isg,.chip').forEach(function(el){{
      el.addEventListener('click',function(){{pick(el.dataset.i);}});
      el.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();pick(el.dataset.i);}}}});
    }});
    document.getElementById('iback').addEventListener('click',reset);
    window.addEventListener('resize',function(){{var on=document.querySelector('.chip.on');setVB(on?fit(D[on.dataset.i].box):FULL);}});
    setVB(FULL);
  }})();
  </script>"""


TOOL_ICON = {
 # 산지 지도: 접힌 지도 + 핀
 "map": ("#3c7a74", '<path d="M6 13l11-4 14 4 11-4v26l-11 4-14-4-11 4z" fill="#fff" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/><path d="M17 9v26M31 13v26" stroke="currentColor" stroke-width="2" opacity=".45"/><path d="M10 25c4-3 7 2 11-1s7-3 10 0 6 1 8-1" stroke="currentColor" stroke-width="1.8" fill="none" opacity=".5" stroke-linecap="round"/><path d="M31 6c-4 0-7 3-7 6.6 0 4.8 7 11.4 7 11.4s7-6.6 7-11.4C38 9 35 6 31 6z" fill="#8b1e3f"/><circle cx="31" cy="12.6" r="2.6" fill="#fff"/>'),
 # 생두 도감: 생두 두 알
 "bean": ("#5e7338", '<g transform="rotate(-28 17 25)"><ellipse cx="17" cy="25" rx="8.5" ry="12" fill="#c9cf9a" stroke="currentColor" stroke-width="2.2"/><path d="M15.5 14c3 4 3 18 0 22" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></g><g transform="rotate(22 32 24)"><ellipse cx="32" cy="24" rx="8.5" ry="12" fill="#a9b56e" stroke="currentColor" stroke-width="2.2"/><path d="M30.5 13c3 4 3 18 0 22" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></g>'),
 # 카페 계산기: 계산기 + 동전
 "calc": ("#b5651d", '<rect x="9" y="6" width="22" height="34" rx="4" fill="#fff" stroke="currentColor" stroke-width="2.2"/><rect x="13" y="10" width="14" height="7" rx="1.5" fill="currentColor" opacity=".85"/><g fill="currentColor" opacity=".55"><circle cx="15" cy="23" r="1.9"/><circle cx="20" cy="23" r="1.9"/><circle cx="25" cy="23" r="1.9"/><circle cx="15" cy="29" r="1.9"/><circle cx="20" cy="29" r="1.9"/><circle cx="25" cy="29" r="1.9"/><circle cx="15" cy="35" r="1.9"/><circle cx="20" cy="35" r="1.9"/><circle cx="25" cy="35" r="1.9"/></g><circle cx="35" cy="34" r="8" fill="#e8b04a" stroke="currentColor" stroke-width="2"/><text x="35" y="38" text-anchor="middle" font-size="10.5" font-weight="800" font-family="sans-serif" fill="currentColor">₩</text>'),
 # 홈 레시피: 설탕 병 + 바닐라빈
 "recipe": ("#a8862e", '<rect x="11" y="13" width="20" height="27" rx="5" fill="#fff" stroke="currentColor" stroke-width="2.2"/><rect x="13" y="8" width="16" height="6" rx="2" fill="currentColor" opacity=".8"/><path d="M13.5 26h15v9a3 3 0 01-3 3h-9a3 3 0 01-3-3z" fill="#f3e6c8"/><path d="M24 40c4-10 9-22 15-32" stroke="#4a2c17" stroke-width="3.4" stroke-linecap="round" fill="none"/><path d="M36 8l4-3M37.5 10.5l4.5-1" stroke="#7a9a4a" stroke-width="2" stroke-linecap="round"/>'),
}
YOUTUBE_URL = "https://www.youtube.com/@ayutacoffeelab"  # 아유타 커피랩 유튜브 채널 주소. 비워 두면 메인에 안 나와요.


HOME_UI = {
 "ko": dict(title="아유타 커피랩 · 인도네시아 커피와 바닐라 아카이브",
            desc="인도네시아 커피 전문가가 산지에서 보고 배운 모든 것. 수마트라·자바·발리·술라웨시·누사틍가라·파푸아의 커피 산지 16곳과 섬별 문화, 바닐라 이야기.",
            maplink="산지 지도 →", h1="인도네시아 <span class='g'>커피</span>와 <span class='r'>바닐라</span> 아카이브",
            sub="인도네시아 커피 전문가가 산지에서 보고 배운 모든 것", ph="토라자, 가요, 길링 바사, 바닐라…", qaria="아카이브 검색",
            count="자료 {}개 · 계속 쌓이는 중", none="아직 없는 자료예요. 곧 채울게요.", by_isl="섬으로 찾기", lab="LAB 노트",
            lab_h="쇼츠에서 본 이야기, 여기서 자세히", more="이야기 전체 보기 →", tools="도구",
            tl=[("map", "indonesia_origin_map.html", "산지 지도", "16곳을 지형 지도에서"), ("bean", "bean_catalog.html", "생두 도감", "산지·가공·향미 카드"),
                ("calc", "cafe_pricing.html", "카페 계산기", "한 잔의 원가와 이익"), ("recipe", "recipe.html", "홈 레시피", "바닐라빈 슈가부터")],
            maker="아유타 커피랩은 인도네시아 커피와 바닐라빈을 들여오는 <b>아유타커피</b>가 만들어요.",
            buy="원두·바닐라빈 → 아유타커피", co="회사 → 아유타상사", ig="아유타커피 인스타그램",
            s_isl="섬", s_org="{} · 산지", s_story="이야기", s_tool="도구·레시피",
            tools_idx=[("인도네시아 커피 산지 지도", "지도 산지 map", "indonesia_origin_map.html"), ("커피 장사로 부자되는 계산기", "계산기 원가 카페 이익", "cafe_pricing.html"),
                       ("생두 도감", "생두 도감 green bean", "bean_catalog.html"), ("바닐라빈 슈가 만드는 법", "바닐라 레시피 설탕", "recipe_vanilla_sugar.html")],
            foot='<div class="foot"><b>아유타 커피랩</b> · AYUTA COFFEE LAB<br>(주)아유타상사 · Ayuta Trading Co., Ltd.</div>', cover="쇼츠 표지", gl=' · <a href="glossary.html">용어 사전</a>', yt="아유타커피랩 유튜브 채널", yt_s="알고 마시면 더 맛있는 인도네시아 커피와 바닐라 이야기"),
 "en": dict(title="AYUTA COFFEE LAB · Indonesian Coffee & Vanilla Archive",
            desc="Everything an Indonesian coffee specialist has seen and learned at the origin: 16 coffee origins across Sumatra, Java, Bali, Sulawesi, Nusa Tenggara and Papua, island culture and the story of vanilla.",
            maplink="Origin map (Korean) →", h1="Indonesian <span class='g'>Coffee</span> &amp; <span class='r'>Vanilla</span> Archive",
            sub="Everything an Indonesian coffee specialist has seen and learned at the origin", ph="Toraja, Gayo, wet-hulling, vanilla…", qaria="Search the archive",
            count="{} entries · and growing", none="Nothing here yet. More is on the way.", by_isl="Explore by island", lab="LAB Notes",
            lab_h="Stories from our Shorts, in depth", more="All stories →", tools="Tools (in Korean)",
            tl=[("map", "../indonesia_origin_map.html", "Origin map", "16 origins on a terrain map"), ("bean", "../bean_catalog.html", "Green bean catalog", "Origin, process, flavor"),
                ("calc", "../cafe_pricing.html", "Café calculator", "Cost and profit per cup"), ("recipe", "../recipe.html", "Home recipes", "Starting with vanilla sugar")],
            maker="AYUTA COFFEE LAB is made by <b>Ayuta Coffee</b>, an importer of Indonesian coffee and vanilla beans.",
            buy="Coffee &amp; vanilla → Ayuta Coffee", co="Company → Ayuta Trading", ig="Ayuta Coffee on Instagram",
            s_isl="Island", s_org="{} · origin", s_story="Story", s_tool="Tool (Korean)",
            tools_idx=[("Indonesian coffee origin map", "map origins", "../indonesia_origin_map.html"), ("Café profit calculator", "calculator cost cafe profit", "../cafe_pricing.html"),
                       ("Green bean catalog", "green bean catalog", "../bean_catalog.html")],
            foot='<div class="foot"><b>AYUTA COFFEE LAB</b><br>Ayuta Trading Co., Ltd.</div>', cover="Short cover", gl="", yt="AYUTA COFFEE LAB on YouTube", yt_s="Stories of Indonesian coffee and vanilla that make every cup taste better (in Korean)"),
}
LAB_IMG = {"lab-vanilla-001": "vanilla-001", "lab-indonesia-001": "indonesia-001", "lab-coffee-001": "coffee-001"}


# 같은 말을 다르게 쓰는 경우 (검색용 별칭)
GLOSS_ALIAS = {
    "BP": "비피 로부스타 클론", "Tugusari": "투구사리", "Lini S (S795)": "라인에스 린이에스 s라인 에스795",
    "Sigararutang": "시가라루탕 시가라 우탕", "Kartika": "카르티카", "Typica / Typika": "티피카 티피카종",
    "Kopyol": "코퓰 코피올", "Red Bourbon": "레드 버번 레드부르봉 부르봉 버본",
    "내추럴 (Natural)": "내추럴 내츄럴 natural 건식", "익스텐디드 내추럴 (Extended Natural)": "익스텐디드 익스텐드 롱 내추럴",
    "아나에로빅 (Anaerobic)": "애너로빅 혐기 무산소 anaerobic", "웨트헐 / 길링 바사 (Giling Basah)": "웻헐 웻헐링 웨트헐링 웨트 헐 wet hull wet-hulled 길링바사 습식 탈각 세미워시",
    "풀워시 (Full Wash · 워시드)": "풀워시드 풀 워시 워시드 washed 수세식 습식", "신도로 · 숨빙 (Sindoro · Sumbing)": "신도로 숨빙 산",
    "커핑 점수": "커핑 스코어 cupping score sca 점수", "밀도 (g/L)": "밀도 density", "그레이드 G1–G3": "등급 그레이드 grade g1 g2 g3", "핸드픽 (Hand-pick)": "핸드픽 핸드피킹 손으로 골라 선별",
}


def glossary():
    """생두 도감의 '용어 풀이'를 검색에 넣는다: (용어, 앵커, 풀이)"""
    p = f"{OUT}/bean_catalog.html"
    if not os.path.exists(p):
        return []
    src = open(p, encoding="utf-8").read()
    out = []
    for gid, term, d in re.findall(r'<div class="gt" id="(g-\d+)"><b>(.*?)</b>\s*[—-]\s*(.*?)</div>', src, re.S):
        d = re.sub("<[^>]+>", "", d).strip()
        out.append((re.sub("<[^>]+>", "", term).strip(), gid, d))
    return out


def tid(i):
    return f"t-{i}"


def all_terms():
    """(그룹, 용어, 별칭, 풀이, 링크, 앵커) — 용어 사전 + 생두 도감 용어 풀이"""
    out = []
    for g, items in GLOSS:
        for t, al, d, u in items:
            out.append((g, t, al, d, u))
    names = {t for _, t, _, _, _ in out}
    for t, gid, d in glossary():
        if t not in names:
            out.append(("생두 도감 용어", t, GLOSS_ALIAS.get(t, ""), d, f"bean_catalog.html#{gid}"))
    return [(g, t, al, d, u, tid(i + 1)) for i, (g, t, al, d, u) in enumerate(out)]


def glossary_page():
    terms = all_terms()
    groups = []
    for g, t, al, d, u, a in terms:
        if not groups or groups[-1][0] != g:
            groups.append((g, []))
        more = f' <a href="{u}">자세히 →</a>' if u else ""
        groups[-1][1].append(f'<li id="{a}"><b>{t}</b><span>{d}{more}</span></li>')
    body = "".join(f'<div class="label">{g}</div><ul class="gl">{"".join(li)}</ul>' for g, li in groups)
    css = """
  .gl{list-style:none;margin:14px 0 0;padding:0;border:1px solid var(--line);border-radius:14px;background:#fff;overflow:hidden}
  .gl li{display:flex;flex-direction:column;gap:4px;padding:13px 16px;scroll-margin-top:20px}
  .gl li+li{border-top:1px solid var(--line-soft)}
  .gl b{font-size:15px;font-weight:800}
  .gl span{font-size:14px;line-height:1.7;color:var(--ink-soft)}
  .gl a{color:var(--green-deep);font-weight:700;text-decoration:none;white-space:nowrap}
  .gl li:target{background:#fbefc9}"""
    title = "인도네시아 커피 용어 사전 · 아유타 커피랩"
    desc = "코피 투브룩, 코피 수수, 굴라 아렌, 코피 루왁, 길링 바사, 아살란, 로부스타까지. 인도네시아 커피와 바닐라 용어를 한국어로 쉽게 풀었어요."
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta(title, desc, "glossary", alt=False)}
<style>{CSS}{css}</style>
</head>
<body>
<div class="wrap">
  <div class="crumb"><a href="index.html">아유타 커피랩</a><span>›</span>용어 사전</div>
  <header>
    <div class="eyebrow">GLOSSARY</div>
    <h1>인도네시아 커피 용어 사전</h1>
    <p class="lead">인도네시아에서 커피를 마시고, 사고, 이야기할 때 나오는 말 {len(terms)}개. 계속 늘어나요.</p>
  </header>
  {body}
  {UI["ko"]["foot"]}
</div>
</body>
</html>
"""


def home(lang="ko"):
    h = HOME_UI[lang]; P = "../" if lang == "en" else ""
    NT = (lambda n: NOTES_EN[n["slug"]]) if lang == "en" else (lambda n: n)
    notes = "".join(
        f'<a class="nc" style="--sc:{SERIES[n["series"]]}" href="{n["slug"]}.html"><img src="{P}img/lab/{LAB_IMG[n["slug"]]}-cover.jpg" width="540" height="960" alt="" loading="lazy">'
        f'<div class="nb"><div class="c">{n["series"]} LAB {n["no"]}</div><div class="t">{NT(n)["title"]}</div></div></a>'
        for n in reversed(NOTES[-3:]))
    idx = []
    for i in ISLANDS:
        li = I(i, lang)
        idx.append(dict(t=li["kr"], k=f'{li["kr"]} {i["en"]} {i["kr"]} {li["line"]}', s=h["s_isl"], u=f'island-{i["slug"]}.html'))
    for o0 in ORIGINS:
        o = O(o0, lang); il = I(IS[o0["island"]], lang)["kr"]
        idx.append(dict(t=o["title"], k=f'{o["title"]} {o["short"]} {o0["en"]} {o0["title"]} {il} {" ".join(o["chips"])} {" ".join(v for k, v in o["specs"])} {o["kind"]}',
                        s=h["s_org"].format(il), u=f'{o0["slug"]}.html'))
    for n in NOTES:
        nt = NT(n)
        idx.append(dict(t=re.sub("<[^>]+>", "", nt["title"]), k=f'{nt["title"]} {nt["desc"]} {n["series"]}', s=h["s_story"], u=f'{n["slug"]}.html'))
    if lang == "ko":
        for g, t, al, d, u, a in all_terms():
            idx.append(dict(t=t, k=f"{t} {al} {d}", s="용어", d=d, u=f"glossary.html#{a}"))
    for t, k, u in h["tools_idx"]:
        idx.append(dict(t=t, k=k, s=h["s_tool"], u=u))
    for d in idx:
        d["k"] = re.sub("<[^>]+>", " ", d["k"]).lower()
    n_docs = len(ORIGINS) + len(ISLANDS) + len(NOTES)
    ext = 'target="_blank" rel="noopener"'
    tools = "".join(f'<a class="tl" href="{u}" style="--tc:{TOOL_ICON[ic][0]}"><div class="ti"><svg viewBox="0 0 48 48" aria-hidden="true">{TOOL_ICON[ic][1]}</svg></div><div class="tb"><div class="h">{t}</div><div class="d">{d}</div></div></a>' for ic, u, t, d in h["tl"])
    yt = (f'<a class="yt" href="{YOUTUBE_URL}" target="_blank" rel="noopener"><span class="yp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 7l8 5-8 5z" fill="#fff"/></svg></span><span><b>{h["yt"]}</b><small>{h["yt_s"]}</small></span><span class="ya">→</span></a>') if YOUTUBE_URL else ""
    yt += (f'<a class="yt ig" href="https://www.instagram.com/ayutacoffee/" target="_blank" rel="noopener"><span class="yp"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="#fff" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="5"/><circle cx="12" cy="12" r="3.6"/><circle cx="16.8" cy="7.2" r=".9" fill="#fff" stroke="none"/></svg></span><span><b>{h["ig"]}</b><small>@ayutacoffee</small></span><span class="ya">→</span></a>')
    contact = contact_link() if lang == "ko" else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
{meta(h["title"], h["desc"], "", lang=lang)}
<style>{HOME_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="brand"><svg viewBox="0 0 24 24" fill="none"><ellipse cx="12" cy="12" rx="6" ry="9" transform="rotate(32 12 12)" stroke="#5e7338" stroke-width="1.8"/><path d="M9.6 5.5c1.6 3.8 1.6 9.2 0 13" transform="rotate(32 12 12)" stroke="#5e7338" stroke-width="1.8" stroke-linecap="round"/></svg>AYUTA COFFEE LAB</div>
    {lang_switch("index.html", lang)}
  </div>

  <header>
    <h1>{h["h1"]}</h1>
    <p class="sub">{h["sub"]}</p>
    <div class="search" role="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <input id="q" type="search" placeholder="{h["ph"]}" aria-label="{h["qaria"]}" autocomplete="off">
    </div>
    <div class="res" id="res"></div>
    <div class="count">{h["count"].format(n_docs)}{h["gl"]}</div>
  </header>

  <div class="label" id="islands">{h["by_isl"]}</div>
  {island_map(lang)}

  <div class="label">{h["lab"]}</div>
  <h2 class="sech">{h["lab_h"]}</h2>
  <div class="notes">{notes}</div>
  <div class="more"><a href="lab.html">{h["more"]}</a></div>
  {yt}

  <div class="label">{h["tools"]}</div>
  <div class="tools">{tools}</div>

  <div class="maker">
    <p>{h["maker"]}</p>
    <div class="mk">
      <a class="buy" href="https://www.ayutacoffee.com/" {ext}>{h["buy"]}</a>
      {contact}
      <a href="https://ayutatrading.com" {ext}>{h["co"]}</a>
    </div>
  </div>
  {h["foot"]}
</div>
<script>
(function(){{
  var IDX={json.dumps(idx, ensure_ascii=False)};
  var q=document.getElementById('q'),res=document.getElementById('res');
  function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  q.addEventListener('input',function(){{
    var v=q.value.trim().toLowerCase();
    if(!v){{res.style.display='none';res.innerHTML='';return;}}
    var ws=v.split(/\\s+/),hit=IDX.filter(function(d){{return ws.every(function(w){{return d.k.indexOf(w)>=0||d.t.toLowerCase().indexOf(w)>=0;}});}});hit.sort(function(a,b){{function r(d){{var t=d.t.toLowerCase();var k=' '+d.k.replace(/[()·,/]/g,' ')+' ';return t===v?0:t.indexOf(v)===0?1:k.indexOf(' '+v+' ')>=0?2:t.indexOf(v)>=0?3:4;}}return r(a)-r(b);}});hit=hit.slice(0,8);
    res.innerHTML=hit.length?hit.map(function(d){{return '<a href="'+d.u+'"><span class="rt">'+esc(d.t)+(d.d?'<em>'+esc(d.d)+'</em>':'')+'</span><small>'+esc(d.s)+'</small></a>';}}).join(''):'<div class="none">{h["none"]}</div>';
    res.style.display='block';
  }});
  q.addEventListener('keydown',function(e){{if(e.key==='Enter'){{var a=res.querySelector('a');if(a)location.href=a.getAttribute('href');}}}});
}})();
</script>
</body>
</html>
"""


def sitemap(paths):
    urls = "".join(f"<url><loc>{SITE}/{p}</loc></url>" for p in paths)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


if __name__ == "__main__":
    os.makedirs(f"{OUT}/en", exist_ok=True)
    paths = []
    for lang, d in (("ko", OUT), ("en", OUT + "/en")):
        pre = "en/" if lang == "en" else ""
        paths.append(pre)
        for o in ORIGINS:
            open(f"{d}/{o['slug']}.html", "w").write(origin_page(o, lang)); paths.append(pre + o["slug"])
        for i in ISLANDS:
            open(f"{d}/island-{i['slug']}.html", "w").write(island_page(i, lang)); paths.append(pre + "island-" + i["slug"])
        open(f"{d}/index.html", "w").write(home(lang))
        if lang == "ko":
            open(f"{d}/glossary.html", "w").write(glossary_page()); paths.append("glossary")
        paths += [pre + "lab"] + [pre + n["slug"] for n in NOTES]
    paths += ["indonesia_origin_map", "bean_catalog", "cafe_pricing", "recipe", "recipe_vanilla_sugar"]
    open(f"{OUT}/sitemap.xml", "w").write(sitemap(paths))
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("origins", len(ORIGINS), "islands", len(ISLANDS), "pages", len(paths))
