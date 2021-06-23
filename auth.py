from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
load_dotenv()
import os
# import json

client_id = os.getenv("APP_CLIENTID")
client_secret = os.getenv("APP_SECRETID")
redirect_uri = "https://localhost:8080/webex-teams-auth.html"

authorization_base_url = 'https://webexapis.com/v1/authorize'
token_url = 'https://webexapis.com/v1/access_token/'

scope = [
    "spark:kms",
    "spark-admin:devices_read",
    "spark-admin:devices_write",
    "spark-admin:workspaces_read",
    "spark-admin:workspaces_write",
]

webex = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

authorization_url, state = webex.authorization_url(authorization_base_url)
print(f'Please go here and authorize: {authorization_url}')

redirect_response = input('Paste the full redirect URL here:')


response = webex.fetch_token(
    token_url,
    client_secret=client_secret,
    include_client_id=True,
    authorization_response=redirect_response
    )

print(f"Access Token: {response['access_token']}")
print(f"Refresh Token: {response['refresh_token']}")
