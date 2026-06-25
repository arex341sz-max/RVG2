# pages/public.py — صفحه پابلیک ساب‌گروه
# محتوای get_public_page_html از pages.py قبلی رو اینجا paste کن

def get_html(uuid_key: str) -> str:
    # همون HTML قبلی get_public_page_html(uuid_key)
    try:
        from pages_legacy import get_public_page_html
        return get_public_page_html(uuid_key)
    except ImportError:
        return f"<h2>صفحه عمومی: {uuid_key}</h2>"
