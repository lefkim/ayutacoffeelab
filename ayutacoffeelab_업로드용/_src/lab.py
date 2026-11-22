import html
from common import *

LAB_CSS = BASE_CSS + """
  .meta{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;color:var(--mud);margin-top:12px}
  .facts{display:flex;margin-top:14px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
  .fa{flex:1;padding:15px 8px;text-align:center} .fa+.fa{border-left:1px solid var(--line-soft)}
  .fa .l{font-size:11px;color:var(--mud);font-weight:600}
  .fa .v{font-family:var(--mono);font-size:15px;font-weight:700;color:var(--ink);margin-top:4px;line-height:1.3}
  .ch{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 18px 16px;margin-top:12px}
  .ch .n{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.14em;color:var(--sc)}
  .ch h2{font-size:17px;font-weight:800;letter-spacing:-.015em;margin:5px 0 0;line-height:1.4}
  .ch p{font-size:14.5px;color:var(--ink-soft);line-height:1.85;margin:9px 0 0}
  .ch p b{color:var(--ink)}
  .q{margin-top:14px;border:1.5px dashed var(--sc);border-radius:14px;padding:17px 18px;background:#fffdf8}
  .q .qq{font-size:15px;font-weight:800;line-height:1.45}
  .q details{margin-top:10px}
  .q summary{cursor:pointer;font-size:13px;font-weight:700;color:var(--sc);list-style:none}
  .q summary::-webkit-details-marker{display:none}
  .q summary::before{content:"▸ "} .q details[open] summary::before{content:"▾ "}
  .q .qa{font-size:14px;color:var(--ink-soft);line-height:1.8;margin:8px 0 0}
  .warn{font-size:12.5px;color:var(--cherry);background:#fbefe9;border:1px solid #efcdbf;border-radius:12px;padding:11px 14px;margin-top:12px;line-height:1.65}
  .src{margin:12px 4px 0;padding:0;list-style:none}
  .src li{font-size:12.5px;line-height:1.6;margin:0 0 6px;padding-left:14px;position:relative;color:var(--ink-soft)}
  .src li::before{content:"–";position:absolute;left:0;color:var(--mud)}
  .src a{color:var(--green-deep);word-break:break-all}
  .pn{display:flex;gap:10px;margin-top:22px}
  .pn a{flex:1;background:var(--card);border:1px solid var(--line);border-radius:13px;padding:12px 14px;text-decoration:none;color:inherit;min-width:0}
  .pn a:hover{border-color:var(--roast)}
  .pn .d{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;color:var(--mud)}
  .pn .t{font-size:13px;font-weight:700;margin-top:3px;line-height:1.4}
  .pn .nx{text-align:right}
"""

SERIES = {
    "VANILLA": "var(--vanilla)",
    "INDONESIA": "var(--green-deep)",
    "COFFEE": "var(--roast)",
}

