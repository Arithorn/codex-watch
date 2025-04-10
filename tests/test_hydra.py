import requests
import os

HYDRA2_URL = "https://hydra.peet.top"  # Change if Hydra2 runs elsewhere
# Replace with your Hydra2 API key
API_KEY = os.environ.get("HYDRA_API_KEY")


def search_hydra(query, category="7020,8010", max_results=5):
    """
    Search Hydra2 for ebooks.
    Category 8000 = "Ebooks" (adjust based on your indexers' categories).
    """
    endpoint = f"{HYDRA2_URL}/api/"
    params = {
        "apikey": API_KEY,
        "q": query,
        "cat": category,
        "limit": max_results,
        "t": "search",
        "cachetime": 60,
        "o": "JSON"
    }
    headers = {"Accept": "application/json"}  # ← Critical for JSON response

    try:
        response = requests.get(endpoint, params=params, headers=headers)
        # print("--- Response ---")
        # print(response.text)
        response.raise_for_status()  # Check for HTTP errors
        results = response.json()
        # print("--- Results ---")
        # print(results)

        # Parse results
        ebooks = []
        for result in results['channel']['item']:
            ebooks.append({
                "title": result['title'],
                # "indexer": result['indexer'],
                "download_url": result["link"],  # For NZB download
            })

        return ebooks

    except Exception as e:
        print(f"Error searching Hydra2: {e}")
        return []


# Example usage
if __name__ == "__main__":
    query = "Primal Hunter 11 epub"
    ebooks = search_hydra(query)

    for idx, ebook in enumerate(ebooks, 1):
        print(f"{idx}. {ebook['title']}")
        # print(f"   Size: {ebook['size']} | Age: {ebook['age']} days")
        # print(f"   Indexer: {ebook['indexer']}")
        print(f"   Download: {ebook['download_url']}\n")
