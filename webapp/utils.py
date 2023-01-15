import requests
import urllib.parse

def find_urn(access_token, type, name):

    if type == "company":
        param = "name&name"
    elif type == "person":
        param = "companyName&companyName"

    # Encode the name parameter in the URL
    url = f"https://api.linkedin.com/v2/search/blended?q={urllib.parse.quite(param)}={urllib.parse.quote(name)}"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Extract the first result from the response
        result = response.json()["elements"][0]

        # The result object will contain a "miniProfile" field with the profile's URN
        urn = result["miniProfile"]["entityUrn"]
        return urn
    else:
        return None

def post(access_token, content):
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    data = {
        "author": "urn:li:organization:88070907",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, json=data, headers=headers)

    #if response.status_code == 201:
    
    return response.text