from flask import Flask, jsonify, render_template, request
from api_handler import translate_scraped_text
import json

app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # A general homepage with links or buttons to different functionalities

@app.route('/translate')
def translate():
    # Example text and language codes
    url = "https://example.com"
    source_language = "en"
    target_language = "de"
    api_key = 'f0c2562ed5msh9a561bf2ed0c36ap1714eejsnb014403e12a8'
    translate_scraped_text(url, source_language, target_language, api_key)
    try:
        with open('output.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            translation = data.get('data', {}).get('translations', [{}])[0].get('translatedText', 'Translation not available')
    except FileNotFoundError:
        translation = "Translation result file not found."
    except json.JSONDecodeError:
        translation = "Error decoding the translation result."
    return render_template('translation.html', translation=translation)

if __name__ == "__main__":
    app.run(debug=True)
