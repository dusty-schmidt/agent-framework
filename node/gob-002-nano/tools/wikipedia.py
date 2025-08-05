import requests

def run(arg: str) -> str:
    try:
        slug = "_".join(word.capitalize() for word in arg.split())
        resp = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{slug}")
        if resp.status_code == 200:
            data = resp.json()
            return data.get("extract", "No summary found.")
        return f"Not found ({resp.status_code})"
    except Exception as e:
        return f"Error: {e}"
