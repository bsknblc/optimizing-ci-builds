import csv
import os
import time
from datetime import datetime
import requests

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

repositories = []
# There are 30 repos in every page, so with 33 iterations we get 990 java repositories.
for i in range(0, 33):
    try:
        url = "https://api.github.com/search/repositories?q=language:java&sort=forks&order=desc&page=" + str(i)
        response = requests.get(url=url, headers=headers).json()
        for repository in response["items"]:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            repositories.append({"name": repository["full_name"], "link": repository["html_url"], "date": dt_string})
    except:
        print("exception")
        time.sleep(5)
        i = i-1
print("Repositories taken.")

# Save repositories to a csv file
with open("repositories.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Link", "Date"])
    for repository in repositories:
        csv_writer.writerow([repository["name"], repository["link"], repository["date"]])
