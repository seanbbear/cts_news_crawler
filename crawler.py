import requests
import wget
import datetime
from bs4 import BeautifulSoup
import urllib
import time
import json


def main():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    date_list = []
    start_date = datetime.date(2020, 8, 3)
    end_date = datetime.date(2021, 10, 21)
    delta = end_date - start_date
    date_list = [(start_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

    prefix_news_url = "https://news.cts.com.tw/sound/api/"
    prefix_sound_url = "https://www.spreaker.com/episode/"

    for date in date_list:
        print(f"current crawling date :{date}")
        url = prefix_news_url + date + ".json"

        try:
            response = requests.get(url)
        except Exception as e:
            print(e)

        if response.status_code == 200:
            text = response.json()
        else:
            continue

        for t in text:
            try:
                response = requests.get(prefix_sound_url + t['episode_id'], headers=headers)
                soup = BeautifulSoup(response.text)

                download_file(t['episode_id'], t['news_id'])

                trans_url = soup.find("div", class_="track_description").select("a")[0].get("href")
                transcript = getTranscript(trans_url, headers)
                with open("../data/cts_news/trans_origin.txt", "a+", encoding='utf-8') as f:
                    content = t['news_id'] + ".mp3\t" + transcript.replace("\n", "").replace("\r", "").replace("\t", "")
                    f.write(content+"\n")
                time.sleep(0.1)
            except Exception as e:
                print(e)
                time.sleep(0.1)
                break
        

def download_file(episode_id, news_id):
    download_url = "https://api.spreaker.com/download/episode/" + episode_id
    print(f"\ndownloading {news_id}")
    wget.download(download_url, out="../data/cts_news/" + news_id + ".mp3")

def getTranscript(trans_url, headers):
    response = requests.get(trans_url, headers=headers)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    
    if soup.find("div", class_="artical-content"):
        transcript = soup.find("div", class_="artical-content").text
    else:
        transcript = ""

    return transcript

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    main()