NOTES = [
  dict(
    slug="lab-vanilla-001", series="VANILLA", no="001", date="2026.11",
    title="바닐라빈이 금값인 이유",
    sub="꽃은 단 하루, 수분은 사람 손으로 한 송이씩.<br>세계에서 두 번째로 비싼 향신료가 된 사연이에요.",
    desc="꽃은 단 하루만 피고, 열매는 사람이 손으로 수분해야 열립니다. 세계에서 두 번째로 비싼 향신료, 바닐라빈 이야기.",
    facts=[("꽃이 피는 시간","단 하루"),("수분","사람 손으로"),("숙성","수개월")],
    chapters=[
      ("사프란 다음으로 비싼 향신료",
       "바닐라빈은 <b>난초과 덩굴식물의 열매</b>예요. 원래 고향은 멕시코인데, 지금은 세계 여러 열대 지역에서 기릅니다. 향신료 가운데 바닐라보다 비싼 건 <b>사프란</b> 정도예요. 왜 이렇게 비쌀까요? 답은 꽃에 있어요."),
      ("꽃은 단 하루만 핍니다",
       "바닐라 꽃은 <b>피어 있는 시간이 하루 남짓</b>이에요. 그날 안에 꽃가루가 옮겨지지 않으면 열매가 맺히지 않아요. 고향 멕시코에는 이 일을 해 주는 곤충이 있지만, 다른 나라로 옮겨 심은 바닐라는 <b>꽃이 피어도 열매가 거의 열리지 않았어요.</b>"),
      ("1841년, 열두 살 소년의 손",
       "해답을 찾은 건 인도양의 레위니옹섬에 살던 <b>열두 살 소년 에드몽 알비우스</b>였어요. 가는 막대와 엄지손가락으로 꽃 한 송이씩 꽃가루를 옮기는 방법이었죠. 놀랍게도 <b>지금도 바닐라 농장에서는 거의 그대로 이 방법</b>을 씁니다. 꽃 한 송이 한 송이를 사람이 직접요."),
      ("갓 딴 열매에선 향이 안 나요",
       "수분에 성공해도 끝이 아니에요. 갓 딴 초록색 꼬투리에서는 <b>우리가 아는 바닐라 향이 거의 나지 않아요.</b> 데치고, 땀을 내듯 묵히고, 햇볕과 그늘에서 말리고, 다시 숙성하는 과정을 <b>수개월</b> 거쳐야 검고 촉촉한 바닐라빈이 됩니다."),
      ("1위 마다가스카르, 2위 인도네시아",
       "세계 바닐라 생산 1위는 마다가스카르, 2위는 <b>인도네시아</b>예요. 어디서 키우든 과정은 똑같아요. 하루뿐인 꽃, 사람 손으로 하는 수분, 몇 달의 숙성. 바닐라빈이 금값인 이유는 결국 <b>사람의 시간</b>이에요."),
    ],
    q=("집에 있는 '바닐라 향' 제품, 진짜 바닐라일까요?",
       "대부분은 아니에요. 시중의 '바닐라 향'은 바닐라빈에서 얻은 게 아니라 <b>따로 만든 바닐린</b>인 경우가 많아요. 성분표에 '바닐라빈', '바닐라 추출물'이 있는지 보면 구분할 수 있어요. 진짜 바닐라빈은 바닐린 말고도 수백 가지 향 성분이 함께 있어서 향이 훨씬 깊어요."),
    cta=dict(eye="아유타가 들여오는 바닐라빈", h="아유타 자바 바닐라빈",
             p="인도네시아 자바산 바닐라빈이에요. 집에서는 바닐라빈 슈가로, 카페에서는 시럽으로 써 보세요.",
             btns=[("recipe_vanilla_sugar.html","바닐라빈 슈가 만들기","btn"),(STORE,"바닐라빈 보러가기","btn2")]),
    sources=[("Vanilla (Wikipedia)","https://en.wikipedia.org/wiki/Vanilla"),
             ("Edmond Albius (Wikipedia)","https://en.wikipedia.org/wiki/Edmond_Albius")],
  ),
  dict(
    slug="lab-indonesia-001", series="INDONESIA", no="001", date="2026.11",
    title="인도네시아 이름에 '인도'가 들어간 이유",
    sub="인도와 붙어 있지도, 인도에 속한 적도 없는 나라.<br>그런데 왜 이름이 인도네시아일까요?",
    desc="인도와 땅이 붙어 있지도 않은 나라 이름에 왜 '인도'가 들어갔을까요? 1850년 학자들이 만든 이름이 나라 이름이 되기까지.",
    facts=[("이름이 생긴 해","1850년"),("뜻","인도 + 섬들"),("나라 이름이 된 해","1945년")],
    chapters=[
      ("유럽 사람들의 '인디즈'",
       "옛 유럽 사람들은 인도부터 중국 사이의 넓은 바다와 섬들을 통틀어 <b>'인디즈(the Indies)'</b>라고 불렀어요. 그래서 지금의 인도네시아는 오랫동안 <b>'네덜란드령 동인도'</b>로 불렸습니다. 이름부터 남이 붙인 이름이었던 거죠."),
      ("1850년, 학자가 만든 단어",
       "1850년, 싱가포르에서 활동하던 영국 학자 <b>제임스 로건</b>이 그리스어 <b>'인도스(인도)'</b>와 <b>'네소스(섬)'</b>를 합쳐 <b>'인도네시아'</b>라는 말을 썼어요. 뜻을 풀면 <b>'인도 쪽의 섬들'</b>이에요. 처음에는 지역을 가리키는 학술 용어였어요."),
      ("학자의 말에서 우리의 이름으로",
       "이 말을 자기 이름으로 받아들인 건 독립을 꿈꾸던 청년들이었어요. <b>1928년 '청년 맹세(숨파 프무다)'</b>에서 '하나의 조국, 하나의 민족, 하나의 언어, 인도네시아'를 외쳤고, <b>1945년 독립</b>과 함께 인도네시아는 정식 나라 이름이 됩니다. 식민지의 이름 대신, 스스로 고른 이름이었죠."),
      ("이름이 하나 더 있어요, 누산타라",
       "인도네시아 사람들에게는 더 오래된 이름도 있어요. 옛 자바어 <b>'누산타라'</b>, 풀면 '바깥의 섬들'이라는 뜻이에요. 지금도 '우리 섬나라'를 부를 때 자주 쓰고, 새로 짓고 있는 수도의 이름도 <b>누산타라</b>예요."),
    ],
    q=("이름에 다른 나라나 지역 이름이 숨어 있는 나라, 또 어디가 있을까요?",
       "인도네시아 바로 옆에 있어요. <b>파푸아뉴기니</b>의 '기니'는 아프리카 서쪽의 기니에서 왔어요. 16세기 유럽 탐험가가 이 섬 사람들이 아프리카 기니 사람들과 닮았다며 '새 기니'라고 불렀거든요. <b>뉴질랜드</b>도 네덜란드의 '제일란트' 지방에서 따온 이름이에요. 나라 이름에는 그 땅을 바라본 사람들의 시선이 담겨 있어요."),
    cta=dict(eye="섬마다 맛이 다른 나라", h="인도네시아 커피 산지 지도",
             p="수마트라, 자바, 발리, 술라웨시… 섬마다 다른 커피 산지를 실제 지형 지도에서 눌러 보세요.",
             btns=[("indonesia_origin_map.html","산지 지도 열기","btn")]),
    sources=[("Names of Indonesia (Wikipedia)","https://en.wikipedia.org/wiki/Names_of_Indonesia"),
             ("Nusantara (Wikipedia)","https://en.wikipedia.org/wiki/Nusantara"),
             ("Kompas, The Great Strides of Indonesia","https://www.kompas.id/baca/english/2020/10/28/the-great-strides-of-indonesia")],
  ),
  dict(
    slug="lab-coffee-001", series="COFFEE", no="001", date="2026.11",
    title="뜨거운 숯을 넣는 커피, 코피 조스",
    sub="족자카르타 기차역 앞 노점에서는<br>벌겋게 달군 숯을 커피잔에 그대로 넣어요.",
    desc="족자카르타 기차역 앞 노점의 명물, 뜨거운 숯을 넣는 커피 코피 조스. 이름의 유래부터 건강 이야기의 진실까지.",
    facts=[("도시","족자카르타"),("한 잔","5,000루피아"),("이름의 뜻","'조스!' 소리")],
    chapters=[
      ("기차역 앞, 수레 노점",
       "인도네시아 자바섬의 <b>족자카르타</b>. 기차역 앞 거리에는 밤마다 <b>앙크링안</b>이라 부르는 수레 노점이 늘어서요. 싼값에 간단한 음식과 커피를 파는 곳인데, 이 가운데 유명한 메뉴가 <b>한 잔에 5,000루피아</b>쯤 하는 코피 조스예요."),
      ("'조스!' 하는 소리",
       "만드는 법은 간단해요. 진하게 탄 커피에 화로에서 <b>벌겋게 달군 숯 한 덩이</b>를 그대로 넣어요. 숯이 커피에 닿는 순간 <b>'조스' 하는 소리</b>가 나는데, 이 소리가 그대로 이름이 됐어요. 코피는 인도네시아어로 커피예요."),
      ("속이 더부룩하던 상인의 우연",
       "전해지는 이야기로는 <b>속이 더부룩하던 노점 상인 릭 만</b>이 화로 속 숯을 커피에 빠뜨린 게 시작이었대요. 지금은 족자카르타에 가면 한 번은 마셔 본다는 <b>도시의 명물</b>이 됐어요."),
      ("속이 편해진다는 말, 사실일까요?",
       "현지에서는 숯이 속을 편하게 해 준다고들 하지만, <b>의학적으로 확인된 적은 없어요.</b> 2023년 말레이시아 보건 당국은 숯은 음식이 아니라며, <b>커피에 숯을 넣어 팔면 처벌받을 수 있다</b>고 경고하기도 했어요. 신기한 길거리 문화로 알아 두는 게 좋겠죠."),
    ],
    warn="※ 현지 문화를 소개하는 글이에요. 집에서 따라 하는 것은 권하지 않아요.",
    q=("숯이 들어간 커피, 기회가 된다면 마셔 보실 건가요?",
       "숯 맛보다 인도네시아 커피 자체가 궁금하다면, 아유타 생두 도감에서 섬과 산지마다 향미가 어떻게 다른지 먼저 살펴보세요. 같은 나라 커피인데도 꽤 달라요."),
    cta=dict(eye="인도네시아 커피, 숯 없이 맛보기", h="아유타 생두 도감",
             p="아유타가 직접 들여오는 인도네시아 생두를 산지·가공·향미별로 정리해 두었어요.",
             btns=[("bean_catalog.html","생두 도감 보기","btn"),(STORE,"원두 보러가기","btn2")]),
    sources=[("Kopi joss (Wikipedia)","https://en.wikipedia.org/wiki/Kopi_joss")],
  ),
]


