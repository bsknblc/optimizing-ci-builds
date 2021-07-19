import base64, copy, csv, os, requests
github_auth_token = os.environ["G_AUTH_TOKEN"]
headers = {
    'Authorization': 'token ' + github_auth_token
}
repositories = []
# 14*30=420
# There are 30 repos in every page, so with 14 iterations we get 420 java repositories.
for i in range(1, 15):
    url = "https://api.github.com/search/repositories?q=language:java&sort=forks&order=desc&page=" + str(i)
    response = requests.get(url=url, headers=headers).json()
    for repository in response["items"]:
        repositories.append({"name": repository["full_name"], "link": repository["html_url"]})
filtered_repositories = []
for repository in repositories:
    files = requests.get(url="https://api.github.com/repos/" + repository["name"] + "/contents", headers=headers).json()
    for file in files:
        # checking if the repository has pom.xml in its root
        if file["name"] == "pom.xml":
            repository["build-tool"] = "maven"
            response = requests.get(url="https://api.github.com/repos/"+ repository["name"] +"/contents/pom.xml", headers=headers).json()
            pom_content = base64.b64decode(response["content"]).decode("utf-8")
            # checking if the pom.xml contains "jacoco-maven-plugin" keyword 
            if "jacoco-maven-plugin" in pom_content:
                repository["coverage-tool"] = "jacoco"
                filtered_repositories.append(copy.deepcopy(repository))
            # checking if the pom.xml contains "cobertura-maven-plugin" keyword 
            if "cobertura-maven-plugin" in pom_content:
                repository["coverage-tool"] = "cobertura"
                filtered_repositories.append(copy.deepcopy(repository))
            break
        elif file["name"] == "build.gradle":
            repository["build-tool"] = "gradle"
            response = requests.get(url="https://api.github.com/repos/"+ repository["name"] +"/contents/build.gradle", headers=headers).json()
            gradle_content = base64.b64decode(response["content"]).decode("utf-8")
            if "jacoco" in gradle_content:
                repository["coverage-tool"] = "jacoco"
                filtered_repositories.append(copy.deepcopy(repository))
            if "cobertura" in gradle_content:
                repository["coverage-tool"] = "cobertura"
                filtered_repositories.append(copy.deepcopy(repository))
            break
# Remove duplicates
final_repositories = []
[final_repositories.append(repository) for repository in filtered_repositories if repository not in final_repositories]
# Save repositories to a csv file
with open("data.csv", "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["name", "link", "build-tool", "coverage-tool"])
    for repository in final_repositories:
        csv_writer.writerow([repository["name"], repository["link"], repository["build-tool"], repository["coverage-tool"]])
