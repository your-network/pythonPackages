
def process_lookup_name(text: str) -> str:
    name = text.replace(' ', '_').lower()
    return name
