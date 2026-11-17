import requests


def fetch_hn_stories(keyword, num_results=20):
    url = "https://hn.algolia.com/api/v1/search"
    params = {"query": keyword, "tags": "story", "hitsPerPage": num_results}

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
    results = fetch_hn_stories("SaaS layoffs hiring", num_results=10)
    for i, story in enumerate(results, start=1):
        print(f"{i}. {story['title']} ({story['points']} points)")
