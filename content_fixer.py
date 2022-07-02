import base64
import copy
import csv
import os
import requests
import time

github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}

# repositories = []
# with open("file_contents.csv", "r", newline="", encoding="utf8") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     next(csv_reader, None)
#     for row in csv_reader:
#         repositories.append(
#             {"name": row[0], "link": row[1], "default_branch": row[2], "sha": row[3],
#              "stargazers_count": row[4], "forks_count": row[5],
#              "Maven": row[6], "Gradle": row[7], "Travis CI": row[8], "Github Actions": row[9],
#              "MJacoco": row[10], "MCobertura": row[11], "MJavadoc": row[12],
#              "GJacoco": row[13], "GCobertura": row[14], "GJavadoc": row[15],
#              "Tyml_codecov": row[16], "Tyml_jacoco": row[17], "Tyml_cobertura": row[18],
#              "Tyml_javadoc": row[19], "Gyml_codecov": row[20], "Gyml_jacoco": row[21],
#              "Gyml_cobertura": row[22], "Gyml_javadoc": row[23]})
# print("Old data have been read.")

repositories = []
with open("file_contents_r.csv", "r", newline="", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        repositories.append(
            {"link": row[0],
             "Maven": row[1], "Gradle": row[2], "Travis CI": row[3], "Github Actions": row[4],
             "MJacoco": row[5], "MCobertura": row[6], "MJavadoc": row[7],
             "GJacoco": row[8], "GCobertura": row[9], "GJavadoc": row[10],
             "Tyml_codecov": row[11], "Tyml_jacoco": row[12], "Tyml_cobertura": row[13],
             "Tyml_javadoc": row[14], "Gyml_codecov": row[15], "Gyml_jacoco": row[16],
             "Gyml_cobertura": row[17], "Gyml_javadoc": row[18]})
print("Old data have been read.")

i = 0

for repository in repositories:
    repository["name"] = repository["link"][19:]

    if not repository["Maven"] == "":
        file_paths = repository["Maven"].split(";")
        file_paths.remove("")

        maven_jacoco_files = repository["MJacoco"].split(";")
        maven_jacoco_files.remove("")

        skipped_flag = 0
        if len(maven_jacoco_files) > 0:
            if "Skipped" in maven_jacoco_files:
                repository["MJacoco"] = ""
                repository["MCobertura"] = ""
                repository["MJavadoc"] = ""
                skipped_flag = 1

        j = 0
        while j < len(file_paths):
            file_path = file_paths[j]
            is_file = file_path.split("/")
            if ".xml" not in is_file[len(is_file)-1]:
                skipped_flag = 0
            if skipped_flag == 1:
                try:
                    response = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents/" +
                                                file_path,
                                            headers=headers).json()
                    if "content" in response:
                        pom_content = base64.b64decode(response["content"]).decode("utf-8")
                        repository["MJacoco"] = repository["MJacoco"].replace("Skipped", "", 1)
                        if "jacoco-maven-plugin" in pom_content:
                            repository["MJacoco"] = repository["MJacoco"] + file_path + ";"
                        if "cobertura-maven-plugin" in pom_content:
                            repository["MCobertura"] = repository["MCobertura"] + file_path + ";"
                        if "maven-javadoc-plugin" in pom_content:
                            repository["MJavadoc"] = repository["MJavadoc"] + file_path + ";"
                        j = j + 1
                    else:
                        j = j + 1
                except:
                    repository["MJacoco"] = repository["MJacoco"] + "Skipped;"
                    repository["MCobertura"] = repository["MCobertura"] + "Skipped;"
                    repository["MJavadoc"] = repository["MJavadoc"] + "Skipped;"
                    time.sleep(3)
            else:
                j = len(file_paths)

    # checking if the repository has build-gradle in its files
    if not repository["Gradle"] == "":
        file_paths = repository["Gradle"].split(";")
        file_paths.remove("")

        gradle_jacoco_files = repository["GJacoco"].split(";")
        gradle_jacoco_files.remove("")

        skipped_flag = 0
        if len(gradle_jacoco_files) > 0:
            if "Skipped" in gradle_jacoco_files:
                repository["GJacoco"] = ""
                repository["GCobertura"] = ""
                repository["GJavadoc"] = ""
                skipped_flag = 1

        j = 0
        while j < len(file_paths):
            file_path = file_paths[j]
            is_file = file_path.split("/")
            if ".gradle" not in is_file[len(is_file) - 1]:
                skipped_flag = 0
            if skipped_flag == 1:
                try:
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository["name"] + "/contents/" + file_path,
                        headers=headers).json()
                    if "content" in response:
                        gradle_content = base64.b64decode(response["content"]).decode("utf-8")
                        if "jacoco" in gradle_content:
                            repository["GJacoco"] = repository["GJacoco"] + file_path + ";"
                        if "cobertura" in gradle_content:
                            repository["GCobertura"] = repository["GCobertura"] + file_path + ";"
                        if "javadoc" in gradle_content or "Javadoc" in gradle_content:
                            repository["GJavadoc"] = repository["GJavadoc"] + file_path + ";"
                        j = j + 1
                    else:
                        j = j + 1
                except:
                    repository["GJacoco"] = repository["GJacoco"] + "Skipped;"
                    repository["GCobertura"] = repository["GCobertura"] + "Skipped;"
                    repository["GJavadoc"] = repository["GJavadoc"] + "Skipped;"
                    time.sleep(3)
            else:
                j = len(file_paths)

    # checking if the repository has .travis.yml in its files
    if not repository["Travis CI"] == "":
        file_paths = repository["Travis CI"].split(";")
        file_paths.remove("")

        travis_jacoco_keyword = repository["Tyml_codecov"].split(";")
        travis_jacoco_keyword.remove("")

        skipped_flag = 0
        if len(travis_jacoco_keyword) > 0:
            if "Skipped" in travis_jacoco_keyword:
                repository["Tyml_codecov"] = ""
                repository["Tyml_jacoco"] = ""
                repository["Tyml_cobertura"] = ""
                repository["Tyml_javadoc"] = ""
                skipped_flag = 1

        j = 0
        while j < len(file_paths):
            file_path = file_paths[j]
            is_file = file_path.split("/")
            if ".travis" not in is_file[len(is_file) - 1]:
                skipped_flag = 0
            if skipped_flag == 1:
                try:
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository["name"] + "/contents/" + file_path,
                        headers=headers).json()
                    if "content" in response:
                        travis_content = base64.b64decode(response["content"]).decode("utf-8")
                        if "https://codecov.io/bash" in travis_content:
                            repository["Tyml_codecov"] = repository["Tyml_codecov"] + file_path + ";"
                        if "jacoco" in travis_content and "jacoco.skip=true" not in travis_content:
                            repository["Tyml_jacoco"] = repository["Tyml_jacoco"] + file_path + ";"
                        if "cobertura" in travis_content:
                            repository["Tyml_cobertura"] = repository["Tyml_cobertura"] + file_path + ";"
                        if "javadoc" in travis_content:
                            repository["Tyml_javadoc"] = repository["Tyml_javadoc"] + file_path + ";"
                        j = j + 1
                    else:
                        j = j + 1
                except:
                    repository["Tyml_codecov"] = repository["Tyml_codecov"] + "Skipped;"
                    repository["Tyml_jacoco"] = repository["Tyml_jacoco"] + "Skipped;"
                    repository["Tyml_cobertura"] = repository["Tyml_cobertura"] + "Skipped;"
                    repository["Tyml_javadoc"] = repository["Tyml_javadoc"] + "Skipped;"
                    time.sleep(3)
            else:
                j = len(file_paths)

    # checking if the repository has *.yml file in /.github/workflows
    if not repository["Github Actions"] == "":
        file_paths = repository["Github Actions"].split(";")
        file_paths.remove("")

        ga_jacoco_keyword = repository["Gyml_codecov"].split(";")
        ga_jacoco_keyword.remove("")

        skipped_flag = 0
        if len(ga_jacoco_keyword) > 0:
            if "Skipped" in ga_jacoco_keyword:
                repository["Gyml_codecov"] = ""
                repository["Gyml_jacoco"] = ""
                repository["Gyml_cobertura"] = ""
                repository["Gyml_javadoc"] = ""
                skipped_flag = 1

        j = 0
        while j < len(file_paths):
            file_path = file_paths[j]
            is_file = file_path.split("/")
            if ".yml" not in is_file[len(is_file) - 1] and ".yaml" not in is_file[len(is_file) - 1]:
                skipped_flag = 0
            if skipped_flag == 1:
                try:
                    response = requests.get(
                        url="https://api.github.com/repos/" + repository["name"] + "/contents/" + file_path,
                        headers=headers).json()
                    if "content" in response:
                        yml_content = base64.b64decode(response["content"]).decode("utf-8")
                        # checking if the *.yml contains "https://codecov.io/bash" keyword
                        if "https://codecov.io/bash" in yml_content:
                            repository["Gyml_codecov"] = repository["Gyml_codecov"] + file_path + ";"
                        if "jacoco" in yml_content and "jacoco.skip=true" not in yml_content:
                            repository["Gyml_jacoco"] = repository["Gyml_jacoco"] + file_path + ";"
                        if "cobertura" in yml_content:
                            repository["Gyml_cobertura"] = repository["Gyml_cobertura"] + file_path + ";"
                        if "javadoc" in yml_content:
                            repository["Gyml_javadoc"] = repository["Gyml_javadoc"] + file_path + ";"
                        j = j + 1
                    else:
                        j = j + 1
                except:
                    repository["Gyml_codecov"] = repository["Gyml_codecov"] + "Skipped;"
                    repository["Gyml_jacoco"] = repository["Gyml_jacoco"] + "Skipped;"
                    repository["Gyml_cobertura"] = repository["Gyml_cobertura"] + "Skipped;"
                    repository["Gyml_javadoc"] = repository["Gyml_javadoc"] + "Skipped;"
                    time.sleep(3)
            else:
                j = len(file_paths)

    i = i + 1
    print(i)

