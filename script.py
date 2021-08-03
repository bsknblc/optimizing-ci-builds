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
# There are 30 repos in every page, so with 30 iterations we get 900 java repositories.
for i in range(1, 31):
    try:
        #big projects
        #url = "https://api.github.com/search/repositories?q=language:java&sort=forks&order=desc&page=" + str(i)
        #mid sized projects
        url = "https://api.github.com/search/repositories?q=stars:%3E1+pushed%3A2018-11-10..2018-11-12+language:java&sort=stars&order=desc&page=1" + str(i)
        response = requests.get(url=url, headers=headers).json()
        for repository in response["items"]:
            repositories.append({"name": repository["full_name"], "link": repository["html_url"]})
    except:
        print("one skipped")
print("repos taken")

for repository in repositories:
    # Making all columns "No" as default
    repository["Maven"] = "No"
    repository["Gradle"] = "No"
    repository["Jacoco"] = "/"
    repository["Cobertura"] = "/"
    repository["Javadoc"] = "/"
    repository["CodecovT"] = "No"
    repository["CodecovG"] = "-"
    repository["Travis CI"] = "No"
    repository["Github Actions"] = "No"
    repository["yml_jacoco"] = "-"
    repository["yml_cobertura"] = "-"
    repository["yml_javadoc"] = "-"
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
                if "https://codecov.io/bash" in travis_content or "codecov/codecov-action@" in travis_content:
                    repository["CodecovT"] = "Yes"
                if "jacoco" in travis_content and "jacoco.skip=true" not in travis_content and "jacoco:report coveralls" not in travis_content:
                    repository["Tyml_jacoco"] = "Yes"
                if "cobertura" in travis_content:
                    repository["Tyml_cobertura"] = "Yes"
                if "javadoc" in travis_content and "maven.javadoc.skip=true" not in travis_content and "maven.javadoc.skip=TRUE" not in travis_content:
                    repository["Tyml_javadoc"] = "Yes"
        except:
            print("one skipped")
        # checking if the repository has pom.xml in its root
        try:
            if file["name"] == "pom.xml":
                repository["Maven"] = "Yes"
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/pom.xml",
                                        headers=headers).json()
                pom_content = base64.b64decode(response["content"]).decode("utf-8")
                # checking if the pom.xml contains "jacoco-maven-plugin" keyword
                if "jacoco-maven-plugin" in pom_content:
                    repository["Jacoco"] = "pom.xml"
                # checking if the pom.xml contains "cobertura-maven-plugin" keyword
                if "cobertura-maven-plugin" in pom_content:
                    repository["Cobertura"] = "pom.xml"
                if "maven-javadoc-plugin" in pom_content:
                    repository["Javadoc"] = "pom.xml"
                    break
        except:
            print("one skipped")
        # checking if the repository has build-gradle in its root
        try:
            if file["name"] == "build.gradle":
                repository["Gradle"] = "Yes"
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/build.gradle",
                                        headers=headers).json()
                gradle_content = base64.b64decode(response["content"]).decode("utf-8")
                if "jacoco" in gradle_content:
                    repository["Jacoco"] = repository["Jacoco"] + "/ build.gradle"
                if "cobertura" in gradle_content:
                    repository["Cobertura"] = repository["Cobertura"] + "/ build.gradle"
                if "javadoc" in gradle_content or "Javadoc" in gradle_content:
                    repository["Javadoc"] = repository["Javadoc"] + "/ build.gradle"
                break
        except:
            print("one skipped")
    print("first files period done")
    # checking if the repository has *.yml file in /.github/workflows
    try:
        GHAFiles = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/.github/workflows",
                                headers=headers).json()
        for file in GHAFiles:
            cnt= 0
            if "name" in file:
                if ".yml" in file["name"] or ".yaml" in file["name"]:
                    repository["Github Actions"] = "Yes"
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository["name"] + "/contents/.github/workflows/" + file[
                            "name"], headers=headers).json()
                    yml_content = base64.b64decode(response["content"]).decode("utf-8")
                    cnt += 1
                    name = "file" + cnt
                    # checking if the *.yml contains "https://codecov.io/bash" keyword
                    if "https://codecov.io/bash" in yml_content or "codecov/codecov-action@" in yml_content:
                        repository["CodecovG"] = repository["CodecovG"] + "/ "+ name
                    if "jacoco" in yml_content and "jacoco.skip=true" not in yml_content and "jacoco:report coveralls" not in yml_content:
                        repository["yml_jacoco"] = repository["yml_jacoco"] + "/ "+ name
                    if "cobertura" in yml_content:
                        repository["yml_cobertura"] = repository["yml_cobertura"] + "/ "+ name
                    if "javadoc" in yml_content and "maven.javadoc.skip=true" not in yml_content and "maven.javadoc.skip=TRUE" not in yml_content:
                        repository["yml_javadoc"] = repository["yml_javadoc"] + "/ "+ name
    except:
        print("one skipped")
    print("second files period done")

print("repos examination done")

# Save repositories to a csv file
with open("data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["link", "Maven", "Gradle", "Jacoco", "Cobertura", "Javadoc", "Codecov GHA", "Codecov Travis", "Github Actions", "Travis CI",
                         "Travis Yml Jacoco", " Travis Yml Cobertura", "Travis Yml Javadoc","GHA Yml Jacoco", "GHA Yml Cobertura", "GHA Yml Javadoc"])
    for repository in repositories:
        csv_writer.writerow([repository["link"], repository["Maven"], repository["Gradle"], repository["Jacoco"],
                             repository["Cobertura"], repository["Javadoc"],repository["CodecovG"], repository["CodecovT"],
                            repository["Github Actions"], repository["Travis CI"], repository["Tyml_jacoco"],
                             repository["Tyml_cobertura"], repository["Tyml_javadoc"],repository["yml_jacoco"],
                             repository["yml_cobertura"], repository["yml_javadoc"]])
