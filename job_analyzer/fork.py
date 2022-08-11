import json
import requests
import sys
import time
import os
import base64


# API endpoint
GITHUB_API = 'https://api.github.com'

github_auth_token = os.environ["G_AUTH_OP"]
headers = {
    'Authorization': 'token ' + github_auth_token
}


# Fork project on GitHub
def fork_project(repository):
    try:
        url = GITHUB_API + '/repos/' + repository
        response = requests.delete(url=url, headers=headers).json()
        print(response)
    except:
        time.sleep(1)
    time.sleep(1)
    try:
        url = GITHUB_API + '/repos/' + repository + '/forks'
        response = requests.post(url=url, headers=headers).json()
        print(response)
    except:
        time.sleep(1)


def take_ci_file(repository):
    file_path = ".github/workflows/RunPetClinic.yml"
    try:
        response = requests.get(
            url="https://api.github.com/repos/" + repository + "/contents/" + file_path,
            headers=headers).json()
        if "content" in response:
            content = base64.b64decode(response["content"]).decode("utf-8")
            with open('a.yaml', 'w') as a:
                a.write(content)
            parse_ci_file()
    except:
        time.sleep(1)


def parse_ci_file():
    with open('a.yaml') as a, open('b.yaml', 'w') as b:
        x = a.readline()
        indent = 0
        file_count = 1
        while x != "":
            x = a.readline()
            if "- uses" in x or "- name" in x or "- run" in x:
                indent = len(x) - len(x.lstrip())
                change = ' ' * indent + "- run: touch file" + str(file_count) + "\n"
                file_count = file_count + 1
                b.write(change)
                b.write(x)
            else:
                b.write(x)


def main():
    # PHASE-1: COLLECTION
    """FORKING THE PROJECT (VIA GITHUB API)"""
    """PARSING THE YAML FILE"""
    """CHANGING THE YAML FILE"""
    fork_project("bsknblc/spring-petclinic")
    take_ci_file("optimizing-ci-builds/spring-petclinic")

    # # PHASE-2: SETUP
    # """SETTING UP RUNNER"""
    # """SETTING UP THE ENVIRONMENT FOR THE RUNNER AND THE INOTIFYWAIT"""
    # """RUNNING THE RUNNER AND THE INOTIFYWAIT"""
    # token: str = "some another dummy token"
    # runner_version: str = "2.294.0"
    # tar_filename: str = f"linux-x64-{runner_version}.tar.gz"
    # utils.setup_runner(tar_filename=tar_filename, runner_version=runner_version, token=token)
    #
    # # PHASE-3: EXECUTION
    # """COMMITTING THE CHANGES IN THE YAML, TRIGGERING THE RUNNER AND INOTIFYWAIT"""
    # monitored_dir_path: str = ""
    # csv_filename: str = ""
    # os.popen(f"inotifywait -mr {monitored_dir_path} --format %T,%w%f,%e --timefmt %T -o {csv_filename}.csv")
    #
    # # PHASE-4: ANALYSIS
    # """ANALYZING THE CSV PRODUCED BY INOTIFYWAIT"""
    # """PRINTING THE JOB (LINE NUMBER) FROM THE YAML FILE CAUSING UNNECESSARY USAGE"""


if __name__ == "__main__":
    main()