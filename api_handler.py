import requests
import json
from scraper import scrape_text_from_url
import paho.mqtt.client as mqtt

def translate_text(text, source_lang, target_lang, api_key):
    
    url = "https://google-translator9.p.rapidapi.com/v2"
    headers = {
        "content-type": "application/json",
	    "X-RapidAPI-Key": api_key,
	    "X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
    }
    data = {
        'q': text,
        'source': source_lang,
        'target': target_lang,
        "format": "text"
    }

    data_json = json.dumps(data)
    response = requests.post(url, headers=headers, data=data_json)

    if response.status_code == 200:
        return response.json() 
    else:
        return {'error': 'Failed to translate text', 'status_code': response.status_code}


def save_to_json(data, filename='output.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def publish_message(topic, message):
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.on_connect = on_connect
    client.connect("broker.hivemq.com", 1883, 60)
    client.loop_start() 
    client.publish(topic, message)
    client.loop_stop() 
    client.disconnect()



def translate_scraped_text(url, source_lang, target_lang, api_key):
    """
    Scrapes text from a URL, translates it, and saves the translation to a JSON file.

    Parameters:
        url (str): URL to scrape text from.
        source_lang (str): Source language of the text.
        target_lang (str): Target language for the translation.
        api_key (str): API key for the Google Translate API.
    """
    text = scrape_text_from_url(url)
    if text:
        translation = translate_text(text, source_lang, target_lang, api_key)
        save_to_json(translation)
        translated_text = translation['data']['translations'][0]['translatedText']
        publish_message("topic/translation", translated_text)
    else:
        print("No text could be scraped from the URL.")

if __name__ == "__main__":

    url = "https://example.com/"
    source_lang = "en"
    target_lang = "lt"

    api_key = 'f0c2562ed5msh9a561bf2ed0c36ap1714eejsnb014403e12a8'
    translate_scraped_text(url, source_lang, target_lang, api_key)
