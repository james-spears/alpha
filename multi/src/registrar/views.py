"""
    defines registrar related views
"""
# import google.oauth2.credentials
import os
import logging
import json

import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests

from rest_framework.response import Response
from rest_framework import viewsets, filters, permissions, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from . import serializers
from . import models

LOGGER = logging.getLogger("django")
CLIENT_SECRET = os.path.join(
    os.path.dirname(__file__),
    'client_secret.json'
)
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    ]

USER = get_user_model()

def credentials_to_dict(credentials):
    """
        turns the google creds into dict
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'id_token': credentials.id_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }

def valid_google_user(email):
    """√alidate users"""
    if email[-10:] != "@example.com":
        return False
    else:
        return True

# ViewSets define the view behaviour

class UsernameViewSet(viewsets.ModelViewSet):
    """
        standard ModelViewset for the user model with
        search capabilities
    """
    # You should not need to be authenticated in
    # order to use the Username endpoint. This is
    # used in order to check whether a username
    # has been taken.
    permission_classes = (permissions.AllowAny,)
    queryset = USER.objects.all()
    serializer_class = serializers.UserCheckSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=username',)


class CompanyViewSet(viewsets.ModelViewSet):
    """
        standard ModelViewset for the user model with
        search capabilities
    """
    # You should not need to be authenticated in
    # order to use the Username endpoint. This is
    # used in order to check whether a username
    # has been taken.
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=company_name',)


class ModuleViewSet(viewsets.ModelViewSet):
    """
        standard ModelViewset for the user model with
        search capabilities
    """
    # You should not need to be authenticated in
    # order to use the Username endpoint. This is
    # used in order to check whether a username
    # has been taken.
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Module.objects.all()
    serializer_class = serializers.ModuleSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=module',)


class ApiKeyViewSet(viewsets.ModelViewSet):
    """
        standard ModelViewset for the user model with
        search capabilities
    """
    # You should not need to be authenticated in
    # order to use the Username endpoint. This is
    # used in order to check whether a username
    # has been taken.
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.ApiKey.objects.all()
    serializer_class = serializers.ApiKeySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=name',)


class Oauth2EndpointViewSet(viewsets.ModelViewSet):
    """
        standard ModelViewset for the user model with
        search capabilities
    """
    # You should not need to be authenticated in
    # order to use the Username endpoint. This is
    # used in order to check whether a username
    # has been taken.
    permission_classes = (permissions.IsAuthenticated,)
    queryset = models.Oauth2Endpoint.objects.all()
    serializer_class = serializers.Oauth2EndpointSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=provider',)


class GoogleOauth2Redirect(viewsets.ViewSet):
    """
        direct user to google Oauth 2.0 server
    """
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        """
            list method provides get request endpoint fot eh redirect url
        """
        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET,
            SCOPES)

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2callback-list'))

        # Generate URL for request to Google's OAuth 2.0 server.
        # Use kwargs to set optional request parameters.
        authorization_url, state = flow.authorization_url(
            # Enable offline access so that you can refresh an access token without
            # re-prompting the user for permission. Recommended for web server apps.
            access_type='offline',
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes='true')

        request.session['state'] = state

        return redirect(authorization_url)


class GoogleOauth2Callback(viewsets.ViewSet):
    """
        direct user to google Oauth 2.0 server
    """
    # You should not need to be authenticated in
    # order to use the Oauth2 callback endpoint.
    # This view will be called from Google servers
    # once they have tried to sign the users
    # credentials.
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        """
            success
        """
        try:
            state = request.session['state']
        except KeyError as exc:
            # Improper Oauth flow likely.
            LOGGER.exception(exc.args[0])
            redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2testfail-list'))
            return redirect(redirect_uri)

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            CLIENT_SECRET, scopes=SCOPES, state=state
        )

        redirect_uri = request.build_absolute_uri(
            reverse('api:googleoauth2callback-list'))
        flow.redirect_uri = redirect_uri

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_code = request.query_params.get("code")
        try:
            flow.fetch_token(code=authorization_code)
        except ValueError as exc:
            # Improper Oauth flow likely.
            LOGGER.exception(exc.args[0])
            redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2testfail-list'))
            return redirect(redirect_uri)

        # Store credentials in the session.
        # ACTION ITEM: In a production app, you likely want to save these
        #              credentials in a persistent database instead.
        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)
        token = credentials.id_token
        client_id = credentials.client_id
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), client_id)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, google_requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            # userid = idinfo['sub']
            messages.add_message(request, messages.INFO, json.dumps(request.session['credentials']))
            redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2testpass-list'))
            return redirect(redirect_uri)
        except ValueError as exc:
            # Invalid token
            LOGGER.exception(exc.args[0])
            redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2testfail-list'))
            return redirect(redirect_uri)


class GoogleOauth2TestPass(viewsets.ViewSet):
    """
        After Google has authenticated the user
        we should either fetch their user record
        or create it if it does not already
        exist. Then generate a JWT from the user record
        and return.
    """
    # You should not need to be authenticated in
    # order to pass Oauth2 flow. Here is where the
    # authentication happens.
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        """
            list method provides get request endpoint
        """
        credentials = messages.get_messages(request)
        try:
            if len(credentials) != 1:
                raise ValueError('Credentials should be length 1.')

            for credential in credentials:
                credential = json.loads(credential.message)

                # Retrieve human readable user information
                # from Google API.
                token = credential["token"]
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                try:
                    oauth2 = models.Oauth2Endpoint.objects.get(
                        provider="Google"
                    )
                except ObjectDoesNotExist as exc:
                    LOGGER.exception(exc.args[0])
                    redirect_uri = request.build_absolute_uri(
                        reverse('api:googleoauth2testfail-list'))
                    return redirect(redirect_uri)

                user_info = requests.get(oauth2.url, headers=headers)
                user_dict = json.loads(user_info.text)

                # Now that we have the user information we
                # need to either pull the user record from the
                # db or create it.

                try:
                    current_user = USER.objects.get(
                        username=user_dict["name"],
                        first_name=user_dict["given_name"],
                        last_name=user_dict["family_name"],
                        email=user_dict["email"],
                    )
                    LOGGER.info("Found user: %s", current_user.username)
                except ObjectDoesNotExist:
                    current_user = USER.objects.create_user(
                        username=user_dict["name"],
                        first_name=user_dict["given_name"],
                        last_name=user_dict["family_name"],
                        email=user_dict["email"],
                    )
                    current_user.set_unusable_password()
                    current_user.save()
                    LOGGER.info("Could not find user: %s", current_user.username)
                    LOGGER.info("Created user: %s", current_user.username)

                # At this point the user has been authenticated and their
                # record has been found. We will generate the initial login
                # jwt here.

                refresh = RefreshToken.for_user(current_user)

                response = {
                    "id_token": token,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }

                response_status = status.HTTP_200_OK
                return Response(response, status=response_status)

        except ValueError as exc:
            # Invalid token
            LOGGER.exception(exc.args[0])
            redirect_uri = request.build_absolute_uri(reverse('api:googleoauth2testfail-list'))
            return redirect(redirect_uri)

class GoogleOauth2TestFail(viewsets.ViewSet):
    """
        direct user to google Oauth 2.0 server
    """
    # You should not need to be authenticated in
    # order to fail Oauth2 flow.
    permission_classes = (permissions.AllowAny,)

    def list(self, request):
        """
            list method provides get request endpoint
        """
        response = {
            "detail": _("Could not authenticate user.")
        }
        response_status = status.HTTP_401_UNAUTHORIZED
        return Response(response, status=response_status)


class JWTRefreshViewSet(viewsets.ViewSet):
    """
        This endpoint is made available in order to
        provide the ability to generate new tokens
        access token if provided the Alpha signed
        refresh JWT.
    """
    # You should not need to be authenticated in
    # order to refresh a JWT.
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        """
            post method
        """
        # Here we will try to refresh the token.
        try:
            refresh_token = RefreshToken(request.data.get("refresh"))
            refresh_token.verify()
            # If the token can be verified then refresh
            # the access token.
            response = {
                "access": str(refresh_token.access_token),
                "refresh": str(refresh_token),
            }
            response_status = status.HTTP_200_OK
            return Response(response, status=response_status)
        # If the token cannot be verified it will throw
        # a "TokenError".
        except TokenError:
            # If the TokenError has been thrown then
            # return an error in the response.
            response = {
                "detail": _("Could not refresh token.")
            }
            response_status = status.HTTP_401_UNAUTHORIZED
            return Response(response, status=response_status)