# # Save repositories to a csv file
# with open("file_contents_r.csv", "w", newline="", encoding="utf-8") as csv_file:
#     csv_writer = csv.writer(csv_file)
#     csv_writer.writerow(
#         ["name", "link", "Default Branch", "SHA", "Stargazers Count", "Forks Count",
#          "Maven", "Gradle", "Travis CI", "Github Actions",
#          "Maven Jacoco", " Maven Cobertura", "Maven Javadoc",
#          "Gradle Jacoco", "Gradle Cobertura", "Gradle Javadoc",
#          "Travis Codecov", "Travis Jacoco", " Travis Cobertura", "Travis Javadoc",
#          "GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc"
#          ])
#
#     for repository in repositories:
#         csv_writer.writerow([repository["name"], repository["link"], repository["default_branch"], repository["sha"],
#                              repository["stargazers_count"], repository["forks_count"],
#                              repository["Maven"], repository["Gradle"],
#                              repository["Travis CI"], repository["Github Actions"],
#                              repository["MJacoco"], repository["MCobertura"], repository["MJavadoc"],
#                              repository["GJacoco"], repository["GCobertura"], repository["GJavadoc"],
#                              repository["Tyml_codecov"], repository["Tyml_jacoco"], repository["Tyml_cobertura"],
#                              repository["Tyml_javadoc"],
#                              repository["Gyml_codecov"], repository["Gyml_jacoco"], repository["Gyml_cobertura"],
#                              repository["Gyml_javadoc"]])

# Save repositories to a csv file
with open("file_contents_r.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["link",
         "Maven", "Gradle", "Travis CI", "Github Actions",
         "Maven Jacoco", " Maven Cobertura", "Maven Javadoc",
         "Gradle Jacoco", "Gradle Cobertura", "Gradle Javadoc",
         "Travis Codecov", "Travis Jacoco", " Travis Cobertura", "Travis Javadoc",
         "GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc"
         ])

    for repository in repositories:
        csv_writer.writerow([repository["link"],
                             repository["Maven"], repository["Gradle"],
                             repository["Travis CI"], repository["Github Actions"],
                             repository["MJacoco"], repository["MCobertura"], repository["MJavadoc"],
                             repository["GJacoco"], repository["GCobertura"], repository["GJavadoc"],
                             repository["Tyml_codecov"], repository["Tyml_jacoco"], repository["Tyml_cobertura"],
                             repository["Tyml_javadoc"],
                             repository["Gyml_codecov"], repository["Gyml_jacoco"], repository["Gyml_cobertura"],
                             repository["Gyml_javadoc"]])
