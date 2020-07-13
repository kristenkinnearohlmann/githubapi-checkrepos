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
                print(f"Page count: {page_nbr}")
                print(f"Record count: {len(results_json)}")                 
                print(f"Status code: {results.status_code}")

                for result in results_json:
                    language = result["language"]   
                    name = result["name"] 

                    if "-000" in name:
                        source = "Flatiron"
                    else:
                        source = "TBD"

                    isForked = result["fork"]

                    if repos.get(language) is None:
                        repos[language] = [{"name":name,"isForked":isForked,"source":source}]
                    else:
                        repos[language].append({"name":name,"isForked":isForked,"source":source})

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
## code from old version
                # created_at = result["created_at"]
                # description = result["description"]
                # pushed_at = result["pushed_at"]

                # if ((name.find('-000') == -1) and (language is not None)):
                #     print(f"{name}\nCreated: {created_at}\nDescription: {description}\nLanguage: {language}\nPushed: {pushed_at}\nFork: {fork}\n")