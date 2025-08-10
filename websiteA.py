# Website A (UTB Library)
import requests
from bs4 import BeautifulSoup

# Set this flag to True to disable SSL verification (for testing purposes)
DISABLE_SSL_VERIFICATION = True

def scrape_website_utb(title=None):
    base_url = f"https://utbopac.library.utb.edu.bn/cgi-bin/koha/opac-search.pl?idx=&q={title}&weight_search=1"

    try:
        # Disable SSL verification if the flag is set
        response = requests.get(base_url, verify=not DISABLE_SSL_VERIFICATION)
        response.raise_for_status()

        # Continue with your code to parse and handle the response
        soup = BeautifulSoup(response.text, 'html.parser')
        book_links = soup.find_all('a', class_='title')

        scraped_data = []
        for book_link in book_links:
            title = book_link.text.strip()
            biblionumber = book_link['href'].split('=')[-1]  # Extract the biblionumber from the href attribute

            # Find the span with the class 'author'
            author_span = book_link.find_next('span', class_='author')
            if author_span:
                # Extract text content from all elements inside the 'author' span
                author_text_parts = [part.strip() for part in author_span.stripped_strings]
                # Concatenate the text parts to get the complete author information
                author = ' '.join(author_text_parts)
            else:
                author = 'Author not found'

            # Find the span with the class 'results_summary publisher'
            publisher_span = book_link.find_next('span', class_='results_summary publisher')
            if publisher_span:
                # Extract individual details from the 'results_summary publisher' span
                location_span = publisher_span.find('span', class_='publisher_place')
                location = location_span.text.strip() if location_span else 'Location not found'
                
                publisher_name_span = publisher_span.find('span', class_='publisher_name')
                publisher_name = publisher_name_span.text.strip() if publisher_name_span else 'Publisher name not found'

                date_published_span = publisher_span.find('span', class_='publisher_date')
                date_published = date_published_span.text.strip() if date_published_span else 'Date published not found'

                # Concatenate the extracted details to get the complete publication details
                publication_details = f"{location} {publisher_name} {date_published}"
            else:
                publication_details = 'Publisher information not found'
            
            # Extract availability information
            availability_label = book_link.find_next('span', class_='AvailabilityLabel').text.strip()
            item_branch = book_link.find_next('span', class_='ItemBranch').text.strip()

            # Construct the correct URL for the original UTB website using the biblionumber
            original_url = f"https://utbopac.library.utb.edu.bn/cgi-bin/koha/opac-detail.pl?biblionumber={biblionumber}"

            scraped_data.append({
                "Title": title,
                "Author": author,
                "Publication Details": publication_details,
                "Availability": availability_label,
                "ItemBranch": item_branch,
                "Link": original_url  # Use the constructed URL as the link
            })

        return scraped_data

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}
