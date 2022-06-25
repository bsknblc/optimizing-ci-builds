import base64
import copy
import csv
import os
import requests

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

repositories = []
# 30*30=900
# There are 30 repos in every page, so with 33 iterations we get 990 java repositories.
for i in range(0, 33):
    try:
        url = "https://api.github.com/search/repositories?q=language:java&sort=forks&order=desc&page=" + str(i)
        response = requests.get(url=url, headers=headers).json()
        for repository in response["items"]:
            repositories.append({"name": repository["full_name"], "link": repository["html_url"]})
    except:
        print("one skipped")
        repositories.append({"name": "skipped", "link": "skipped"})


# Save repositories to a csv file
with open("repositories.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Name", "Link"])
    for repository in repositories:
        csv_writer.writerow([repository["full_name"], repository["html_url"]])

print("Repos taken")
filtered_repositories = []

for repository in repositories:
    # Making all columns "No" as default
    repository["Maven"] = "No"
    repository["Gradle"] = "No"
    repository["Jacoco"] = "No"
    repository["Cobertura"] = "No"
    repository["Javadoc"] = "No"
    repository["CodecovT"] = "No"
    repository["CodecovG"] = "No"
    repository["Travis CI"] = "No"
    repository["Github Actions"] = "No"
    repository["yml_jacoco"] = "No"
    repository["yml_cobertura"] = "No"
    repository["yml_javadoc"] = "No"
    repository["jacoco.skip=true"] = "No"
    usableFlag = 0
    files = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents", headers=headers).json()
    for file in files:
        # checking if the repository has .travis.yml in its root
        try:
            if file["name"] == ".travis.yml":
                repository["Travis CI"] = "Yes"
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/.travis.yml",
                                        headers=headers).json()
                travis_content = base64.b64decode(response["content"]).decode("utf-8")
                # checking if the .travis.yml contains "https://codecov.io/bash" keyword
                if "https://codecov.io/bash" in travis_content:
                    repository["CodecovT"] = "Yes"
                    usableFlag += 1
                if "jacoco" in travis_content:
                    repository["yml_jacoco"] = "Yes Travis"
                    usableFlag += 1
                if "cobertura" in travis_content:
                    repository["yml_cobertura"] = "Yes Travis"
                    usableFlag += 1
                if "javadoc" in travis_content:
                    repository["yml_javadoc"] = "Yes Travis"
                    usableFlag += 1
                if "jacoco.skip=true" in travis_content:
                    repository["jacoco.skip=true"] = "Yes Travis"
                    usableFlag += 1
        except:
            print("one skipped in travis file")
            repository["Travis CI"] = "Skipped"
        # checking if the repository has pom.xml in its root
        try:
            if file["name"] == "pom.xml":
                repository["Maven"] = "Yes"
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/pom.xml",
                                        headers=headers).json()
                pom_content = base64.b64decode(response["content"]).decode("utf-8")
                # checking if the pom.xml contains "jacoco-maven-plugin" keyword
                if "jacoco-maven-plugin" in pom_content:
                    repository["Jacoco"] = "Yes"
                    usableFlag += 1
                # checking if the pom.xml contains "cobertura-maven-plugin" keyword
                if "cobertura-maven-plugin" in pom_content:
                    repository["Cobertura"] = "Yes"
                    usableFlag += 1
                if "maven-javadoc-plugin" in pom_content:
                    repository["Javadoc"] = "Yes"
                    usableFlag += 1
                    break
        except:
            print("one skipped")
            repository["Maven"] = "Skipped"
        # checking if the repository has build-gradle in its root
        try:
            if file["name"] == "build.gradle":
                repository["Gradle"] = "Yes"
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/build.gradle",
                                        headers=headers).json()
                gradle_content = base64.b64decode(response["content"]).decode("utf-8")
                if "jacoco" in gradle_content:
                    repository["Jacoco"] = "Yes"
                    usableFlag += 1
                if "cobertura" in gradle_content:
                    repository["Cobertura"] = "Yes"
                    usableFlag += 1
                if "javadoc" in gradle_content or "Javadoc" in gradle_content:
                    repository["Javadoc"] = "Yes"
                    usableFlag += 1
                break
        except:
            print("one skipped")
            repository["Gradle"] = "Skipped"
    print("first files period done")
    # checking if the repository has *.yml file in /.github/workflows
    try:
        GHAFiles = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/.github/workflows",
                                headers=headers).json()
        for file in GHAFiles:
            if "name" in file:
                if ".yml" in file["name"] or ".yaml" in file["name"]:
                    repository["Github Actions"] = "Yes"
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository["name"] + "/contents/.github/workflows/" + file[
                            "name"], headers=headers).json()
                    yml_content = base64.b64decode(response["content"]).decode("utf-8")
                    # checking if the *.yml contains "https://codecov.io/bash" keyword
                    if "https://codecov.io/bash" in yml_content:
                        repository["CodecovG"] = "Yes"
                        usableFlag += 1
                    if "jacoco" in yml_content:
                        repository["yml_jacoco"] = "Yes GHA"
                        usableFlag += 1
                    if "cobertura" in yml_content:
                        repository["yml_cobertura"] = "Yes GHA"
                        usableFlag += 1
                    if "javadoc" in yml_content:
                        repository["yml_javadoc"] = "Yes GHA"
                        usableFlag += 1
                    if "jacoco.skip=true" in yml_content:
                        repository["jacoco.skip=true"] = "Yes GHA"
                        usableFlag += 1
    except:
        print("one skipped")
        repository["Github Actions"] = "Skipped"
    print("second files period done")
    if usableFlag > 0:
        filtered_repositories.append(copy.deepcopy(repository))
print("repos examination done")

# Remove duplicates
final_repositories = []
[final_repositories.append(repository) for repository in filtered_repositories if repository not in final_repositories]

# Save repositories to a csv file
with open("data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["link", "Maven", "Gradle", "Jacoco", "Cobertura", "Javadoc", "Codecov GHA", "Codecov Travis", "Travis CI",
                         "Github Actions", "Yml Jacoco", "Yml Cobertura", "Yml Javadoc", "Jacoco skip"])
    for repository in final_repositories:
        csv_writer.writerow([repository["link"], repository["Maven"], repository["Gradle"], repository["Jacoco"],
                             repository["Cobertura"], repository["Javadoc"],repository["CodecovG"], repository["CodecovT"],
                             repository["Travis CI"], repository["Github Actions"], repository["yml_jacoco"],
                             repository["yml_cobertura"], repository["yml_javadoc"], repository["jacoco.skip=true"]])
