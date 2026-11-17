import pandas as pd
from datetime import datetime
from fetch_data import fetch_hn_stories
from analyze_trends import ask_gemini_for_signals

LOG_FILE = "trends_log.csv"

def save_signals(keyword="SaaS layoffs hiring", how_many=20):
    headlines = fetch_hn_stories(keyword, num_results=how_many)
    signals = ask_gemini_for_signals(headlines)["signals"]

    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_rows = []
    for signal in signals:
        new_rows.append({
            "date": today,
            "company": signal["company"],
            "signal_type": signal["signal_type"],
            "description": signal["description"]
        })

    new_data = pd.DataFrame(new_rows)

    try:
        old_data = pd.read_csv(LOG_FILE)
        all_data = pd.concat([old_data, new_data], ignore_index=True)
    except FileNotFoundError:
        all_data = new_data

    all_data.to_csv(LOG_FILE, index=False)
    print(f"Saved {len(new_rows)} signals to {LOG_FILE}")
    return all_data

if __name__ == "__main__":
    all_data = save_signals()
    print(all_data.tail(3))
