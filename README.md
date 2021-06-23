# Python Webex Bulk Endpoint Update Tool for Control Hub

## This is not for use in production, this is a demonstration of how to use OAuth and Webex API.  Use at your own discretion. 

## Purpose

This appliation simply uses the Cisco Webex Meetings REST API to gather all the workspaces from Control Hub.  It then saves that output to the `files/gathered/` folder.  The end user will make the modifications needed, save that modified output to `files/to_update` folder and run the application again.  

## How to run

>Only tested on Python version 3.8.2

>This assumes you've already created your [Webex Integrations](https://developer.webex.com/docs/integrations).

> Helpful OAuth2.0 Summary for Webex [Walk Through](https://developer.webex.com/blog/real-world-walkthrough-of-building-an-oauth-webex-integration)
1. `git clone https://github.com/justinhaef/webex_meeting_host_counter.git`
1. `pip install -r requirements.txt`
1. Rename `.env_template` to `.env`.
1. Change the values in `.env` file to your values. 
1. Run `python auth.py` to get the Access and Refresh Tokens
1. Add those values to your `.env` file.
1. Run `python app.py -o gather` to discover all workspaces in Control Hub.
1. Make modifications needed in `files/gathered/output.json`. 
1. Duplicate the `files/gathered/output.json` that has been modified to `files/to_update/updated.json`.
1. Run `python app.py -o update` to put all modified workspaces into Control Hub. 

## Caveat

This application has not yet been tested to loop over multiple workspaces yet.  

## Things to remember

1. The Scopes selected when the Integration was created need to be defined in the `auth.py` scopes list.
1. The redirect URI in `auth.py` needs to match what was defined when the Integration was created. 
1. Treat your client_id, client_secret, refresh_token, auth_token and access_token with care. 