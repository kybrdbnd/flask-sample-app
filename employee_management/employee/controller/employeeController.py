import random
import string

import boto3
from flask import current_app

client = boto3.client('cognito-idp')


def update_name_slug(data):
    name = data['name']
    nameObjs = name.split(' ')
    nameObjs = list(map(lambda x: x.lower(), nameObjs))
    data['nameSlug'] = '-'.join(nameObjs)
    return data


def generate_random_password():
    S = 8  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    upperCase = random.choices(string.ascii_uppercase, k=4)
    lowerCase = random.choices(string.ascii_lowercase, k=4)
    digits = random.choices(string.digits, k=4)
    combinedLetters = upperCase + lowerCase + digits
    password = ''.join(random.sample(combinedLetters, k=S))
    return password


def create_cognito_user(email):
    try:
        password = generate_random_password()
        response = client.admin_create_user(
            UserPoolId=current_app.config['COGNITO_USERPOOL_ID'],
            Username=email,
            TemporaryPassword=password,
            ForceAliasCreation=False,
            MessageAction='SUPPRESS'
        )
        print(f"cognito user {email} created successfully")
        return password
    except Exception as err:
        print(err)


def add_user_cognito_group(email, groupName):
    try:
        response = client.admin_add_user_to_group(
            UserPoolId=current_app.config['COGNITO_USERPOOL_ID'],
            Username=email,
            GroupName=groupName
        )
        print(f"user {email} added to group {groupName} successfully")
    except Exception as err:
        print(err)


def authenticate_user(username, password):
    """get the access token from the cognito user pool"""
    try:
        response = client.admin_initiate_auth(
            UserPoolId=current_app.config['COGNITO_USERPOOL_ID'],
            ClientId=current_app.config['COGNITO_APP_CLIENT_ID'],
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return {
            'access_token': response['AuthenticationResult']['AccessToken'],
            'refresh_token': response['AuthenticationResult']['RefreshToken']
        }
    except Exception as err:
        print(f"incorrect username/password, {str(err)}")
    return None


def confirm_user(username, password):
    try:
        response = client.admin_set_user_password(
            UserPoolId=current_app.config['COGNITO_USERPOOL_ID'],
            Username=username,
            Password=password,
            Permanent=True
        )
        print(f"user {username} confirmed")
    except Exception as err:
        print(err)
