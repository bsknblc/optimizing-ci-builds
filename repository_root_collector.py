import csv
import os
import time
from datetime import datetime
import requests

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

# Read the repositories from the csv file.
repositories = []
with open("repositories.csv", "r", newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        repositories.append({"name": row[0], "link": row[1], "date": row[2]})
print("Repositories taken.")

for repository in repositories:
    # Making all columns "No" as default
    repository["Maven"] = "No"
    repository["Gradle"] = "No"
    repository["Travis CI"] = "No"
    repository["Github Actions"] = "No"
    try:
        files = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents",
                             headers=headers).json()
        for file in files:
            # checking if the repository has pom.xml in its root
            if file["name"] == "pom.xml":
                repository["Maven"] = "Yes"
            # checking if the repository has build-gradle in its root
            if file["name"] == "build.gradle":
                repository["Gradle"] = "Yes"
            # checking if the repository has .travis.yml in its root
            if file["name"] == ".travis.yml":
                repository["Travis CI"] = "Yes"
    except:
        repository["Maven"] = "Skipped"
        repository["Gradle"] = "Skipped"
        repository["Travis CI"] = "Skipped"

    try:
        # checking if the repository has *.yml file in /.github/workflows
        GHAFiles = requests.get(
            url="https://api.github.com/repos/" + repository["name"] + "/contents/.github/workflows23"3,
            headers=headers).json()
        for file in GHAFiles:
            if "name" in file:
                if ".yml" in file["name"] or ".yaml" in file["name"]:
                    if repository["Github Actions"] == "No":
                        repository["Github Actions"] = file["name"] + ";"
                    else:
                        repository["Github Actions"] = repository["Github Actions"].append(file["name"] + ";")
    except:
        repository["Github Actions"] = "Skipped"

# Save data to a csv file
with open("root_content.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["name", "link", "Maven", "Gradle", "Travis CI", "Github Actions"])
    for repository in repositories:
        csv_writer.writerow([repository["name"], repository["link"], repository["Maven"], repository["Gradle"], repository["Travis CI"],
                             repository["Github Actions"]])
