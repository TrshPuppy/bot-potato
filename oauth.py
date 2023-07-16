# This module will handle updating the oauth keys/tokens which need to be refreshed every 4-5 hours
import json
import requests
import time


def check_auth_status():
    if is_auth_expired():
        auth_response = get_new_auth_token()
        print(f"auth response  = {auth_response.status_code}")

        if auth_response.status_code == 400:
            if auth_response.text == "Invalid refresh token":
                #
                # We'll have to handle this case better.
                # ... The Twitch refresh token does eventually expire
                # ... According to the documentation anyway...
                #
                get_new_refresh_token()
            else:
                # We may get a 400 response for other unhandled reasons:
                print(
                    f"Status code 400 from Twitch for oauth refresh. Unhandled Error."
                )
                print(f"Twitch Response Message: {auth_response.text}")

        if auth_response.status_code == 200:
            # Turn response object into JSON object:
            auth_resp_json = auth_response.json()
            print(f"auth resp json = {auth_resp_json}")

            update_auth_json(auth_resp_json)

    return


def get_new_auth_token():
    # Build the request URL:
    TWITCH_REFRESH_URL = "https://id.twitch.tv/oauth2/token"

    # Load Oauth data from JSON:
    with open("data/api.json", "r") as f:
        oauth = json.load(f)

    # Set variables needed for request:
    CLIENT_ID = oauth["CLIENT_ID"]
    CLIENT_SECRET = oauth["CLIENT_SECRET"]
    GRANT_TYPE = "refresh_token"
    REFRESH_TOKEN = oauth["REFRESH_TOKEN"]
    HEADERS = {"Content_Typpe": "application/x-www-form-urlencoded"}

    # Send a POST request to fetch a new OAuth token
    response = requests.post(
        TWITCH_REFRESH_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": GRANT_TYPE,
            "refresh_token": REFRESH_TOKEN,
        },
        headers=HEADERS,
    )

    # # Make sure we actually succeeded at refreshing the token:
    # response_json = response.json()

    # if response_json["message"] == "Invalid refresh token":
    #     new_r_token = get_new_refresh_token()
    #     return False

    return response


def is_auth_expired():
    return True


def get_new_refresh_token():
    # This is not handled yet
    # # The Twitch refresh token will eventually expire...
    print(f"You need a new refresh token")
    return "this is a fake refresh token"


def update_auth_json(rj):
    # Build properties from response to update json:
    OA_TOKEN = rj["access_token"]
    REFRESH_TOKEN = rj["refresh_token"]
    OA_EXPIRE = rj["expires_in"]
    LAST_REFRESH = int(time.time())

    # Load JSON file for reading:
    with open("data/api.json", "r") as f:
        oauth_data = json.load(f)

    oauth_data["OA_TOKEN"] = OA_TOKEN
    oauth_data["REFRESH_TOKEN"] = REFRESH_TOKEN
    oauth_data["OA_EXPIRE"] = OA_EXPIRE
    oauth_data["LAST_REFRESH"] = LAST_REFRESH

    # Load JSON file  for writing:
    with open("data/api.json", "w") as wf:
        json.dump(oauth_data, wf)

    # Example response:
    # response = {
    #     "access_token": "",
    #     "expires_in": <int>,
    #     "refresh_token": "",
    #     "scope": ["string"],
    #     "token_type": "bearer",
    # }

    return


check_auth_status()
