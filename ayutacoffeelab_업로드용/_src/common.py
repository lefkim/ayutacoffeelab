SITE = "https://ayutacoffeelab.com"
PHONE = "010-4263-4982"
STORE = "https://smartstore.naver.com/ayutatrading"

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Spline+Sans+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">"""


def meta(title, desc, path, image="og.png"):
    url = SITE + ("/" + path if path else "")
    return f"""<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="아유타 커피랩 · AYUTA COFFEE LAB" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{SITE}/{image}" />
<meta property="og:locale" content="ko_KR" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="theme-color" content="#f1e9db" />
<link rel="icon" href="favicon.svg" type="image/svg+xml" />
{FONTS}"""


BASE_CSS = """
  :root{--ink:#241c17;--ink-soft:#5b4d40;--paper:#f1e9db;--card:#fbf7ef;--line:#ddccb4;--line-soft:#e9ddca;
  --green:#5e7338;--green-deep:#465828;--roast:#b5651d;--mud:#9a8467;--cherry:#c24b3a;--vanilla:#a8862e;
  --kr:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard","Noto Sans KR",sans-serif;--mono:"Spline Sans Mono",ui-monospace,Menlo,monospace;}
  *{box-sizing:border-box} html,body{margin:0}
  body{background:var(--paper);color:var(--ink);font-family:var(--kr);line-height:1.55;-webkit-font-smoothing:antialiased;padding:0 0 64px;word-break:keep-all}
  .wrap{max-width:640px;margin:0 auto;padding:0 18px}
  .back{display:inline-flex;align-items:center;gap:6px;margin-top:20px;font-size:12.5px;color:var(--mud);text-decoration:none;font-weight:600}
  .back:hover{color:var(--green-deep)}
  header{padding:22px 0 4px;text-align:center}
  .eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--green-deep);font-weight:700;display:flex;align-items:center;justify-content:center;gap:10px}
  .eyebrow::before,.eyebrow::after{content:"";height:1px;width:22px;background:var(--line)}
  h1{font-size:clamp(24px,6.4vw,30px);letter-spacing:-.025em;margin:13px 0 8px;font-weight:800;line-height:1.25}
  .sub{color:var(--ink-soft);font-size:14.5px;margin:0;line-height:1.7}
  .label{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--mud);margin:32px 2px 0;display:flex;align-items:center;gap:10px}
  .label::after{content:"";flex:1;height:1px;background:var(--line)}
  .note{font-size:11.5px;color:var(--mud);margin:10px 4px 0;line-height:1.65}
  .cta{margin-top:34px;background:var(--ink);color:#f3ead9;border-radius:18px;padding:30px 24px;text-align:center;background-image:radial-gradient(rgba(241,233,219,.05) .7px,transparent .7px);background-size:13px 13px}
  .cta .eye{font-family:var(--mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#caa46f;font-weight:700}
  .cta h2{font-size:21px;font-weight:800;letter-spacing:-.02em;margin:11px 0 0;line-height:1.35}
  .cta p{color:#cdbfab;font-size:13.5px;margin:9px auto 0;max-width:420px;line-height:1.7}
  .cta .btns{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:18px}
  .btn{display:inline-flex;align-items:center;gap:8px;background:var(--roast);color:#fff;text-decoration:none;font-weight:700;font-size:14px;padding:12px 20px;border-radius:12px;border:0;cursor:pointer;font-family:inherit}
  .btn:hover{background:#c4701f}
  .btn2{display:inline-flex;align-items:center;gap:7px;background:#03c75a;color:#fff;text-decoration:none;font-weight:700;font-size:13.5px;padding:12px 20px;border-radius:12px}
  .btn3{display:inline-flex;align-items:center;gap:7px;background:transparent;color:#f3ead9;text-decoration:none;font-weight:700;font-size:13.5px;padding:11px 18px;border-radius:12px;border:1.5px solid #6b5a4a}
  .foot{margin-top:26px;text-align:center;font-family:var(--mono);font-size:11px;letter-spacing:.05em;color:var(--mud);line-height:1.9}
  .foot b{color:var(--ink-soft);font-weight:600}
  .foot a{color:var(--mud)}
"""

FOOT = f"""<div class="foot"><b>아유타 커피랩</b> · AYUTA COFFEE LAB<br>아유타커피 · <a href="tel:{PHONE}">{PHONE}</a></div>"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><rect width="24" height="24" rx="6" fill="#f1e9db"/><g transform="rotate(32 12 12)"><ellipse cx="12" cy="12" rx="5.6" ry="8.4" fill="none" stroke="#465828" stroke-width="2"/><path d="M9.8 5.8c1.5 3.6 1.5 8.8 0 12.4" fill="none" stroke="#465828" stroke-width="2" stroke-linecap="round"/></g></svg>"""
