import os
import requests
import json

class GithubHelper:
    def __init__(self, application, repo_name, branch='branch1', test_folder='PR_Tracker', json_response=None):
        self.token = ''
        actual_value = ''
        self.request_url = 'https://api.github.com/repos/Neethu04/demo_repo/pulls?state=all'
        self.files_list = []
        self.test_folder = test_folder
        self.application = self.test_folder.split('/')[-1]
        self.json_response = json_response
        self.repo_name = repo_name
        self.branch = branch

    def get_files(self):
        if not self.json_response:
            resp = self.github_request(self.test_folder)
            self.add_files(resp)
        else:
            with open(self.json_response) as data_file:
                data = json.load(data_file)

            for repo in data:
                if repo.get('type') == 'dir':
                    path_elements = repo.get('path').split('/')
                    index_start = path_elements.index(self.application)
                    condensed_path = '/'.join(path_elements[index_start:])
                    nested_resp_req_url = repo.get('url')+'&access_token='+self.token
                    nested_resp = requests.get(nested_resp_req_url, verify=True)
                    nested_resp.raise_for_status()
                    self.add_files(nested_resp, '/'.join(condensed_path.split('/')[1:]))
                else:
                    self.files_list.append(repo.get('name'))
        return self.files_list

    def github_request(self, application, url=None):
        resp = requests.get(
            self.request_url.format(application=application, repo_name=self.repo_name, branch=self.branch,
            test_folder=self.test_folder, token=self.token),
            verify=True)
        return resp