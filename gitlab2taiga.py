#!/usr/bin/env python3

import ujson
import pandas as pd
import requests
import json
import sys, getopt
import getpass
import validators

ENDPOINT_GET_PROJECT = "/api/v1/projects"
ENDPOINT_GET_MEMBERS = "/api/v1/memberships"
ENDPOINT_LOGIN = "/api/v1/auth"

def main(argv):
    try:
        opts, args = getopt.getopt(argv,'hi:m:e:u:')
    except getopt.GetoptError:
        print ('gitlab2taiga.py -i <issues file> -m <members file> -e <taiga endpoint> -u <taiga username>')
        sys.exit(2)
    if len(opts) != 4:
        print ('gitlab2taiga.py -i <issues file> -m <members file> -e <taiga endpoint> -u <taiga username>')
        sys.exit(2)
    else:
        print (opts)
        for opt, arg in opts:
            if opt == '-h':
                print ('gitlab2taiga.py -i <issues file> -m <members file> -e <taiga endpoint> -u <taiga username>')
                sys.exit()
            elif opt in '-i':
                issues_file = arg
            elif opt in '-m':
                members_file = arg
            elif opt in '-e':
                endpoint = arg
            elif opt in '-u':
                username = arg
            else:
                print ('gitlab2taiga.py -i <issues file> -m <members file> -e <taiga endpoint> -u <taiga username>')
        if (username is not None) and (issues_file is not None) and (members_file is not None) and (endpoint is not None):
            getAccessToken(username, issues_file, members_file, endpoint)
            getMemberships(username, issues_file, members_file, endpoint)

def importIssues(issues, members ):
    records = map(ujson.loads, open(path_issues, encoding="utf8"))
    df = pd.DataFrame.from_records(records)
    pd.set_option("display.max_rows", None, "display.max_columns", None,'display.max_colwidth', None)
    #print(df.keys())
    #print(df[['title','description','author_id']])
    print(df[['description']].head(15))
    #print(df.iloc[2])

def getAccessToken(username, issues_file, members_file, endpoint):
    if (validators.url(endpoint)):
        global password
        password = getpass.getpass()
        d = {}
        d['password'] = password;
        d['type'] = 'normal';
        d['username'] = username;
        response = requests.post(endpoint + ENDPOINT_LOGIN, data = d)
        if response.ok:
            responseJson = response.json()
            try:
                global authToken
                authToken = responseJson['auth_token']
                print ('Auth token request successful')
            except:
                print ('We could not get the authorization token from the login request')
                exit (2)
        else:
            print ('The response from the server is not valid')
            exit (2)
    else:
        print ('The endpoint provided is not a valid url')
        exit (2)

def getMemberships(username, issues_file, members_file, endpoint):
    if (validators.url(endpoint)):
        if (password is not None):
            if (authToken is not None):
                headers = {"Authorization": "Bearer " + authToken}
                response = requests.get(endpoint + ENDPOINT_GET_MEMBERS, headers = headers)
                if response.ok:
                    responseJson = response.json()
                    try:
                        memberName = []
                        for membership in responseJson:
                            memberName.append(membership['full_name'])
                        print ('The current memberships are: ' , memberName)
                        return memberName
                    except:
                        print ('We could not get the memberships full name')
                else:
                    print ('The response from the server is not valid')
                    exit (2)
            else:
                print ('The auth token is not correct')
                exit (2)
        else:
            print ('The password is not correct')
            exit (2)
    else:
        print ('The endpoint provided is not a valid url')
        exit (2)

def createIssue(username, issues_file, members_file, endpoint):
    if (validators.url(endpoint)):
        if (password is not None):
            if (authToken is not None):
                print (authToken)
            else:
                print ('The auth token is not correct')
                exit (2)
        else:
            print ('The password is not correct')
            exit (2)
    else:
        print ('The endpoint provided is not a valid url')
        exit (2)

if __name__ == "__main__":
   main(sys.argv[1:])
