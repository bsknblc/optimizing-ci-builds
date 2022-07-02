import base64
import copy
import csv
import os
import time

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
print("Data have been read.")

maven_count = 0
gradle_count = 0
travis_count = 0
gaci_count = 0
MJacoco_count = 0
MCobertura_count = 0
MJavadoc_count = 0
GJacoco_count = 0
GCobertura_count = 0
GJavadoc_count = 0
Tyml_codecov_count = 0
Tyml_jacoco_count = 0
Tyml_cobertura_count = 0
Tyml_javadoc_count = 0
Gyml_codecov_count = 0
Gyml_jacoco_count = 0
Gyml_cobertura_count = 0
Gyml_javadoc_count = 0

MJacocoCobertura = 0
MCoberturaJavadoc = 0
MJacocoJavadoc = 0
MJacocoCoberturaJavadoc = 0
MJacocoCoberturaJavadocAny = 0

GJacocoCobertura = 0
GCoberturaJavadoc = 0
GJacocoJavadoc = 0
GJacocoCoberturaJavadoc = 0
GJacocoCoberturaJavadocAny = 0

Tyml_codecov_jacoco = 0
Tyml_codecov_cobertura = 0
Tyml_codecov_javadoc = 0
Tyml_jacoco_cobertura_javadoc = 0

Gyml_codecov_jacoco = 0
Gyml_codecov_cobertura = 0
Gyml_codecov_javadoc = 0
Gyml_jacoco_cobertura_javadoc = 0

MTyml_codecov = 0
MTyml_jacoco = 0
MTyml_cobertura = 0
MTyml_javadoc = 0
MTyml_codecov_jacoco = 0
MTyml_codecov_cobertura = 0
MTyml_codecov_javadoc = 0
MTyml_jacoco_cobertura_javadoc = 0

GTyml_codecov = 0
GTyml_jacoco = 0
GTyml_cobertura = 0
GTyml_javadoc = 0
GTyml_codecov_jacoco = 0
GTyml_codecov_cobertura = 0
GTyml_codecov_javadoc = 0
GTyml_jacoco_cobertura_javadoc = 0

MGyml_codecov = 0
MGyml_jacoco = 0
MGyml_cobertura = 0
MGyml_javadoc = 0
MGyml_codecov_jacoco = 0
MGyml_codecov_cobertura = 0
MGyml_codecov_javadoc = 0
MGyml_jacoco_cobertura_javadoc = 0

GGyml_codecov = 0
GGyml_jacoco = 0
GGyml_cobertura = 0
GGyml_javadoc = 0
GGyml_codecov_jacoco = 0
GGyml_codecov_cobertura = 0
GGyml_codecov_javadoc = 0
GGyml_jacoco_cobertura_javadoc = 0

