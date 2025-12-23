from modules.llm_client import query_llm, extract_json_from_text

def main():
    # Test prompt: very strict JSON
    messages = [
        {
            "role": "system",
            "content": (
                "You are a strict JSON generator. "
                "Return ONLY valid JSON. "
                "No explanations, no markdown."
            )
        },
        {
            "role": "user",
            "content": (
                "Generate a simple JSON object with keys: "
                "status (string) and working (boolean)."
            )
        }
    ]

    print("🔹 Sending request to LLM...\n")

    try:
        response_text = query_llm(messages)
        print("🔹 RAW LLM RESPONSE:")
        print(response_text)
        print("\n----------------------\n")

        parsed_json = extract_json_from_text(response_text)

        if parsed_json is None:
            print("❌ Failed to extract valid JSON")
        else:
            print("✅ Extracted JSON successfully:")
            print(parsed_json)

    except Exception as e:
        print("❌ Error while testing LLM client:")
        print(str(e))


if __name__ == "__main__":
    main()
