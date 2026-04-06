

# --- QUERY ---
def sanitize_query(q: str) -> str | None:
    if not q:
        return None
    q = q.strip()
    q = " ".join(q.split())
    return q[:500]


# --- IMAGE OUTPUT ---
def sanitize_image_output(text: str) -> str | None:
    if not text or len(text) > 2000:
        return None

    blacklist = ["ignore previous", "system prompt", "follow instructions"]
    if any(word in text.lower() for word in blacklist):
        return None

    return text
