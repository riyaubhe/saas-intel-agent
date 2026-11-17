import time
import requests


def fetch_hn_stories(keyword, num_results=20):
    # search_by_date gives the newest stories first
    url = "https://hn.algolia.com/api/v1/search_by_date"

    # only get stories from the last 24 hours
    one_day_ago = int(time.time()) - 24 * 60 * 60

    params = {
        "query": keyword,
        "tags": "story",
        "hitsPerPage": num_results,
        "numericFilters": f"created_at_i>{one_day_ago}",
    }

    # give up after 10 seconds so it doesn't get stuck
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    stories = []
    for hit in data["hits"]:
        title = hit.get("title")
        if title:
            stories.append({"title": title, "url": hit.get("url"), "points": hit.get("points")})
    return stories


if __name__ == "__main__":
    results = fetch_hn_stories("layoffs", num_results=10)
    for i, story in enumerate(results, start=1):
        print(f"{i}. {story['title']} ({story['points']} points)")
