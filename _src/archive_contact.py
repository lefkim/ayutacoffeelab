"""협업 연락처는 코드에 적지 않고 환경 변수 LAB_CONTACT_EMAIL에서 읽어요."""
import os

CONTACT = os.environ.get("LAB_CONTACT_EMAIL", "").strip()


def contact_link():
    if CONTACT:
        return f'<a href="mailto:{CONTACT}">협업 제안 → {CONTACT}</a>'
    return ""
