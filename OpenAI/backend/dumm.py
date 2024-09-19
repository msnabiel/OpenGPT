from urllib.parse import urlparse, parse_qs

def extract_user_id_from_url(url: str) -> str:
    """
    Extracts the user_id from the provided URL.

    Args:
    url (str): The URL containing user_id as a query parameter.

    Returns:
    str: The extracted user_id or 'default_user_id' if not found.
    """
    # Parse the URL and extract query parameters
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Get the user_id from the query parameters
    user_id = query_params.get('user_id', [None])[0]
    if user_id is None:
        user_id = "default_user_id"  # Default user ID if not found
    
    return user_id

# Example usage
url = "http://localhost:8000/?user_id=12345"
user_id = extract_user_id_from_url(url)
print(f"Extracted user_id: {user_id}")