for repository in repositories:
    maven = 0
    gradle = 0
    travis = 0
    github_actions = 0
    MJacoco = 0
    MCobertura = 0
    MJavadoc = 0
    GJacoco = 0
    GCobertura = 0
    GJavadoc = 0
    Tyml_codecov = 0
    Tyml_jacoco = 0
    Tyml_cobertura = 0
    Tyml_javadoc = 0
    Gyml_codecov = 0
    Gyml_jacoco = 0
    Gyml_cobertura = 0
    Gyml_javadoc = 0

    if repository["Maven"]:
        maven = 1
        maven_count += 1

    if repository["Gradle"]:
        gradle = 1
        gradle_count += 1

    if repository["Travis CI"]:
        travis = 1
        travis_count += 1

    if repository["Github Actions"]:
        github_actions = 1
        gaci_count += 1

    if repository["MJacoco"]:
        MJacoco = 1
        MJacoco_count += 1

    if repository["MCobertura"]:
        MCobertura = 1
        MCobertura_count += 1
        if MJacoco == 1:
            MJacocoCobertura += 1

    if repository["MJavadoc"]:
        MJavadoc = 1
        MJavadoc_count += 1
        if MCobertura == 1:
            MCoberturaJavadoc += 1
        if MJacoco == 1:
            MJacocoJavadoc += 1
        if MCobertura == 1 and MJacoco == 1:
            MJacocoCoberturaJavadoc += 1

    if MJacoco == 1 or MCobertura == 1 or MJacoco == 1:
        MJacocoCoberturaJavadocAny += 1

    if repository["GJacoco"]:
        GJacoco = 1
        GJacoco_count += 1

    if repository["GCobertura"]:
        GCobertura = 1
        GCobertura_count += 1
        if GJacoco == 1:
            GJacocoCobertura += 1

    if repository["GJavadoc"]:
        GJavadoc = 1
        GJavadoc_count += 1
        if GCobertura == 1:
            GCoberturaJavadoc += 1
        if GJacoco == 1:
            GJacocoJavadoc += 1
        if GCobertura == 1 and GJacoco == 1:
            GJacocoCoberturaJavadoc += 1

    if GJacoco == 1 or GCobertura == 1 or GJacoco == 1:
        GJacocoCoberturaJavadocAny += 1

    if repository["Tyml_codecov"]:
        Tyml_codecov = 1
        Tyml_codecov_count += 1
        if maven == 1:
            MTyml_codecov += 1
        if gradle == 1:
            GTyml_codecov += 1

    if repository["Tyml_jacoco"]:
        Tyml_jacoco = 1
        Tyml_jacoco_count += 1
        if Tyml_codecov == 1:
            Tyml_codecov_jacoco += 1
        if maven == 1:
            MTyml_jacoco += 1
            if Tyml_codecov == 1:
                MTyml_codecov_jacoco += 1
        if gradle == 1:
            GTyml_jacoco += 1
            if Tyml_codecov == 1:
                GTyml_codecov_jacoco += 1

    if repository["Tyml_cobertura"]:
        Tyml_cobertura = 1
        Tyml_cobertura_count += 1
        if Tyml_codecov == 1:
            Tyml_codecov_cobertura += 1
        if maven == 1:
            MTyml_cobertura += 1
            if Tyml_codecov == 1:
                MTyml_codecov_cobertura += 1
        if gradle == 1:
            GTyml_cobertura += 1
            if Tyml_codecov == 1:
                GTyml_codecov_cobertura += 1

    if repository["Tyml_javadoc"]:
        Tyml_javadoc = 1
        Tyml_javadoc_count += 1
        if Tyml_codecov == 1:
            Tyml_codecov_javadoc += 1
        if maven == 1:
            MTyml_javadoc += 1
            if Tyml_codecov == 1:
                MTyml_codecov_javadoc += 1
        if gradle == 1:
            GTyml_javadoc += 1
            if Tyml_codecov == 1:
                GTyml_codecov_javadoc += 1

    if Tyml_jacoco or Tyml_cobertura or Tyml_javadoc:
        Tyml_jacoco_cobertura_javadoc += 1
        if maven == 1:
            MTyml_jacoco_cobertura_javadoc += 1
        if gradle == 1:
            GTyml_jacoco_cobertura_javadoc += 1

    if repository["Gyml_codecov"]:
        Gyml_codecov = 1
        Gyml_codecov_count += 1
        if gradle == 1:
            GGyml_codecov += 1
        if maven == 1:
            MGyml_codecov += 1

    if repository["Gyml_jacoco"]:
        Gyml_jacoco = 1
        Gyml_jacoco_count += 1
        if Gyml_codecov == 1:
            Gyml_codecov_jacoco += 1
        if gradle == 1:
            GGyml_jacoco += 1
            if Gyml_codecov == 1:
                GGyml_codecov_jacoco += 1
        if maven == 1:
            MGyml_jacoco += 1
            if Gyml_codecov == 1:
                MGyml_codecov_jacoco += 1

    if repository["Gyml_cobertura"]:
        Gyml_cobertura = 1
        Gyml_cobertura_count += 1
        if Gyml_codecov == 1:
            Gyml_codecov_cobertura += 1
        if gradle == 1:
            GGyml_cobertura += 1
            if Gyml_codecov == 1:
                GGyml_codecov_cobertura += 1
        if maven == 1:
            MGyml_cobertura += 1
            if Gyml_codecov == 1:
                MGyml_codecov_cobertura += 1

    if repository["Gyml_javadoc"]:
        Gyml_javadoc = 1
        Gyml_javadoc_count += 1
        if Gyml_codecov == 1:
            Gyml_codecov_javadoc += 1
        if gradle == 1:
            GGyml_javadoc += 1
            if Gyml_codecov == 1:
                GGyml_codecov_javadoc += 1
        if maven == 1:
            MGyml_javadoc += 1
            if Gyml_codecov == 1:
                MGyml_codecov_javadoc += 1

    if Gyml_jacoco or Gyml_cobertura or Gyml_javadoc:
        Gyml_jacoco_cobertura_javadoc += 1
        if gradle == 1:
            GGyml_jacoco_cobertura_javadoc += 1
        if maven == 1:
            MGyml_jacoco_cobertura_javadoc += 1

