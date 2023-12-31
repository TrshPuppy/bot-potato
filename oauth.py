# This module will handle updating the oauth keys/tokens which need to be refreshed every 4-5 hours
import json
import requests
import time


def check_auth_status():
    if is_auth_expired():
        auth_response = get_new_auth_token()

        # Check status codes first:
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

            update_auth_json(auth_resp_json)


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

    return response


def is_auth_expired():
    #
    # ... We will check how long it's been since
    # ... last refresh to determine if we should
    # ... pre-emptively ask Twitch for a new one:
    #
    CHECK_WINDOW = 5 * 60  # set to 5 minutes
    current_time = int(time.time())  # should be in seconds

    # Load details from data/api.json:
    with open("data/api.json", "r") as f:
        auth_data = json.load(f)

    last_refresh_time = auth_data["LAST_REFRESH"]  # should also be in seconds
    auth_expiration = auth_data["OA_EXPIRE"]

    # Check to see if we are w/i 5 mins of the expiration or over:
    if current_time - last_refresh_time >= auth_expiration - CHECK_WINDOW:
        print("OAUTH TOKEN EXPIRED")
        return True

    print("OAUTH NOT EXPIRED")
    return False


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
