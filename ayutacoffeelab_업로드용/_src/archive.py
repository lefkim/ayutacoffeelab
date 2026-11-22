"""아유타 커피랩 아카이브 생성기: 섬 페이지 + 산지 사전 페이지 + 메인 + sitemap"""
import json, re, sys, html, os
from common import *
from lab import NOTES, SERIES
from archive_contact import contact_link

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


def page(title, desc, path, body, ic="#465828"):
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta(title, desc, path)}
<style>{CSS}
  :root{{--ic:{ic}}}
</style>
</head>
<body>
<div class="wrap">
{body}
<div class="foot"><b>아유타 커피랩</b> · AYUTA COFFEE LAB<br>인도네시아 커피·바닐라 아카이브</div>
</div>
</body>
</html>
"""


def spec_rows(o):
    rows = [("섬", f'<a href="island-{o["island"]}.html" style="color:inherit">{IS[o["island"]]["kr"]}</a>'), ("종류", o["kind"])] + o["specs"]
    return "".join(f'<div class="tr"><div class="k">{k}</div><div class="v">{v}</div></div>' for k, v in rows)


def ocard(o, cur=None):
    c = " cur" if cur and cur["slug"] == o["slug"] else ""
    small = "<small>로부스타</small>" if o["kind"] == "로부스타" else ""
    return f'<a class="oc{c}" style="--ic:{IS[o["island"]]["color"]}" href="{o["slug"]}.html"><div class="t">{o["short"]}{small}</div><div class="d">{" · ".join(o["chips"][:3])}</div></a>'


def origin_page(o):
    isl = IS[o["island"]]
    alt = re.sub(r"\s*\(.*?\)", "", o["specs"][1][1])
    desc = f'{o["title"]} 산지 정보: {isl["kr"]} {o["specs"][0][1]}, 고도 {alt}, {o["specs"][2][1]}. 향미 {", ".join(o["chips"][:3])}.'
    desc = html.escape(re.sub("<[^>]+>", "", desc), quote=True)
    ay = ""
    if o["ayuta"]:
        note = f'<p>{o["ayuta"]["note"]}</p>' if o["ayuta"]["note"] else ""
        ay = f'''<div class="label">아유타가 들여오는 로트</div>
  <div class="ayuta"><div class="h">AYUTA LOT</div><div class="lot">{o["ayuta"]["lot"]}</div>{note}
  <a href="https://www.ayutacoffee.com/" target="_blank" rel="noopener">아유타커피에서 보기 →</a></div>'''
    others = [x for x in isl["origins"] if x is not o]
    sib = (f'<div class="label">{isl["kr"]}의 다른 산지</div><div class="olist">' + "".join(ocard(x) for x in others) + "</div>") if others else ""
    body = f'''  <div class="crumb"><a href="index.html">아유타 커피랩</a><span>›</span><a href="island-{isl["slug"]}.html">{isl["kr"]}</a><span>›</span>{o["short"].split(" · ")[-1]}</div>
  <header>
    <div class="eyebrow">{isl["kr"]} · 커피 산지 {o["no"]:02d}</div>
    <h1>{o["title"]}<span class="kind">{o["kind"]}</span></h1>
    <div class="en">{o["en"]} · {isl["en"]}, Indonesia</div>
    <p class="lead">{o["memo"]}</p>
  </header>

  <div class="label">향미</div>
  <div class="chips">{"".join(f"<span>{c}</span>" for c in o["chips"])}</div>
  <p class="note">※ 향미는 일반적인 경향이에요. 로트와 가공에 따라 달라져요.</p>

  <div class="label">산지 정보</div>
  <div class="tbl">{spec_rows(o)}</div>

  {ay}

  {sib}
  <div class="btnrow">
    <a class="lb" href="island-{isl["slug"]}.html">{isl["kr"]} 섬 이야기 →</a>
    <a class="lb" href="indonesia_origin_map.html#r-{o["no"]}">지도에서 보기 →</a>
  </div>

  <p class="src">출처: {MAP_SRC} · 아유타 로트·거래 농장 노트는 아유타 직접 거래처 정보</p>'''
    return page(f'{o["title"]} · {isl["kr"]} 커피 산지 | 아유타 커피랩', desc, o["slug"], body, isl["color"])


def island_page(isl):
    ol = "".join(ocard(o) for o in isl["origins"])
    notes = [n for n in NOTES if isl["slug"] in NOTE_ISLAND.get(n["slug"], [])]
    nb = ""
    if notes:
        nb = '<div class="label">관련 이야기</div><div class="olist">' + "".join(
            f'<a class="oc" style="--ic:{SERIES[n["series"]]}" href="{n["slug"]}.html"><div class="t">{n["title"]}</div><div class="d">{n["series"]} LAB {n["no"]}</div></a>' for n in notes) + "</div>"
    others = "".join(f'<a class="lb" href="island-{x["slug"]}.html">{x["kr"]}</a>' for x in ISLANDS if x is not isl)
    names = ", ".join(o["short"].split(" · ")[-1] for o in isl["origins"])
    desc = html.escape(f'인도네시아 {isl["kr"]}({isl["en"]}) 커피 산지와 문화 정리. {names}. {isl["line"]}', quote=True)
    body = f'''  <div class="crumb"><a href="index.html">아유타 커피랩</a><span>›</span>{isl["kr"]}</div>
  <header>
    <div class="eyebrow">인도네시아의 섬</div>
    <h1>{isl["kr"]}</h1>
    <div class="en">{isl["en"]}, Indonesia</div>
    <p class="lead">{isl["line"]}</p>
  </header>

  <div class="label">커피 산지 · {len(isl["origins"])}</div>
  <div class="olist">{ol}</div>

  <div class="label">알아 두면 좋은 것</div>
  <ul class="facts">{"".join(f"<li>{f}</li>" for f in isl["facts"])}</ul>

  {nb}

  <div class="label">다른 섬</div>
  <div class="btnrow">{others}</div>
  <div class="btnrow"><a class="lb" href="indonesia_origin_map.html">산지 지도 열기 →</a></div>

  <p class="src">출처: <a href="{isl["wiki"]}" target="_blank" rel="noopener">{isl["en"]} (Wikipedia)</a> · 산지 자료: {MAP_SRC}</p>'''
    return page(f'{isl["kr"]} 커피와 문화 · 인도네시아 {isl["kr"]} | 아유타 커피랩', desc, "island-" + isl["slug"], body, isl["color"])


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
  .res .none{padding:12px 15px;font-size:13.5px;color:var(--mud)}
  .count{font-family:var(--mono);font-size:11px;color:var(--mud);letter-spacing:.08em;margin-top:12px}
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
  .notes{display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin-top:18px}
  @media(max-width:640px){.notes{grid-template-columns:1fr}}
  .nc{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--sc);border-radius:14px;padding:14px 15px;text-decoration:none;color:inherit}
  .nc:hover{border-color:var(--roast)}
  .nc .c{font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.12em;color:var(--sc)}
  .nc .t{font-size:15px;font-weight:800;letter-spacing:-.01em;line-height:1.4;margin-top:5px}
  .more{text-align:center;margin-top:12px} .more a{font-size:13px;font-weight:700;color:var(--green-deep);text-decoration:none}
  .tools{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-top:18px}
  @media(max-width:640px){.tools{grid-template-columns:1fr 1fr}}
  .tl{display:block;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:13px 14px;text-decoration:none;color:inherit}
  .tl:hover{border-color:var(--roast)}
  .tl .h{font-size:14.5px;font-weight:800} .tl .h::after{content:" →";color:var(--roast)}
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


def island_map():
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
        g.append(f'<g class="isg" data-i="{i["slug"]}" tabindex="0" role="button" aria-label="{i["kr"]} 확대" style="--c:{i["color"]}"><path d="{" ".join(groups[i["slug"]])}"/></g>')
    # 산지 핀: 섬을 고르면 이름과 함께 나타남. 겹치지 않게 좌우를 번갈아 둠
    pins = []
    for i in ISLANDS:
        for n, o in enumerate(i["origins"]):
            x, y = GEO["pins"][str(o["no"])]
            side = {8: -1, 9: 1, 10: 1}.get(o["no"], 1 if n % 2 == 0 else -1)
            name = o["short"].split(" · ")[-1].split("/")[0]
            anchor = "start" if side > 0 else "end"
            pins.append(f'<a class="op" data-i="{i["slug"]}" href="{o["slug"]}.html" transform="translate({x} {y})" aria-label="{o["title"]}">'
                        f'<g class="sc"><circle r="5"/><text x="{9*side}" y="4.5" text-anchor="{anchor}">{name}</text></g></a>')
    dots = "".join(f'<circle class="dot" cx="{x}" cy="{y}" r="3.2"/>' for x, y in GEO["pins"].values())
    labels = {"sumatra": (95, 205), "java": (300, 330), "bali": (418, 340), "sulawesi": (668, 160), "nusa-tenggara": (560, 345), "papua": (845, 160)}
    lab = "".join(f'<text x="{x}" y="{y}">{IS[k]["kr"]}</text>' for k, (x, y) in labels.items())
    lab += '<text class="offt" x="380" y="120">칼리만탄</text><text class="offt" x="712" y="250">말루쿠</text>'
    data = {}
    for i in ISLANDS:
        x0, y0, x1, y1 = bbox(groups[i["slug"]] if i["slug"] != "papua" else groups[i["slug"]])
        if i["slug"] == "papua":  # 인도네시아 쪽(서쪽 절반) 위주로
            x1 = min(x1, 945)
        pad = max(x1 - x0, y1 - y0) * 0.18 + 14
        data[i["slug"]] = dict(kr=i["kr"], en=i["en"], c=i["color"], line=i["line"], box=[round(x0 - pad, 1), round(y0 - pad, 1), round(x1 - x0 + 2 * pad, 1), round(y1 - y0 + 2 * pad, 1)],
                               o=[dict(t=o["short"].split(" · ")[-1], u=o["slug"] + ".html", r=o["kind"] == "로부스타") for o in i["origins"]])
    chips = "".join(f'<button type="button" class="chip" data-i="{i["slug"]}" style="--c:{i["color"]}">{i["kr"]}</button>' for i in ISLANDS)
    return f"""<div class="imap" id="imap">
    <svg id="isvg" viewBox="0 0 960 352.7" role="group" aria-label="인도네시아 섬 지도. 섬을 누르면 확대돼요">{"".join(g)}{dots}<g class="lbl">{lab}</g>{"".join(pins)}</svg>
    <button type="button" class="back" id="iback">← 전체 지도</button>
  </div>
  <div class="ichips" role="group" aria-label="섬 고르기">{chips}</div>
  <div class="ipanel" id="ip" aria-live="polite"><div class="hint">지도에서 섬을 눌러 보세요. 그 섬의 커피 산지가 보여요.</div></div>
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
      ip.innerHTML='<div class="ph"><div><div class="pn">'+d.kr+'</div><div class="pe">'+d.en+'</div></div><a class="pg" href="island-'+k+'.html">섬 이야기 →</a></div>'
        +'<p class="pl">'+d.line+'</p><div class="pk">커피 산지 · '+d.o.length+'</div><div class="po">'
        +d.o.map(function(o){{return '<a href="'+o.u+'">'+o.t+(o.r?'<small>로부스타</small>':'')+'</a>';}}).join('')+'</div>';
    }}
    function reset(){{wrap.classList.remove('zoomed');document.querySelectorAll('.on').forEach(function(el){{el.classList.remove('on');}});
      go(FULL);ip.style.removeProperty('--c');ip.innerHTML='<div class="hint">지도에서 섬을 눌러 보세요. 그 섬의 커피 산지가 보여요.</div>';}}
    document.querySelectorAll('.isg,.chip').forEach(function(el){{
      el.addEventListener('click',function(){{pick(el.dataset.i);}});
      el.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();pick(el.dataset.i);}}}});
    }});
    document.getElementById('iback').addEventListener('click',reset);
    window.addEventListener('resize',function(){{var on=document.querySelector('.chip.on');setVB(on?fit(D[on.dataset.i].box):FULL);}});
    setVB(FULL);
  }})();
  </script>"""


def home():
    isl = "".join(
        f'<a class="ic" style="--c:{i["color"]}" href="island-{i["slug"]}.html"><div class="n">{i["kr"]}</div><div class="e">{i["en"]}</div>'
        f'<div class="o">{", ".join(o["short"].split(" · ")[-1] for o in i["origins"])}</div><div class="c">산지 {len(i["origins"])}곳 →</div></a>'
        for i in ISLANDS)
    notes = "".join(
        f'<a class="nc" style="--sc:{SERIES[n["series"]]}" href="{n["slug"]}.html"><div class="c">{n["series"]} LAB {n["no"]}</div><div class="t">{n["title"]}</div></a>'
        for n in reversed(NOTES[-3:]))
    idx = []
    for i in ISLANDS:
        idx.append(dict(t=i["kr"], k=f'{i["kr"]} {i["en"]} 섬 {i["line"]}', s="섬", u=f'island-{i["slug"]}.html'))
    for o in ORIGINS:
        idx.append(dict(t=o["title"], k=f'{o["title"]} {o["short"]} {o["en"]} {IS[o["island"]]["kr"]} {" ".join(o["chips"])} {" ".join(v for k, v in o["specs"])} {o["kind"]}',
                        s=f'{IS[o["island"]]["kr"]} · 산지', u=f'{o["slug"]}.html'))
    for n in NOTES:
        idx.append(dict(t=n["title"], k=f'{n["title"]} {n["desc"]} {n["series"]}', s="이야기", u=f'{n["slug"]}.html'))
    for t, k, u in [("인도네시아 커피 산지 지도", "지도 산지 map", "indonesia_origin_map.html"), ("커피 장사로 부자되는 계산기", "계산기 원가 카페 이익", "cafe_pricing.html"),
                    ("생두 도감", "생두 도감 green bean", "bean_catalog.html"), ("바닐라빈 슈가 만드는 법", "바닐라 레시피 설탕", "recipe_vanilla_sugar.html")]:
        idx.append(dict(t=t, k=k, s="도구·레시피", u=u))
    for d in idx:
        d["k"] = re.sub("<[^>]+>", " ", d["k"]).lower()
    n_docs = len(ORIGINS) + len(ISLANDS) + len(NOTES)
    ext = 'target="_blank" rel="noopener"'
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta("아유타 커피랩 · 인도네시아 커피·바닐라 아카이브", "인도네시아 커피 산지, 섬별 문화, 바닐라 이야기를 한국어로 정리한 아카이브. 수마트라·자바·발리·술라웨시·누사틍가라·파푸아의 커피 산지 16곳.", "")}
<style>{HOME_CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="top">
    <div class="brand"><svg viewBox="0 0 24 24" fill="none"><ellipse cx="12" cy="12" rx="6" ry="9" transform="rotate(32 12 12)" stroke="#5e7338" stroke-width="1.8"/><path d="M9.6 5.5c1.6 3.8 1.6 9.2 0 13" transform="rotate(32 12 12)" stroke="#5e7338" stroke-width="1.8" stroke-linecap="round"/></svg>AYUTA COFFEE LAB</div>
    <a href="indonesia_origin_map.html">산지 지도 →</a>
  </div>

  <header>
    <h1>인도네시아 <span class="g">커피</span>와 <span class="r">바닐라</span>,<br>한국어로 정리한 아카이브</h1>
    <p class="sub">인도네시아 커피 전문가가 산지에서 보고 배운 것을 섬별로 모았어요.</p>
    <div class="search" role="search">
      <svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
      <input id="q" type="search" placeholder="토라자, 가요, 길링 바사, 바닐라…" aria-label="아카이브 검색" autocomplete="off">
    </div>
    <div class="res" id="res"></div>
    <div class="count">자료 {n_docs}개 · 계속 쌓이는 중</div>
  </header>

  <div class="label">섬으로 찾기</div>
  {island_map()}

  <div class="label">LAB 노트</div>
  <h2 class="sech">쇼츠에서 본 이야기, 여기서 자세히</h2>
  <div class="notes">{notes}</div>
  <div class="more"><a href="lab.html">이야기 전체 보기 →</a></div>

  <div class="label">도구</div>
  <div class="tools">
    <a class="tl" href="indonesia_origin_map.html"><div class="h">산지 지도</div><div class="d">16곳을 지형 지도에서</div></a>
    <a class="tl" href="bean_catalog.html"><div class="h">생두 도감</div><div class="d">산지·가공·향미 카드</div></a>
    <a class="tl" href="cafe_pricing.html"><div class="h">카페 계산기</div><div class="d">한 잔의 원가와 이익</div></a>
    <a class="tl" href="recipe.html"><div class="h">홈 레시피</div><div class="d">바닐라빈 슈가부터</div></a>
  </div>

  <div class="maker">
    <p>아유타 커피랩은 인도네시아 커피와 바닐라빈을 들여오는 <b>아유타커피</b>가 만들어요.</p>
    <div class="mk">
      <a class="buy" href="https://www.ayutacoffee.com/" {ext}>원두·바닐라빈 → 아유타커피</a>
      {contact_link()}
      <a href="https://ayutatrading.com" {ext}>회사 → 아유타상사</a>
    </div>
  </div>
  <div class="foot"><b>아유타 커피랩</b> · AYUTA COFFEE LAB<br>(주)아유타상사 · Ayuta Trading Co., Ltd.</div>
</div>
<script>
(function(){{
  var IDX={json.dumps(idx, ensure_ascii=False)};
  var q=document.getElementById('q'),res=document.getElementById('res');
  function esc(s){{return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  q.addEventListener('input',function(){{
    var v=q.value.trim().toLowerCase();
    if(!v){{res.style.display='none';res.innerHTML='';return;}}
    var ws=v.split(/\\s+/),hit=IDX.filter(function(d){{return ws.every(function(w){{return d.k.indexOf(w)>=0||d.t.toLowerCase().indexOf(w)>=0;}});}}).slice(0,8);
    res.innerHTML=hit.length?hit.map(function(d){{return '<a href="'+d.u+'">'+esc(d.t)+'<small>'+esc(d.s)+'</small></a>';}}).join(''):'<div class="none">아직 없는 자료예요. 곧 채울게요.</div>';
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
    paths = [""]
    for o in ORIGINS:
        open(f"{OUT}/{o['slug']}.html", "w").write(origin_page(o)); paths.append(o["slug"])
    for i in ISLANDS:
        open(f"{OUT}/island-{i['slug']}.html", "w").write(island_page(i)); paths.append("island-" + i["slug"])
    open(f"{OUT}/index.html", "w").write(home())
    paths += ["lab"] + [n["slug"] for n in NOTES] + ["indonesia_origin_map", "bean_catalog", "cafe_pricing", "recipe", "recipe_vanilla_sugar"]
    open(f"{OUT}/sitemap.xml", "w").write(sitemap(paths))
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("origins", len(ORIGINS), "islands", len(ISLANDS))
