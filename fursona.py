import requests
import random
import os
import psycopg2
import time
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from urllib import parse
from mastodon import Mastodon


def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline()
    return file.readline()


parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()
cur.execute("SELECT * from last_toot")
last_toot = cur.fetchall()
last_toot = last_toot[0][0]
latest_id = False

mastodon = Mastodon(
    client_id='pytooter_clientcred.secret',
    access_token='pytooter_usercred.secret',
    api_base_url='https://botsin.space'
)

base_date = datetime.now(timezone.utc) - relativedelta(years=5)
orig_date = base_date
notifications = mastodon.notifications(since_id=last_toot)

mentions = []

while notifications:
    for alert in notifications:
        if alert['type'] == "mention" and "give me a fursona" in alert['status']['content'].lower():
            mentions.append(alert)
    notifications = mastodon.fetch_previous(notifications[0]['_pagination_prev'])

if mentions:
    for alert in mentions:
        if alert['created_at'] > base_date:
            base_date = alert['created_at']
            latest_id = alert['id']
        fursona = get_random_line("fursona.txt")[:-1]
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color_values = str(r) + "," + str(g) + "," + str(b)
        color_request = requests.get("http://www.thecolorapi.com/id", params={"rgb": color_values})
        color = color_request.json()['name']['value'].lower()
        if color == "":
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            color_values = str(r) + "," + str(g) + "," + str(b)
            color_request = requests.get("http://www.thecolorapi.com/id", params={"rgb": color_values})
            color = color.request.json()['name']['value']
        if color != "":
            if color[0] in ['a', 'e', 'i', 'o', 'u']:
                status = "@" + alert['account']['acct'] + " Your fursona is an " + color + "-colored " + fursona + "."
            else:
                status = "@" + alert['account']['acct'] + " Your fursona is a " + color + "-colored " + fursona + "."
            mastodon.status_post(status, in_reply_to_id=alert['status']['id'])
            time.sleep(3)

if orig_date != base_date and latest_id:
    cur.execute("delete from last_toot")
    cur.execute("insert into last_toot values (%s)", (int(latest_id),))
    conn.commit()
    conn.close()
