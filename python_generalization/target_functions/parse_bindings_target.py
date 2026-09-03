def parse_bindings(bindings, venue, year):
    papers = {}
    for item in bindings:
        if "publication" not in item or "authorName" not in item:
            continue
        url = item["publication"]["value"]
        title = item.get("title", {}).get("value")
        author = item["authorName"]["value"]
        if url not in papers:
            papers[url] = {
                "venue": venue,
                "title": title,
                "year": year,
                "url": url,
                "authors": []
            }
        if author not in papers[url]["authors"]:
            papers[url]["authors"].append(author)
    return list(papers.values())
