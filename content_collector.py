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
        break
print("Data have been read.")

filtered_repositories = []

for repository in repositories:
    # Making all columns "No" as default

    # Maven Dependencies
    repository["MJacoco"] = ""
    repository["MCobertura"] = ""
    repository["MJavadoc"] = ""

    # Gradle Dependencies
    repository["GJacoco"] = ""
    repository["GCobertura"] = ""
    repository["GJavadoc"] = ""

    # Travis tools
    repository["Tyml_codecov"] = ""
    repository["Tyml_jacoco"] = ""
    repository["Tyml_cobertura"] = ""
    repository["Tyml_javadoc"] = ""

    # Github Action Tools
    repository["Gyml_codecov"] = ""
    repository["Gyml_jacoco"] = ""
    repository["Gyml_cobertura"] = ""
    repository["Gyml_javadoc"] = ""

    i = 0
    # checking if the repository has pom.xml in its files
    if not repository["Maven"] == "":
        file_paths = repository["Maven"].split(";")
        for file_path in file_paths:
            try:
                response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/"+file_path,
                                        headers=headers).json()
                pom_content = base64.b64decode(response["content"]).decode("utf-8")
                # checking if the pom.xml contains "jacoco-maven-plugin" keyword
                if "jacoco-maven-plugin" in pom_content:
                    repository["MJacoco"] = repository["MJacoco"]+ file_path+";"
                # checking if the pom.xml contains "cobertura-maven-plugin" keyword
                if "cobertura-maven-plugin" in pom_content:
                    repository["MCobertura"] = repository["MCobertura"]+file_path+";"
                if "maven-javadoc-plugin" in pom_content:
                    repository["MJavadoc"] = repository["MJavadoc"]+file_path+";"
            except:
                repository["MJacoco"] = repository["MJacoco"]+"Skipped;"
                repository["MCobertura"] = repository["MCobertura"]+"Skipped;"
                repository["MJavadoc"] = repository["MJavadoc"]+"Skipped;"

    # checking if the repository has build-gradle in its files
    if not repository["Gradle"] == "":
        file_paths = repository["Gradle"].split(";")
        for file_path in file_paths:
            try:
                response = requests.get(
                    url="https://api.github.com/repos/" + repository["name"] + "/contents/"+file_path,
                    headers=headers).json()
                gradle_content = base64.b64decode(response["content"]).decode("utf-8")
                if "jacoco" in gradle_content:
                    repository["GJacoco"] = repository["GJacoco"]+file_path+";"
                if "cobertura" in gradle_content:
                    repository["GCobertura"] = repository["GCobertura"]+file_path+";"
                if "javadoc" in gradle_content or "Javadoc" in gradle_content:
                    repository["GJavadoc"] = repository["GJavadoc"]+file_path+";"
                break
            except:
                repository["GJacoco"] = repository["GJacoco"]+"Skipped;"
                repository["GCobertura"] = repository["GCobertura"]+"Skipped;"
                repository["GJavadoc"] = repository["GJavadoc"]+"Skipped;"

    # checking if the repository has .travis.yml in its files
    if not repository["Travis CI"] == "":
        file_paths = repository["Travis CI"].split(";")
        for file_path in file_paths:
            try:
                response = requests.get(
                    url="https://api.github.com/repos/" + repository["name"] + "/contents/"+file_path,
                    headers=headers).json()
                travis_content = base64.b64decode(response["content"]).decode("utf-8")
                if "https://codecov.io/bash" in travis_content:
                    repository["Tyml_codecov"] = repository["Tyml_codecov"]+file_path+";"
                if "jacoco" in travis_content and "jacoco.skip=true" not in travis_content:
                    repository["Tyml_jacoco"] = repository["Tyml_jacoco"]+file_path+";"
                if "cobertura" in travis_content:
                    repository["Tyml_cobertura"] = repository["Tyml_cobertura"]+file_path+";"
                if "javadoc" in travis_content:
                    repository["Tyml_javadoc"] = repository["Tyml_javadoc"]+file_path+";"
            except:
                repository["Tyml_codecov"] = repository["Tyml_codecov"]+"Skipped;"
                repository["Tyml_jacoco"] = repository["Tyml_jacoco"]+"Skipped;"
                repository["Tyml_cobertura"] = repository["Tyml_cobertura"]+"Skipped;"
                repository["Tyml_javadoc"] = repository["Tyml_javadoc"]+"Skipped;"

        # checking if the repository has *.yml file in /.github/workflows
    if not repository["Github Actions"] == "":
        file_paths = repository["Github Actions"].split(";")
        for file_path in file_paths:
            try:
                response = requests.get(
                    url="https://api.github.com/repos/" + repository["name"] + "/contents/"+file_path,
                    headers=headers).json()
                yml_content = base64.b64decode(response["content"]).decode("utf-8")
                # checking if the *.yml contains "https://codecov.io/bash" keyword
                if "https://codecov.io/bash" in yml_content:
                    repository["Gyml_codecov"] = repository["Gyml_codecov"]+file_path+";"
                if "jacoco" in yml_content and "jacoco.skip=true" not in yml_content:
                    repository["Gyml_jacoco"] = repository["Gyml_jacoco"]+file_path+";"
                if "cobertura" in yml_content:
                    repository["Gyml_cobertura"] = repository["Gyml_cobertura"]+file_path+";"
                if "javadoc" in yml_content:
                    repository["Gyml_javadoc"] = repository["Gyml_javadoc"]+file_path+";"
            except:
                repository["Gyml_codecov"] = repository["Gyml_codecov"]+"Skipped;"
                repository["Gyml_jacoco"] = repository["Gyml_jacoco"]+"Skipped;"
                repository["Gyml_cobertura"] = repository["Gyml_cobertura"]+"Skipped;"
                repository["Gyml_javadoc"] = repository["Gyml_javadoc"]+"Skipped;"
    i = i+1
    print(i)


# Save repositories to a csv file
with open("file_contents.csv", "w", newline="") as csv_file:
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

