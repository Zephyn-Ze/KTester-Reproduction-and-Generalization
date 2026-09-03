def generate_manifest_template(inventory, venue):
    manifest = {venue: {}}
    for record in inventory:
        year = record["year"]
        if year not in manifest[venue]:
            manifest[venue][year] = []
        if record["kind"] == "proceedings":
            manifest[venue][year].append(
                {
                    "kind":"proceedings",
                    "part":record["part"],
                    "display_name":record["part_title"],
                    "paper_count":record["paper_count"],
                }
            )
        else:
            display_name = (
                f"{record['journal']} "
                f"volume {record['volume']} "
                f"issue {record['issue']}"
            )
            manifest[venue][year].append(
                {
                    "kind":"journal",
                    "journal":record["journal"],
                    "display_name":display_name,
                    "volume":record["volume"],
                    "issue":record["issue"],
                    "paper_count":record["paper_count"],
                }
            )
    return manifest
