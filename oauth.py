# This module will handle updating the oauth keys/tokens which need to be refreshed every 4-5 hours
import json
import requests


def check_auth_status():
    if is_auth_expired():
        auth_response = get_new_auth_token()

        if auth_response.message == "Invalid refresh token":
            get_new_refresh_token()
            #
            # We'll have to handle this case better.
            # ... The Twitch refresh token does eventually expire
            # ... According to the documentation anyway...
            #
        if auth_response.status == 400:
            # We may get a 400 response for other unhandled reasons:
            print(f"Status code 400 from Twitch for oauth refresh. Unhandled Error.")
            print(f"Twitch Response Message: {auth_response.message}")

        if auth_response.status == 200:
            update_auth_json(auth_response)

        print(f"response = {auth_response.text}")

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

    # response = {
    #     "access_token": "qo7ju8mvsyex9gw39cpg3vmrmsa63x",
    #     "expires_in": 13022,
    #     "refresh_token": "ycp6k35tn80exju6rjnrxldus9x0ko81bg43qq0j6g0igh0n84",
    #     "scope": ["channel:moderate", "chat:edit", "chat:read"],
    #     "token_type": "bearer",
    # }

    return response


def is_auth_expired():
    return True


def get_new_refresh_token():
    # This is not handled yet
    # # The Twitch refresh token will eventually expire...
    print(f"You need a new refresh token")
    return "this is a fake refresh token"


async def update_auth_json():
    return


check_auth_status()
