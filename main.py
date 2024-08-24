from flask import Flask, request, render_template
from googlesearch import search
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_details(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string.strip() if soup.title and soup.title.string else 'No Title'
        description_tag = soup.find('meta', attrs={'name': 'description'})
        description = description_tag['content'].strip() if description_tag and 'content' in description_tag.attrs else 'No Description'
        
        return {'title': title, 'url': url, 'description': description}
    except Exception as e:
        return {'title': 'Error', 'url': url, 'description': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search_results():
    query = request.args.get('q')
    if not query:
        return "No query provided.", 400
    
    # Paginación
    page = int(request.args.get('page', 1))
    num_results = 10  # Número de resultados por página
    start = (page - 1) * num_results
    
    results = []
    try:
        # Convertir el generador a lista
        search_results = list(search(query, num_results=num_results * (page + 1)))
        results = [fetch_details(result_url) for result_url in search_results[start:start + num_results]]
        
        # Genera la paginación
        total_results = len(search_results)
        page_numbers = range(1, (total_results // num_results) + 2)
        prev_page = page - 1 if page > 1 else None
        next_page = page + 1 if (page * num_results) < total_results else None
    except Exception as e:
        return f"Error during search: {e}", 500
    
    return render_template('results.html', query=query, results=results, 
                           prev_page=prev_page, next_page=next_page, 
                           page_numbers=page_numbers, current_page=page)

if __name__ == '__main__':
    app.run(debug=True)
