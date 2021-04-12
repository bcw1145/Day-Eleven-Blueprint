import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
}

subreddits = [
    "javascript", "reactjs", "reactnative", "programming", "css", "golang",
    "flutter", "rust", "django"
]

os.system('clear')

db = []


def get_reddit(word):

    url = f"https://www.reddit.com/r/{word}/top/?t=month"
    results = requests.get(url, headers=headers).text
    soup = BeautifulSoup(results, 'html.parser')
    contents = (soup.find(class_='rpBJOHq2PR60pnwJlUyP0').find_all(
        'div', class_='_1oQyIsiPHYt6nx7VOmd1sz'))
    for content in contents:
        title = content.find(class_='_eYtD2XCVieq6emjKBH3m').text
        votes = content.find(
            class_='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo').text
        if votes == 'Vote':
            vote = 0
        elif 'k' in votes:
            num = votes.split('k')
            vote = int(float(num[0]) * 1000)
        else:
            vote = int(votes)
        link = content.find(class_='_3jOxDPIQ0KaOWpzvSQo-1s')['href']
        db.append((word, title, vote, link))


app = Flask("DayEleven")


@app.route("/")
def home():
    return render_template('home.html', datas=subreddits)


@app.route("/read")
def read():
    reading = ''
    for subreddit in subreddits:
        read = request.args.get(subreddit)
        if read == 'on':
            get_reddit(subreddit)
            reading = reading + f"/{subreddit}"

    data = sorted(db, key=lambda value: value[2], reverse=True)

    return render_template('read.html', datas=data, reading=reading)


app.run(host="0.0.0.0")
