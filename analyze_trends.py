import os
import json
from dotenv import load_dotenv
from google import genai
from fetch_data import fetch_hn_stories

load_dotenv()


def ask_gemini_for_signals(headlines, client=None):
    # only connect to gemini when we need it (so the tests work without a key)
    if client is None:
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    title_list = "\n".join(f"- {story['title']}" for story in headlines)

    prompt = f"""Here are recent Hacker News headlines about SaaS company hiring and layoffs:

{title_list}

Find up to 3 real hiring or layoff signals in these headlines.
For each one, give the company name (or "unspecified" if not named), whether it's hiring or a layoff, and a short explanation.

Reply with ONLY valid JSON, nothing else, like this:
{{
  "signals": [
    {{"company": "name", "signal_type": "hiring or layoff", "description": "short explanation"}}
  ]
}}

If the headlines don't have 3 real signals, just return fewer. Don't make any up."""

    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
    reply = response.text.strip()

    # sometimes gemini puts ```json around the answer, so take it off
    reply = reply.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    return json.loads(reply)


if __name__ == "__main__":
    headlines = fetch_hn_stories("SaaS layoffs hiring", num_results=20)
    signals = ask_gemini_for_signals(headlines)["signals"]

    for i, signal in enumerate(signals, start=1):
        print(f"{i}. [{signal['signal_type'].upper()}] {signal['company']}")
        print(f"   {signal['description']}\n")
