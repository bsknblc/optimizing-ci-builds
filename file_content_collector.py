import base64
import copy
import csv
import os
import requests

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

# Read the data from the csv file.
repositories = []
with open("root_content.csv", "r", newline="") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        repositories.append(
            {"name": row[0], "link": row[1], "default_branch": row[2], "sha": row[3],
             "stargazers_count": row[4], "forks_count": row[5],
             "Maven": row[6], "Gradle": row[7], "Travis CI": row[8], "Github Actions": row[9]})
print("Data have been read.")

filtered_repositories = []

for repository in repositories:
    # Making all columns "No" as default

    # Maven Dependencies
    repository["MJacoco"] = "No"
    repository["MCobertura"] = "No"
    repository["MJavadoc"] = "No"

    # Gradle Dependencies
    repository["GJacoco"] = "No"
    repository["GCobertura"] = "No"
    repository["GJavadoc"] = "No"

    # Travis tools
    repository["Tyml_codecov"] = "No"
    repository["Tyml_jacoco"] = "No"
    repository["Tyml_cobertura"] = "No"
    repository["Tyml_javadoc"] = "No"

    # Github Action Tools
    repository["Gyml_codecov"] = ""
    repository["Gyml_jacoco"] = ""
    repository["Gyml_cobertura"] = ""
    repository["Gyml_javadoc"] = ""

    # checking if the repository has pom.xml in its root
    if not repository["Maven"] == "":
        try:
            response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/pom.xml",
                                    headers=headers).json()
            pom_content = base64.b64decode(response["content"]).decode("utf-8")
            # checking if the pom.xml contains "jacoco-maven-plugin" keyword
            if "jacoco-maven-plugin" in pom_content:
                repository["MJacoco"] = "Yes"
            # checking if the pom.xml contains "cobertura-maven-plugin" keyword
            if "cobertura-maven-plugin" in pom_content:
                repository["MCobertura"] = "Yes"
            if "maven-javadoc-plugin" in pom_content:
                repository["MJavadoc"] = "Yes"
        except:
            repository["MJacoco"] = "Skipped"
            repository["MCobertura"] = "Skipped"
            repository["MJavadoc"] = "Skipped"

    # checking if the repository has build-gradle in its root
    if not repository["Gradle"] == "":
        try:
            response = requests.get(
                url="https://api.github.com/repos/" + repository["name"] + "/contents/build.gradle",
                headers=headers).json()
            gradle_content = base64.b64decode(response["content"]).decode("utf-8")
            if "jacoco" in gradle_content:
                repository["GJacoco"] = "Yes"
            if "cobertura" in gradle_content:
                repository["GCobertura"] = "Yes"
            if "javadoc" in gradle_content or "Javadoc" in gradle_content:
                repository["GJavadoc"] = "Yes"
            break
        except:
            repository["GJacoco"] = "Skipped"
            repository["GCobertura"] = "Skipped"
            repository["GJavadoc"] = "Skipped"

    # checking if the repository has .travis.yml in its root
    if not repository["Travis CI"] == "":
        try:
            response = requests.get(
                url="https://api.github.com/repos/" + repository["name"] + "/contents/.travis.yml",
                headers=headers).json()
            travis_content = base64.b64decode(response["content"]).decode("utf-8")
            if "https://codecov.io/bash" in travis_content:
                repository["Tyml_codecov"] = "Travis;"
            if "jacoco" in travis_content and "jacoco.skip=true" not in travis_content:
                repository["Tyml_jacoco"] = "Travis;"
            if "cobertura" in travis_content:
                repository["Tyml_cobertura"] = "Travis;"
            if "javadoc" in travis_content:
                repository["Tyml_javadoc"] = "Travis;"
        except:
            repository["Tyml_codecov"] = "Skipped Travis;"
            repository["Tyml_jacoco"] = "Skipped Travis;"
            repository["Tyml_cobertura"] = "Skipped Travis;"
            repository["Tyml_javadoc"] = "Skipped Travis;"

        # checking if the repository has *.yml file in /.github/workflows
        GHAFiles = repository["Github Actions"].split(";")
        for filename in GHAFiles:
            if ".yml" in filename or ".yaml" in filename:
                try:
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository[
                            "name"] + "/contents/.github/workflows/" + filename, headers=headers).json()
                    yml_content = base64.b64decode(response["content"]).decode("utf-8")
                    # checking if the *.yml contains "https://codecov.io/bash" keyword
                    if "https://codecov.io/bash" in yml_content:
                        repository["Gyml_codecov"] = repository["Gyml_codecov"].append(";"+filename)
                    if "jacoco" in yml_content and "jacoco.skip=true" not in yml_content:
                        repository["Gyml_jacoco"] = repository["Gyml_jacoco"].append(";"+filename)
                    if "cobertura" in yml_content:
                        repository["Gyml_cobertura"] = repository["Gyml_cobertura"].append(";"+filename)
                    if "javadoc" in yml_content:
                        repository["Gyml_javadoc"] = repository["Gyml_javadoc"].append(";"+filename)
                except:
                    repository["Gyml_codecov"]  = "Skipped"
                    repository["Gyml_jacoco"] = "Skipped"
                    repository["Gyml_cobertura"] = "Skipped"
                    repository["Gyml_javadoc"] = "Skipped"

    print("Looking to its angeleyes.")


# Save repositories to a csv file
with open("data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["link", "Maven", "Gradle", "Travis CI", "Github Actions",
         "Maven Jacoco", " Maven Cobertura", "Maven Javadoc",
         "Gradle Jacoco", "Gradle Cobertura", "Gradle Javadoc",
         "Travis Codecov", "Travis Jacoco", " Travis Cobertura", "Travis Javadoc",
         "GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc"
         ])

    for repository in repositories:
        csv_writer.writerow([repository["link"], repository["Maven"], repository["Gradle"],
                             repository["Travis CI"], repository["Github Actions"],
                             repository["MJacoco"], repository["MCobertura"], repository["MJavadoc"],
                             repository["GJacoco"],repository["GCobertura"], repository["GJavadoc"],
                             repository["Tyml_codecov"], repository["Tyml_jacoco"], repository["Tyml_cobertura"], repository["Tyml_javadoc"],
                             repository["Gyml_codecov"], repository["Gyml_jacoco"], repository["Gyml_cobertura"], repository["Gyml_javadoc"]])

print("One look and you're hypnotized")
