import re


def clean_text(text: str) -> str:
    """Remove noise from scraped web content."""
    text = re.sub(r'<[^>]*?>', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9 .,;:\-\'\"()\n]', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = text.strip()
    text = ' '.join(text.split())
    return text


def split_subject_body(email_text: str):
    """
    Split an email string that starts with 'Subject: ...\n\n...'
    into (subject, body). Returns (None, full_text) if no subject line.
    """
    if email_text.strip().lower().startswith("subject:"):
        lines = email_text.strip().split("\n", 2)
        subject = lines[0].replace("Subject:", "").replace("subject:", "").strip()
        body    = lines[2].strip() if len(lines) > 2 else ""
        return subject, body
    return None, email_text


def truncate(text: str, max_chars: int = 300, suffix: str = "…") -> str:
    """Truncate text to max_chars."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rsplit(" ", 1)[0] + suffix


def skills_to_list(skills_str: str) -> list:
    """Convert comma-separated skills string to a cleaned list."""
    return [s.strip() for s in skills_str.split(",") if s.strip()]


def verdict_emoji(verdict: str) -> str:
    mapping = {
        "Strong Fit": "🟢",
        "Good Fit":   "🔵",
        "Partial Fit":"🟡",
        "Weak Fit":   "🔴",
    }
    return mapping.get(verdict, "⚪")