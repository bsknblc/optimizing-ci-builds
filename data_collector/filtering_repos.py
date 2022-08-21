import base64
import copy
import csv
import os
import time

os.chdir("..")

repositories = []
with open("data/file_contents.csv", "r", newline="", encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader, None)
    for row in csv_reader:
        repositories.append(
            {"name": row[0], "link": row[1], "default_branch": row[2], "sha": row[3],
             "stargazers_count": row[4], "forks_count": row[5],
             "Maven": row[6], "Gradle": row[7], "Travis CI": row[8], "Github Actions": row[9],
             "MJacoco": row[10], "MCobertura": row[11], "MJavadoc": row[12],
             "GJacoco": row[13], "GCobertura": row[14], "GJavadoc": row[15],
             "Tyml_codecov": row[16], "Tyml_coveralls": row[17], "Tyml_codacy": row[18],
             "Tyml_jacoco": row[19], "Tyml_cobertura": row[20], "Tyml_javadoc": row[21],
             "Gyml_codecov": row[22], "Gyml_coveralls": row[23], "Gyml_codacy": row[24],
             "Gyml_jacoco": row[25], "Gyml_cobertura": row[26], "Gyml_javadoc": row[27]})
print("Data have been read.")



filtered_repositories = []

for repository in repositories:
    Gyml_codecov = 0
    Gyml_coveralls = 0
    Gyml_codacy = 0
    Gyml_jacoco = 0
    Gyml_cobertura = 0
    Gyml_javadoc = 0

    if repository["Gyml_codecov"]:
        Gyml_codecov = 1

    if repository["Gyml_coveralls"]:
        Gyml_coveralls = 1

    if repository["Gyml_codacy"]:
        Gyml_codacy = 1

    if repository["Gyml_jacoco"]:
        Gyml_jacoco = 1

    if repository["Gyml_cobertura"]:
        Gyml_cobertura = 1

    if Gyml_codecov == 0 and Gyml_coveralls == 0 and Gyml_codacy == 0:
        if Gyml_jacoco == 1 or Gyml_cobertura == 1:
            filtered_repositories.append(repository)

# Save repositories to a csv file
with open("data/filtered_repositories.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["name", "link", "Default Branch", "SHA", "Stargazers Count", "Forks Count",
         "Maven", "Gradle", "Travis CI", "Github Actions",
         "Maven Jacoco", " Maven Cobertura", "Maven Javadoc",
         "Gradle Jacoco", "Gradle Cobertura", "Gradle Javadoc",
         "Travis Codecov", "Travis Coveralls", "Travis Codacy",
         "Travis Jacoco", " Travis Cobertura", "Travis Javadoc",
         "GA Codecov", "GA Coveralls", "GA Codacy",
         "GA Jacoco", " GA Cobertura", "GA Javadoc"
         ])

    for repository in filtered_repositories:
        csv_writer.writerow([repository["name"], repository["link"], repository["default_branch"], repository["sha"],
                             repository["stargazers_count"], repository["forks_count"],
                             repository["Maven"], repository["Gradle"],
                             repository["Travis CI"], repository["Github Actions"],
                             repository["MJacoco"], repository["MCobertura"], repository["MJavadoc"],
                             repository["GJacoco"], repository["GCobertura"], repository["GJavadoc"],
                             repository["Tyml_codecov"], repository["Tyml_coveralls"], repository["Tyml_codacy"],
                             repository["Tyml_jacoco"], repository["Tyml_cobertura"], repository["Tyml_javadoc"],
                             repository["Gyml_codecov"], repository["Gyml_coveralls"], repository["Gyml_codacy"],
                             repository["Gyml_jacoco"], repository["Gyml_cobertura"], repository["Gyml_javadoc"]])