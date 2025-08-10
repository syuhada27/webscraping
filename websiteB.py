# website B (PIB Library)
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Set this flag to True to disable SSL verification (for testing purposes)

def scrape_website_pib(title=None):

    encoded_query = quote(f"{{{title}}}") 

    url = f"https://e-ilami.unissa.edu.bn:8443/discover?query={encoded_query}"

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the <a> tag with the class "title" and dir="ltr"
        book_links = soup.find_all('div', class_='row ds-artifact-item')    

        scraped_data = []
        for book_link in book_links:

            # Extract the text inside the <h4> tag including the <strong> tag content
            title_element = book_link.find('h4')

            # Extract the full title by getting the text including the <strong> tag
            if title_element:
                title = title_element.get_text(strip=True)
            else:
                title = "Title Not Found"
    
                # Find the <span> tag with the class "author h4"
            author_element = book_link.find('span', class_='author h4')

            # Extract the author's name from the nested <span> tag
            if author_element:
                author = author_element.find('span').get_text(strip=True)
            else:
                author = "Author Not Found"

            scraped_data.append({
                "Title": title,
                "Author": author,
                # "Year": year,
                # "Availability": availability_label,
                # "Link": full_url  # Include the full URL in the dictionary
            })

        return scraped_data

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

