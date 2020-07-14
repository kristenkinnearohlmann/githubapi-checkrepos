import datetime
import requests
import sys

def get_user_repos(gh_api_url,user_nm,page_nbr):
    if gh_api_url != "":
        gh_api_url += f"/users/{user_nm}/repos?page={page_nbr}&per_page=100"
        response = requests.get(gh_api_url)

        if response:
            return response
        else:
            # print(f"Error: {response.status_code}")
            # print("Error description: ")
            # print(f"Headers: ")
            # for key, value in response.headers.items():
            #     print(f"   {key}: {value}")
            response.raise_for_status()                
            return False
    else:
        print(f"No URL available for processing.")

if __name__ == "__main__":
    print(f"Script start: {datetime.datetime.now()}")

    gh_api_url = "https://api.github.com"
    user_nm = "kristenkinnearohlmann"

    page_nbr = 1
    repos = {}
    is_success = True
    while is_success:
        results = get_user_repos(gh_api_url, user_nm, page_nbr)

        if results == False:
            print(f"False case: {results}")
            is_success = False
        else:        
            results_json = results.json()
            if len(results_json) == 0:
                is_success = False
            else:
                # print(results_json)
                print(f"Status: {results.status_code}. Page {page_nbr}: {len(results_json)} records.")

                for result in results_json:
                    language = result["language"]   
                    name = result["name"] 
                    id = result["id"]

                    if "-000" in name:
                        source = "Flatiron"
                    else:
                        source = "TBD"

                    isForked = result["fork"]

                    if repos.get(language) is None:
                        repos[language] = [{"name":name, "id":id, "isForked":isForked, "source":source}]
                    else:
                        repos[language].append({"name":name, "id":id, "isForked":isForked, "source":source})

                page_nbr += 1
    original_stdout = sys.stdout
    with open('repos.txt', 'w') as f:
        sys.stdout = f
        for key in repos.keys():
            print(f"{key}: {len(repos[key])} repos")     
            for repo in repos[key]:
                if repo["source"] != "Flatiron":
                    print(f"\t{repo}")
        sys.stdout = original_stdout
    print(f"Script end: {datetime.datetime.now()}")

## OAuth help?
## https://stackoverflow.com/questions/17622439/how-to-use-github-api-token-in-python-for-requesting


## keys for returned data
# dict_keys(['id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url', 'description', 'fork', 'url', 'forks_url', 'keys_url', 'collaborators_url', 'teams_url', 'hooks_url', 'issue_events_url', 'events_url', 'assignees_url', 'branches_url', 'tags_url', 'blobs_url', 'git_tags_url', 'git_refs_url', 'trees_url', 'statuses_url', 'languages_url', 'stargazers_url', 'contributors_url', 'subscribers_url', 'subscription_url', 'commits_url', 'git_commits_url', 'comments_url', 'issue_comment_url', 'contents_url', 'compare_url', 'merges_url', 'archive_url', 'downloads_url', 'issues_url', 'pulls_url', 'milestones_url', 'notifications_url', 'labels_url', 'releases_url', 'deployments_url', 'created_at', 'updated_at', 'pushed_at', 'git_url', 'ssh_url', 'clone_url', 'svn_url', 'homepage', 'size', 'stargazers_count', 'watchers_count', 'language', 'has_issues', 'has_projects', 'has_downloads', 'has_wiki', 'has_pages', 'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 
# 'license', 'forks', 'open_issues', 'watchers', 'default_branch'])                