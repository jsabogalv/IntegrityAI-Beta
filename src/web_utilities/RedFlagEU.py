import requests
import threading

class TimeoutException(Exception):
    pass

def timeout_handler():
    raise TimeoutException("Query timed out")

def search_organization(api_key, query, timeout=180):
    base_url = "http://api.redflags.eu"
    endpoints = {
        "organization": "/organization",
        "organizations": "/organizations",
        "notice": "/notice",
        "notices": "/notices"
    }

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    # Function to print organization details
    def print_organization(org):
        print(f"ID: {org['id']}")
        print(f"Name: {org['name']}")
        print(f"Type: {org.get('type', 'N/A')}")
        print(f"Calls: {org.get('calls', 'N/A')}")
        print(f"Wins: {org.get('wins', 'N/A')}")
        print("-" * 40)

    def run_queries():
        try:
            # Search for organizations
            params = {
                "count": 10,
                "page": 1,
                "nameLike": query,
                "access_token": api_key
            }

            response = requests.get(base_url + endpoints["organizations"], params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "result" in data:
                organizations = data["result"]
                print("Organizations found:")
                for org in organizations:
                    print_organization(org)
            else:
                print("No organizations found.")

            # Search for notices by contracting authority name
            params = {
                "count": 10,
                "page": 1,
                "contractingAuthorityNameLike": query,
                "access_token": api_key
            }

            response = requests.get(base_url + endpoints["notices"], params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "result" in data:
                notices = data["result"]
                print("Notices found:")
                for notice in notices:
                    print(f"ID: {notice['id']}")
                    print(f"Title: {notice['title']}")
                    print(f"Contracting Authority: {notice['contractingOrgName']}")
                    print(f"Date: {notice['date']}")
                    print(f"URL: {notice.get('url', 'N/A')}")
                    print("-" * 40)
            else:
                print("No notices found.")

            # Search for notices by winner name
            params = {
                "count": 10,
                "page": 1,
                "winnerNameLike": query,
                "access_token": api_key
            }

            response = requests.get(base_url + endpoints["notices"], params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "result" in data:
                notices = data["result"]
                print("Notices found by winner name:")
                for notice in notices:
                    print(f"ID: {notice['id']}")
                    print(f"Title: {notice['title']}")
                    print(f"Contracting Authority: {notice['contractingOrgName']}")
                    print(f"Date: {notice['date']}")
                    print(f"URL: {notice.get('url', 'N/A')}")
                    print("-" * 40)
            else:
                print("No notices found by winner name.")

            # Search for notices by text
            params = {
                "count": 10,
                "page": 1,
                "textLike": query,
                "access_token": api_key
            }

            response = requests.get(base_url + endpoints["notices"], params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if "result" in data:
                notices = data["result"]
                print("Notices found by text:")
                for notice in notices:
                    print(f"ID: {notice['id']}")
                    print(f"Title: {notice['title']}")
                    print(f"Contracting Authority: {notice['contractingOrgName']}")
                    print(f"Date: {notice['date']}")
                    print(f"URL: {notice.get('url', 'N/A')}")
                    print("-" * 40)
            else:
                print("No notices found by text.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from RedFlags API: {e}")

    thread = threading.Thread(target=run_queries)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        print("Query timed out. Please try again later.")
        thread._stop()

if __name__ == "__main__":
    api_key = "TU CLAVE AQUI"  # Replace with your actual API key
    query = "ELN"  # Replace with the name or identifier you want to search for
    search_organization(api_key, query)
