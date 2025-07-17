

def chatFunction(doc, result, data, expected_utilities):
    for i, token in enumerate(doc):
        # Handle '1 bed', '2 bathroom', etc.
        if token.like_num:
            next_token = doc[i + 1].text.lower() if i + 1 < len(doc) else ""
            if "bed" in next_token:
                result["bed"] = int(token.text)
            elif "bath" in next_token:
                result["bath"] = int(token.text)

        # Handle 'Dublin 6' (separate tokens)
        if token.text.lower() == "dublin" and i + 1 < len(doc):
            next_token = doc[i + 1]
            if next_token.like_num:
                result["location"] = f"Dublin {next_token.text}"

        # Fallback: handle 'dublin6' (single token)
        if token.text.lower().startswith("dublin") and token.text[-1].isdigit():
            result["location"] = token.text.title()

    expected_utilities_lower = [item.lower() for item in expected_utilities]

    for util in expected_utilities_lower:
        if util in data.text.lower():
            result["utilities"].append(util.title())

    return result

    