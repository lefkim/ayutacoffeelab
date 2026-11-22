# 아유타 커피랩 생성 코드

사이트의 일부 페이지는 이 폴더의 파이썬 코드로 만들어요. 고칠 때는 HTML을 직접 고치지 말고 여기를 고친 뒤 다시 만들어요.

| 파일 | 만드는 페이지 |
| --- | --- |
| `archive.py` | `index.html`(아카이브 메인), `island-*.html`(섬 6곳), `origin-*.html`(산지 16곳), `sitemap.xml`, `robots.txt` |
| `lab.py` | `lab.html`(LAB 노트 목록), `lab-*-001.html`(LAB 노트), `favicon.svg` |
| `recipe_hub.py` | `recipe.html`(홈 레시피 목록) |
| `origins.json` | 산지 16곳 자료 (`indonesia_origin_map.html`에서 꺼낸 것) |
| `mapgeo.json` | 메인 섬 지도용 지형 조각과 산지 핀 위치 |
| `common.py` | 공통 색·글꼴·공유 미리보기 태그 |

직접 만든 페이지(코드로 만들지 않음): `indonesia_origin_map.html`, `bean_catalog.html`, `cafe_pricing.html`, `recipe_vanilla_sugar.html`

## 다시 만들기

```bash
cd _src
python3 lab.py ..
python3 recipe_hub.py ..
LAB_CONTACT_EMAIL=협업메일주소 python3 archive.py ..
```

`LAB_CONTACT_EMAIL`을 주면 메인 맨 아래에 협업 메일 링크가 생겨요. 없으면 그 링크만 빠져요.

## 새 LAB 노트 더하기

`lab.py`의 `NOTES` 목록에 하나를 더하고 `lab.py`와 `archive.py`를 다시 돌려요. 섬과 이어지는 이야기면 `archive.py`의 `NOTE_ISLAND`에도 적어요.

이 폴더는 `.vercelignore`로 사이트에 올라가지 않아요.
