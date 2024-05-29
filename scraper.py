import requests
from bs4 import BeautifulSoup

def scrape_text_from_url(url):
    """
    This function fetches content from the given URL and extracts all textual content found within <p> tags.

    Parameters:
        url (str): URL of the webpage to scrape.

    Returns:
        str: A string containing all the concatenated text extracted from paragraph tags.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all paragraph elements
        paragraphs = soup.find_all('p')
        extracted_text = ' '.join([para.get_text() for para in paragraphs])

        return extracted_text
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    url = "https://example.com/"
    extracted_text = scrape_text_from_url(url)
    print(extracted_text)
