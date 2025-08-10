#app.py BARU

# app.py
from flask import Flask, render_template, request
from websiteA import scrape_website_utb as scrape_website_a
#from websiteB import scrape_website_pib as scrape_website_b
from websiteC import scrape_website_unissa as scrape_website_c

app = Flask(__name__)

@app.route('/')
def index():
    # Get the search query parameter from the URL
    search_query = request.args.get('search_query', default=None, type=str)

    # Get the library selection from the URL
    library_selected = request.args.get('library_select', default='all', type=str)

    # If there is no search query, render the initial page without displaying results
    if not search_query:
        return render_template('index4.html', library_selected=library_selected, search_query='')

    # Based on the selected library, scrape data from the corresponding website
    if library_selected == 'utb':
        data_a = scrape_website_a(title=search_query)
        data_b = []
        data_c = []
    #elif library_selected == 'umk':
        #data_a = []
        #data_b = scrape_website_b(title=search_query)
        #data_c = []
    elif library_selected == 'unissa':
        data_a = []
        data_b = []
        data_c = scrape_website_c(title=search_query)
    else:
        # Scrape data from all websites
        data_a = scrape_website_a(title=search_query)
        #data_b = scrape_website_b(title=search_query)
        data_c = scrape_website_c(title=search_query)

    if "error" in data_a:
        return render_template('error.html', error_message=data_a["error"])
    #elif "error" in data_b:
        #return render_template('error.html', error_message=data_b["error"])
    elif "error" in data_c:
        return render_template('error.html', error_message=data_c["error"])
    else:
        return render_template('index4.html', data_a=data_a, data_c=data_c, library_selected=library_selected, search_query=search_query)
        #return render_template('index4.html', data_a=data_a, data_b=data_b, data_c=data_c, library_selected=library_selected, search_query=search_query)

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