def note_page(i):
    n = NOTES[i]
    sc = SERIES[n["series"]]
    code = f"{n['series']} LAB {n['no']}"
    facts = "".join(f'<div class="fa"><div class="l">{l}</div><div class="v">{v}</div></div>' for l, v in n["facts"])
    chs = "".join(
        f'<section class="ch"><div class="n">{k+1:02d}</div><h2>{h}</h2><p>{p}</p></section>'
        for k, (h, p) in enumerate(n["chapters"]))
    warn = f'<div class="warn">{n["warn"]}</div>' if n.get("warn") else ""
    q, a = n["q"]
    c = n["cta"]
    ext = lambda u: ' target="_blank" rel="noopener"' if u.startswith("http") else ""
    btns = "".join(f'<a class="{cls}" href="{u}"{ext(u)}>{t}</a>' for u, t, cls in c["btns"])
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in n["sources"])
    prev = NOTES[i-1] if i > 0 else None
    nxt = NOTES[i+1] if i < len(NOTES)-1 else None
    pn = '<nav class="pn">'
    pn += (f'<a href="{prev["slug"]}.html"><div class="d">← {prev["series"]} LAB {prev["no"]}</div><div class="t">{prev["title"]}</div></a>' if prev else '<a href="lab.html"><div class="d">← LAB 노트</div><div class="t">전체 목록</div></a>')
    pn += (f'<a class="nx" href="{nxt["slug"]}.html"><div class="d">{nxt["series"]} LAB {nxt["no"]} →</div><div class="t">{nxt["title"]}</div></a>' if nxt else '<a class="nx" href="lab.html"><div class="d">LAB 노트 →</div><div class="t">전체 목록</div></a>')
    pn += "</nav>"
    title = f"{n['title']} · {code} · 아유타 커피랩"
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta(title, n['desc'], n['slug'])}
<style>{LAB_CSS}
  :root{{--sc:{sc}}}
  .eyebrow{{color:var(--sc)}}
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="lab.html">← LAB 노트</a>
  <header>
    <div class="eyebrow">{code}</div>
    <h1>{n['title']}</h1>
    <p class="sub">{n['sub']}</p>
    <div class="meta">아유타 커피랩 · {n['date']}</div>
  </header>

  <div class="label">한눈에</div>
  <div class="facts">{facts}</div>

  <div class="label">이야기</div>
  {chs}
  {warn}

  <div class="label">궁금증 하나</div>
  <div class="q"><div class="qq">{q}</div><details><summary>아유타의 답 보기</summary><p class="qa">{a}</p></details></div>

  <div class="cta">
    <div class="eye">{c['eye']}</div>
    <h2>{c['h']}</h2>
    <p>{c['p']}</p>
    <div class="btns">{btns}</div>
  </div>

  <div class="label">참고</div>
  <ul class="src">{src}</ul>

  {pn}
  {FOOT}
