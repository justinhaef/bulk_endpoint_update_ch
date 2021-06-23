# import csv
# import asyncio
import json
import argparse
import logging
import os
import requests
from pathlib import Path
from requests_oauthlib import OAuth2Session

from dotenv import load_dotenv
load_dotenv()

from rich.console import Console

logging.basicConfig(
    filename=Path('app.log'),
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

console = Console()

# We need to get our credintials to get a new Access Token.
client_id = os.getenv("APP_CLIENTID")
client_secret = os.getenv("APP_SECRETID")

refresh_token = os.getenv("REFRESH_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")

base_url = 'https://webexapis.com/v1'

webex = OAuth2Session(client_id)

def main():
    """ Main entry point for the application.
    """
    url = f'{base_url}/workspaces'
    response = requests.get(url=url, headers={'Authorization': f'Bearer {access_token}'})
    if response.status_code == 401:
        logging.warning('Access Token was Expired')
        # get a new access_token
        new_access_token = refresh_my_token()
        # try with new access_token
        response = requests.get(url=url, headers={'Authorization': f'Bearer {new_access_token}'})
    return response

def update(to_update_workspaces):
    for workspace in to_update_workspaces["items"]:
        print(f'Workspace: {workspace}')
        url = f'{base_url}/workspaces/{workspace["id"]}'
        response = requests.put(url=url, json=workspace, headers={'Authorization': f'Bearer {access_token}'})
        if response.status_code == 401:
            logging.warning('Access Token was Expired')
            # get a new access_token
            new_access_token = refresh_my_token()
            # try with new access_token
            response = requests.put(url=url, headers={'Authorization': f'Bearer {new_access_token}'})
    return response

def refresh_my_token():
    # Refresh the Access Token
    logging.warning('Attempting to refresh access token...')
    url = f'{base_url}/access_token?grant_type=refresh_token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    headers = {'accept':'application/json','content-type':'application/x-www-form-urlencoded'}
    response = webex.refresh_token(token_url=url, **payload)
    return response['access_token']


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
        Bulk Endpoint Update Tool for Webex Control Hub
    """,
    )

    argument_parser.add_argument(
        "-o",
        "--option",
        help="Gather or Update all endpoints in Webex Control Hub",
        choices=['gather', 'update'],
        dest="option",
        required=True,
    )

    args = argument_parser.parse_args()

    if args.option == 'gather':
        logging.info('User selected to gather endpoints.')
        response = main()
        json_response = json.loads(response.text)
        print(json.dumps(json_response, indent=4))
        with open(Path('./files/gathered/output.json'), 'w') as outfile:
            json.dump(json_response, outfile)

    if args.option == 'update':
        logging.info('User selected to update endpoints.')
        with open(Path('./files/to_update/updated.json')) as json_file:
            data = json.load(json_file)
            response = update(data)
            json_response = json.loads(response.text)
            print(json.dumps(json_response, indent=4))

