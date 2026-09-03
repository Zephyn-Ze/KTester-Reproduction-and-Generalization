import re

def is_main_conference(record, venue, config):
    exclude = [
        "companion",
        "workshop",
        "tutorial",
        "demo",
    ]
    name = record["display_name"].lower()
    for word in exclude:
        if word in name:
            return False
    if record["kind"] == "proceedings":
        url = record["part"].lower()
        stream_mapping = {
            "ase": "kbse",
            "fse": "sigsoft"
        }
        stream_key = stream_mapping.get(venue.lower(), venue.lower())
        if re.search(f"{stream_key}/\\d{{4}}(-\\d+)?$", url, re.IGNORECASE):
            return True
        return False
    else:
        if venue.lower() == record["issue"].lower():
            return True
    return False
