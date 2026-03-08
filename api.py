import requests

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
# Persistent session for faster subsequents requests
session = requests.Session()

def get_cat_info():
    """Fetches the image URL from the API."""
    try:
        response = session.get(CAT_API_URL, timeout=5)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"API Error: {e}")
        return None

def get_cat_bytes():
    """Fetches the actual image data (bytes)"""
    url = get_cat_info()[0]['url']
    if not url:
        return None

    try:
        img_response = session.get(url, timeout=5)
        img_response.raise_for_status()
        return img_response.content
    except requests.exceptions.RequestException as e:
        print(f"API Error (Image download): {e}")
        return None