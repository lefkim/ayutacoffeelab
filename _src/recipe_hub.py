import base64, sys
from common import *

CSS = BASE_CSS + """
  .lede{color:var(--ink-soft);font-size:13.5px;line-height:1.8;text-align:center;margin:14px auto 0;max-width:470px}
  .list{display:flex;flex-direction:column;gap:11px;margin-top:22px}
  .rc{display:flex;gap:14px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px;text-decoration:none;color:inherit;transition:transform .15s,box-shadow .15s}
  a.rc:hover{transform:translateY(-2px);box-shadow:0 10px 24px -14px rgba(36,28,23,.4);border-color:var(--roast)}
  .rc .ph{flex:none;width:84px;height:84px;border-radius:11px;overflow:hidden;background:#efe7d6;border:1px solid var(--line-soft);display:grid;place-items:center;color:var(--mud)}
  .rc .ph img{width:100%;height:100%;object-fit:cover;display:block}
  .rc .ph svg{width:30px;height:30px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round;opacity:.6}
  .rc .b{flex:1;min-width:0}
  .rc .k{font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.12em;color:var(--green-deep)}
  .rc .t{font-size:16px;font-weight:800;letter-spacing:-.015em;margin-top:4px;line-height:1.35}
  .rc .d{font-size:12.5px;color:var(--ink-soft);margin-top:4px;line-height:1.55}
  .rc.soon{opacity:.65}
  .badge{flex:none;align-self:flex-start;font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.08em;padding:3px 8px;border-radius:20px;white-space:nowrap;color:var(--mud);background:#efe6d4;border:1px solid var(--line)}
  @media(prefers-reduced-motion:reduce){.rc{transition:none}a.rc:hover{transform:none}}
"""

CUP = '<svg viewBox="0 0 24 24"><path d="M5 9h11v4a5 5 0 0 1-5 5H10a5 5 0 0 1-5-5V9z"/><path d="M16 10h2a2 2 0 0 1 0 4h-2"/></svg>'


def page():
    return f"""<!doctype html>
<html lang="ko">
<head>
{meta("아유타커피 홈 레시피 · 아유타 커피랩", "아유타커피의 원두와 바닐라빈으로, 집에서 누구나 쉽게 따라 하는 레시피. 레시피는 계속 추가돼요.", "recipe", alt=False)}
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="index.html">← 아유타 커피랩</a>
  <header>
    <div class="eyebrow">HOME RECIPES</div>
    <h1>아유타커피 홈 레시피</h1>
    <p class="sub">누구나 쉽게 따라 하는, 아유타커피·바닐라빈 레시피</p>
    <p class="lede">복잡하지 않아요. 사진을 누르면 레시피가 열려요!<br>아유타커피랩은 지금도 새 레시피를 만들고 있어요.</p>
  </header>
  <div class="list">
    <a class="rc" href="recipe_vanilla_sugar.html">
      <div class="ph"><img src="recipe-vanilla-sugar.jpg" alt="유리병에 담긴 바닐라빈 슈가" width="84" height="84"></div>
      <div class="b"><div class="k">VANILLA</div><div class="t">바닐라빈 슈가 만드는 법</div><div class="d">바닐라빈 2줄기와 설탕 500g. 10분 만들고 1~2주 숙성해요.</div></div>
    </a>
    <div class="rc soon">
      <div class="ph">{CUP}</div>
      <div class="b"><div class="k">COFFEE</div><div class="t">드립커피 맛있게 내리는 법</div><div class="d">아유타 클린컵 로부스타로 내리는 핸드드립</div></div>
      <span class="badge">준비중</span>
    </div>
    <div class="rc soon">
      <div class="ph">{CUP}</div>
      <div class="b"><div class="k">VANILLA × COFFEE</div><div class="t">바닐라빈 라떼 (따뜻 · 아이스)</div><div class="d">직접 만든 바닐라빈 시럽으로 카페 맛 그대로</div></div>
      <span class="badge">준비중</span>
    </div>
  </div>
  <div class="cta">
    <div class="eye">레시피의 시작은 좋은 재료</div>
    <h2>아유타 원두와 바닐라빈</h2>
    <p>레시피에 쓰는 원두와 바닐라빈은 스마트스토어에서 만나 보세요.</p>
    <div class="btns"><a class="btn2" href="{STORE}" target="_blank" rel="noopener">스마트스토어 가기</a></div>
  </div>
  {FOOT}
</div>
</body>
</html>
"""


if __name__ == "__main__":
    open(sys.argv[1] + "/recipe.html", "w").write(page())
    print("ok")
