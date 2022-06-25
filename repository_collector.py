import csv
import os
import time

import requests

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

repositories = []
# 30*33=990
# There are 30 repos in every page, so with 33 iterations we get 990 java repositories.
for i in range(0, 33):
    try:
        url = "https://api.github.com/search/repositories?q=language:java&sort=forks&order=desc&page=" + str(i)
        response = requests.get(url=url, headers=headers).json()
        for repository in response["items"]:
            repositories.append({"name": repository["full_name"], "link": repository["html_url"]})
    except:
        time.sleep(4)
        i = i-1


# Save repositories to a csv file
with open("repositories.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Link"])
    for repository in repositories:
        csv_writer.writerow([repository["name"], repository["link"]])