# Save statistics to a csv file
with open("statistics.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["Maven", "Gradle", "Travis CI", "Github Actions"])

    csv_writer.writerow([maven_count, gradle_count, travis_count, gaci_count])

    csv_writer.writerow(["Maven"])

    csv_writer.writerow(
        ["Maven Jacoco", " Maven Cobertura", "Maven Javadoc",
         "Jacoco&Cobertura", "Cobertura&Javadoc", "Jacoco&Javadoc",
         "Jacoco&Cobertura&Javadoc", "Jacoco or Cobertura or Javadoc"])

    csv_writer.writerow(
        [MJacoco_count, MCobertura_count, MJavadoc_count,
         MJacocoCobertura, MCoberturaJavadoc, MJacocoJavadoc,
         MJacocoCoberturaJavadoc, MJacocoCoberturaJavadocAny])

    csv_writer.writerow(["Gradle"])

    csv_writer.writerow(
        ["Gradle Jacoco", "Gradle Cobertura", "Gradle Javadoc",
         "Jacoco&Cobertura", "Cobertura&Javadoc", "Jacoco&Javadoc",
         "Jacoco&Cobertura&Javadoc", "Jacoco or Cobertura or Javadoc"])

    csv_writer.writerow(
        [GJacoco_count, GCobertura_count, GJavadoc_count,
         GJacocoCobertura, GCoberturaJavadoc, GJacocoJavadoc,
         GJacocoCoberturaJavadoc, GJacocoCoberturaJavadocAny])

    csv_writer.writerow(["Travis CI"])

    csv_writer.writerow(
        ["Travis Codecov", "Travis Jacoco", "Travis Cobertura", "Travis Javadoc",
         "Tyml_codecov_jacoco", "Tyml_codecov_cobertura", "Tyml_codecov_javadoc",
         "Tyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [Tyml_codecov_count, Tyml_jacoco_count, Tyml_cobertura_count, Tyml_javadoc_count,
         Tyml_codecov_jacoco, Tyml_codecov_cobertura, Tyml_codecov_javadoc,
         Tyml_jacoco_cobertura_javadoc])

    csv_writer.writerow(["Github Actions"])

    csv_writer.writerow(
        ["GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc",
         "Gyml_codecov_jacoco", "Gyml_codecov_cobertura", "Gyml_codecov_javadoc",
         "Gyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [Gyml_codecov_count, Gyml_jacoco_count, Gyml_cobertura_count, Gyml_javadoc_count,
         Gyml_codecov_jacoco, Gyml_codecov_cobertura, Gyml_codecov_javadoc,
         Gyml_jacoco_cobertura_javadoc])

    csv_writer.writerow(["Maven Projects - Travis CI"])

    csv_writer.writerow(
        ["Travis Codecov", "Travis Jacoco", "Travis Cobertura", "Travis Javadoc",
         "Tyml_codecov_jacoco", "Tyml_codecov_cobertura", "Tyml_codecov_javadoc",
         "Tyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [MTyml_codecov, MTyml_jacoco, MTyml_cobertura, MTyml_javadoc,
         MTyml_codecov_jacoco, MTyml_codecov_cobertura, MTyml_codecov_javadoc,
         MTyml_jacoco_cobertura_javadoc])

    csv_writer.writerow(["Gradle Projects - Travis CI"])

    csv_writer.writerow(
        ["Travis Codecov", "Travis Jacoco", "Travis Cobertura", "Travis Javadoc",
         "Tyml_codecov_jacoco", "Tyml_codecov_cobertura", "Tyml_codecov_javadoc",
         "Tyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [GTyml_codecov, GTyml_jacoco, GTyml_cobertura, GTyml_javadoc,
         GTyml_codecov_jacoco, GTyml_codecov_cobertura, GTyml_codecov_javadoc,
         GTyml_jacoco_cobertura_javadoc])

    csv_writer.writerow(["Maven Projects - Github Actions"])

    csv_writer.writerow(
        ["GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc",
         "Gyml_codecov_jacoco", "Gyml_codecov_cobertura", "Gyml_codecov_javadoc",
         "Gyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [MGyml_codecov, MGyml_jacoco, MGyml_cobertura, MGyml_javadoc,
         MGyml_codecov_jacoco, MGyml_codecov_cobertura, MGyml_codecov_javadoc,
         MGyml_jacoco_cobertura_javadoc])

    csv_writer.writerow(["Gradle Projects - Github Actions"])

    csv_writer.writerow(
        ["GA Codecov", "GA Jacoco", " GA Cobertura", "GA Javadoc",
         "Gyml_codecov_jacoco", "Gyml_codecov_cobertura", "Gyml_codecov_javadoc",
         "Gyml_jacoco_cobertura_javadoc Any"])

    csv_writer.writerow(
        [GGyml_codecov, GGyml_jacoco, GGyml_cobertura, GGyml_javadoc,
         GGyml_codecov_jacoco, GGyml_codecov_cobertura, GGyml_codecov_javadoc,
         GGyml_jacoco_cobertura_javadoc])
