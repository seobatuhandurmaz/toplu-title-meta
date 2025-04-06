from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://www.batuhandurmaz.com"}})

@app.route('/get-meta', methods=['POST'])
def get_meta():
    urls = request.json.get('urls', [])
    results = []

    for url in urls:
        url = url.strip()
        if not url:
            continue
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else ''
            description_tag = soup.find('meta', attrs={'name': 'description'})
            description = description_tag['content'].strip() if description_tag and 'content' in description_tag.attrs else ''

            results.append({
                'url': url,
                'title': title,
                'description': description
            })
        except Exception as e:
            results.append({
                'url': url,
                'title': '',
                'description': '',
                'error': str(e)
            })

    return jsonify(results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