</div>
</body>
</html>
"""


HUB_CSS = BASE_CSS + """
  .lede{color:var(--ink-soft);font-size:13.5px;line-height:1.8;text-align:center;margin:14px auto 0;max-width:470px}
  .filters{display:flex;flex-wrap:wrap;justify-content:center;gap:7px;margin-top:22px}
  .filters button{font-family:var(--mono);font-size:10.5px;font-weight:700;letter-spacing:.1em;padding:7px 12px;border-radius:20px;border:1px solid var(--line);background:var(--card);color:var(--ink-soft);cursor:pointer}
  .filters button[aria-pressed="true"]{background:var(--ink);color:#f3ead9;border-color:var(--ink)}
  .list{display:flex;flex-direction:column;gap:11px;margin-top:18px}
  .item{display:block;background:var(--card);border:1px solid var(--line);border-left:4px solid var(--sc);border-radius:14px;padding:16px 18px;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s}
  .item:hover{transform:translateY(-2px);box-shadow:0 10px 24px -14px rgba(36,28,23,.4)}
  .item .c{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.14em;color:var(--sc)}
  .item .t{font-size:16.5px;font-weight:800;letter-spacing:-.015em;margin-top:5px;line-height:1.4}
  .item .d{font-size:13px;color:var(--ink-soft);margin-top:6px;line-height:1.65}
  .soonrow{border:1px dashed var(--line);border-radius:14px;padding:14px 18px;text-align:center;font-size:12.5px;color:var(--mud)}
  @media(prefers-reduced-motion:reduce){.item{transition:none}.item:hover{transform:none}}
"""


def hub():
    items = "".join(
        f'<a class="item" data-s="{n["series"]}" style="--sc:{SERIES[n["series"]]}" href="{n["slug"]}.html">'
        f'<div class="c">{n["series"]} LAB {n["no"]}</div><div class="t">{n["title"]}</div><div class="d">{n["desc"]}</div></a>'
        for n in reversed(NOTES))
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta("LAB 노트 · 아유타 커피랩", "쇼츠로 본 커피와 바닐라, 인도네시아 이야기를 글로 자세히 정리했어요. 산지에서 보고 배운 이야기를 아유타 커피랩이 기록합니다.", "lab")}
<style>{HUB_CSS}</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">← 아유타 커피랩</a>
  <header>
    <div class="eyebrow">LAB NOTES</div>
    <h1>LAB 노트</h1>
    <p class="sub">쇼츠에서 본 이야기, 여기서 자세히</p>
    <p class="lede">인도네시아 커피 전문가가 산지에서 보고 배운 커피와 바닐라, 인도네시아 이야기를 기록해요. 새 노트는 계속 추가될 거예요.</p>
  </header>
  <div class="filters" role="group" aria-label="시리즈">
    <button aria-pressed="true" data-f="">전체</button>
    <button aria-pressed="false" data-f="COFFEE">COFFEE</button>
    <button aria-pressed="false" data-f="VANILLA">VANILLA</button>
    <button aria-pressed="false" data-f="INDONESIA">INDONESIA</button>
  </div>
  <div class="list">
    {items}
    <div class="soonrow">다음 LAB 노트를 준비하고 있어요</div>
  </div>
  {FOOT}
</div>
<script>
  document.querySelectorAll('.filters button').forEach(b=>b.addEventListener('click',()=>{{
    const f=b.dataset.f;
    document.querySelectorAll('.filters button').forEach(x=>x.setAttribute('aria-pressed',x===b));
    document.querySelectorAll('.item').forEach(it=>{{it.style.display=(!f||it.dataset.s===f)?'':'none'}});
  }}));
</script>
</body>
</html>
"""


if __name__ == "__main__":
    import sys
    out = sys.argv[1]
    for i, n in enumerate(NOTES):
        open(f"{out}/{n['slug']}.html", "w").write(note_page(i))
    open(f"{out}/lab.html", "w").write(hub())
    open(f"{out}/favicon.svg", "w").write(FAVICON)
    print("ok")
