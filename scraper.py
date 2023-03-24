from flask import Flask, request, render_template
import requests
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    page_no = request.form['page_no']
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://ieeexplore.ieee.org",
        "Content-Type": "application/json",
    }
    payload = {
        "newsearch": True,
        "queryText": search_term,
        "highlight": True,
        "returnFacets": ["ALL"],
        "returnType": "SEARCH",
        "pageNumber": page_no
    }
    r = requests.post(
        "https://ieeexplore.ieee.org/rest/search",
        json=payload,
        headers=headers
    )
    page_data = r.json()
    articles = []
    for record in page_data["records"]:
        articles.append({
            "title": record["articleTitle"],
            "link": 'https://ieeexplore.ieee.org' + record["documentLink"]
        })
    return render_template('results.html', articles=articles)
if __name__=='__main__':
    app.run(debug=True)
