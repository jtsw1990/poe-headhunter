from datetime import datetime, timezone
from utils.elapsed import time_elapsed_str
from tabulate import tabulate
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import requests
import json
import pytz
import smtplib
import ssl
import os

#load_dotenv()

#email_password = os.getenv("EMAIL_PASSWORD")

email_password = os.environ["EMAIL_PASSWORD"]

with open("config.json", "r") as c:
    config = json.load(c)


url = f'https://www.pathofexile.com/api/trade/search/{config["league"]}'

r = requests.request(
    "POST", 
    url, 
    headers=config["headers"], 
    data=json.dumps(config["payload"])
)

if not r.ok:
    print("REST failed")
else:
    response = r.json()
    qurl = f'https://www.pathofexile.com/api/trade/fetch/{",".join(response["result"][:config["cheapest_n"]])}?query={response["id"]}'
    sale_results = requests.request("GET", qurl, headers=config["headers"])
    local = pytz.timezone("Australia/Sydney")
    detail_list = []

    for k in sale_results.json()["result"]:
            detail_list.append(
                {
                    "account_name": k["listing"]["account"]["name"],
                    "currency": k["listing"]["price"]["currency"], 
                    "amount": k["listing"]["price"]["amount"],
                    "corrupted": "True" if "corrupted" in k["item"].keys() else "False",
                    "posted": time_elapsed_str(
                        datetime.now(timezone.utc).astimezone() - 
                        local.localize(datetime.strptime(k["listing"]["indexed"], "%Y-%m-%dT%H:%M:%SZ"))
                    )
                }
            )
    result_str = tabulate(pd.DataFrame(detail_list), headers='keys', tablefmt='psql')
    if (np.min([x["amount"] for x in detail_list]) <= config["ex_threshold"]) | ("chaos" in [x["currency"] for x in detail_list]):
        print("email sent")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config["smtp_server"], config["port"], context=context) as server:
            server.login(config["sender_email"], email_password)
            server.sendmail(config["sender_email"], config["receiver_email"], result_str.encode("euc_kr"))
    else:
        print("email not sent")

