"""
    This module contains the registrar
    tests.
"""
import os
from collections import OrderedDict
from django.test import TransactionTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from registrar import models
from registrar import views
# Create your tests here.

THIS_DIR = os.path.dirname(__file__)
B64_IMG_DIR = os.path.join(THIS_DIR, 'test_image_b64.txt')
USER = get_user_model()
with open(B64_IMG_DIR, 'r') as b64_file:
    TEST_B64_IMG = b64_file.read()

class UnitTestCompanyViewSet(TransactionTestCase):
    """
        UnitTestCompanyViewSet holds unit
        tests for CompanyViewSet.
    """
    def setUp(self):
        """
            Set up all the models needed for this test.
        """
        company = models.Company.objects.create(
            company_id="0",
            company_name="Test0",
            company_logo=SimpleUploadedFile(
                name='test_image.jpg',
                content=open(
                    os.path.join(
                        os.path.dirname(__file__), 'test_image.jpg'), 'rb').read(),
                content_type='image/jpeg'
            )
        )
        company.save()

        company = models.Company.objects.create(
            company_id="1",
            company_name="Test1",
            company_logo=SimpleUploadedFile(
                name='test_image.jpg',
                content=open(
                    os.path.join(
                        os.path.dirname(__file__), 'test_image.jpg'), 'rb').read(),
                content_type='image/jpeg'
            )
        )
        company.save()

        user = models.AlphaUser.objects.create_user(
            username="TestUser",
        )
        user.save()

    def tearDown(self):
        """
            Set up all the models needed for this test.
        """
        company = models.Company.objects.get(
            company_id="0",
            company_name="Test0",
        )
        company.delete()

        company = models.Company.objects.get(
            company_id="1",
            company_name="Test1",
        )
        company.delete()

        user = models.AlphaUser.objects.get(
            username="TestUser",
        )
        user.delete()

    def test_authenticated_detail(self):
        """
            This method tests an authenticated get
            to model/company/1/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "company_id": "0",
            "company_name": "Test0",
            "company_logo_b64": TEST_B64_IMG.encode(),
            "id": 1,
        }
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/company/1/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.CompanyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=1)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_x_authenticated_detail_404(self):
        """
            This method tests an authenticated get
            to model/company/99/ (404), and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Not found."
        }
        exp_status_code = 404

        # Set up request
        url_string = "/api/v1/model/company/99/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.CompanyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=99)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_detail(self):
        """
            This method tests an unauthenticated get
            to model/company/3/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/company/3/"
        request = APIRequestFactory().get(url_string)
        viewset = views.CompanyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=3)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_authenticated_list(self):
        """
            This method tests an authenticated call
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation (We need to remember to increment the
        # primary key, as there will already have been a
        # company record added and removed by the time this test
        # is excecuted).
        exp_data = [
            OrderedDict(
                [
                    ("company_id", "0"),
                    ("company_name", "Test0"),
                    ("company_logo_b64", TEST_B64_IMG.encode()),
                    ("id", 3),
                ],
            ),
            OrderedDict(
                [
                    ("company_id", "1"),
                    ("company_name", "Test1"),
                    ("company_logo_b64", TEST_B64_IMG.encode()),
                    ("id", 4),
                ],
            )
        ]
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/company/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.CompanyViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_list(self):
        """
            This method tests an unauthenticated get
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/company/"
        request = APIRequestFactory().get(url_string)
        viewset = views.CompanyViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_create(self):
        """
            This method tests an unauthenticated get
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        body = dict()
        url_string = "/api/v1/model/company/"
        request = APIRequestFactory().post(url_string, body)
        viewset = views.CompanyViewSet.as_view({"post": "create"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)


class UnitTestModuleViewSet(TransactionTestCase):
    """
        UnitTestModuleViewSet holds unit
        tests for ModuleViewSet viewset.
    """
    def setUp(self):
        """
            Set up all the models needed for this test.
        """
        module = models.Module.objects.create(
            module_name="TestModule0",
            url="TestModuleURL0"
        )
        module.save()

        module = models.Module.objects.create(
            module_name="TestModule1",
            url="TestModuleURL1"
        )
        module.save()

        user = models.AlphaUser.objects.create_user(
            username="TestUser",
        )
        user.save()

    def tearDown(self):
        """
            Set up all the models needed for this test.
        """
        module = models.Module.objects.get(
            module_name="TestModule0",
            url="TestModuleURL0"
        )
        module.delete()

        module = models.Module.objects.get(
            module_name="TestModule1",
            url="TestModuleURL1"
        )
        module.delete()

        user = models.AlphaUser.objects.get(
            username="TestUser",
        )
        user.delete()

    def test_authenticated_detail(self):
        """
            This method tests an authenticated get
            to model/company/1/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "module_name": "TestModule0",
            "url": "TestModuleURL0",
            "id": 1,
        }
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/module/1/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ModuleViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=1)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_x_authenticated_detail_404(self):
        """
            This method tests an authenticated get
            to model/module/99/ (404), and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Not found."
        }
        exp_status_code = 404

        # Set up request
        url_string = "/api/v1/model/module/99/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ModuleViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=99)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_detail(self):
        """
            This method tests an unauthenticated get
            to model/module/3/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/module/3/"
        request = APIRequestFactory().get(url_string)
        viewset = views.ModuleViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=3)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_authenticated_list(self):
        """
            This method tests an authenticated call
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation (We need to remember to increment the
        # primary key, as there will already have been a
        # company record added and removed by the time this test
        # is excecuted).
        exp_data = [
            OrderedDict(
                [
                    ("module_name", "TestModule0"),
                    ("url", "TestModuleURL0"),
                    ("id", 3),
                ],
            ),
            OrderedDict(
                [
                    ("module_name", "TestModule1"),
                    ("url", "TestModuleURL1"),
                    ("id", 4),
                ],
            ),
        ]
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/module/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ModuleViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_list(self):
        """
            This method tests an unauthenticated get
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/module/"
        request = APIRequestFactory().get(url_string)
        viewset = views.ModuleViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_create(self):
        """
            This method tests an unauthenticated get
            to model/module/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        body = dict()
        url_string = "/api/v1/model/module/"
        request = APIRequestFactory().post(url_string, body)
        viewset = views.ModuleViewSet.as_view({"post": "create"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)


class UnitTestOauth2EndpointViewSet(TransactionTestCase):
    """
        UnitTestOauth2EndpointViewSet holds unit
        tests for Oauth2EndpointViewSet viewset.
    """
    def setUp(self):
        """
            Set up all the models needed for this test.
        """
        oauth_2_endpoint = models.Oauth2Endpoint.objects.create(
            provider="TestOauth2Endpoint0",
            url="TestOauth2EndpointURL0"
        )
        oauth_2_endpoint.save()

        oauth_2_endpoint = models.Oauth2Endpoint.objects.create(
            provider="TestOauth2Endpoint1",
            url="TestOauth2EndpointURL1"
        )
        oauth_2_endpoint.save()

        user = models.AlphaUser.objects.create_user(
            username="TestUser",
        )
        user.save()

    def tearDown(self):
        """
            Set up all the models needed for this test.
        """
        oauth_2_endpoint = models.Oauth2Endpoint.objects.get(
            provider="TestOauth2Endpoint0",
            url="TestOauth2EndpointURL0"
        )
        oauth_2_endpoint.delete()

        oauth_2_endpoint = models.Oauth2Endpoint.objects.get(
            provider="TestOauth2Endpoint1",
            url="TestOauth2EndpointURL1"
        )
        oauth_2_endpoint.delete()

        user = models.AlphaUser.objects.get(
            username="TestUser",
        )
        user.delete()

    def test_authenticated_detail(self):
        """
            This method tests an authenticated get
            to model/oauth2endpoint/1/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "provider": "TestOauth2Endpoint0",
            "url": "TestOauth2EndpointURL0",
            "id": 1,
        }
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/oauth2endpoint/1/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.Oauth2EndpointViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=1)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_x_authenticated_detail_404(self):
        """
            This method tests an authenticated get
            to model/oauth2endpoint/99/ (404), and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Not found."
        }
        exp_status_code = 404

        # Set up request
        url_string = "/api/v1/model/oauth2endpoint/99/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.Oauth2EndpointViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=99)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_detail(self):
        """
            This method tests an unauthenticated get
            to model/oauth2endpoint/3/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/oauth2endpoint/3/"
        request = APIRequestFactory().get(url_string)
        viewset = views.Oauth2EndpointViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=3)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_authenticated_list(self):
        """
            This method tests an authenticated call
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation (We need to remember to increment the
        # primary key, as there will already have been a
        # company record added and removed by the time this test
        # is excecuted).
        exp_data = [
            OrderedDict(
                [
                    ("provider", "TestOauth2Endpoint0"),
                    ("url", "TestOauth2EndpointURL0"),
                    ("id", 3),
                ],
            ),
            OrderedDict(
                [
                    ("provider", "TestOauth2Endpoint1"),
                    ("url", "TestOauth2EndpointURL1"),
                    ("id", 4),
                ],
            ),
        ]
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/oauth2endpoint/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.Oauth2EndpointViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_list(self):
        """
            This method tests an unauthenticated get
            to model/company/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/oauth2endpoint/"
        request = APIRequestFactory().get(url_string)
        viewset = views.Oauth2EndpointViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_create(self):
        """
            This method tests an unauthenticated get
            to model/oauth2endpoint/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        body = dict()
        url_string = "/api/v1/model/oauth2endpoint/"
        request = APIRequestFactory().post(url_string, body)
        viewset = views.Oauth2EndpointViewSet.as_view({"post": "create"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

class UnitTestApiKeyViewSet(TransactionTestCase):
    """
        UnitTestApiKeyViewSet holds unit
        tests for ApiKeyViewSet viewset.
    """
    def setUp(self):
        """
            Set up all the models needed for this test.
        """
        api_key = models.ApiKey.objects.create(
            api_key="ApiKey0",
            name="TestApiKey0",
            url="TestApiKeyURL0"
        )
        api_key.save()

        api_key = models.ApiKey.objects.create(
            api_key="ApiKey1",
            name="TestApiKey1",
            url="TestApiKeyURL1"
        )
        api_key.save()

        user = models.AlphaUser.objects.create_user(
            username="TestUser",
        )
        user.save()

    def tearDown(self):
        """
            Set up all the models needed for this test.
        """
        api_key = models.ApiKey.objects.get(
            name="TestApiKey0",
            url="TestApiKeyURL0"
        )
        api_key.delete()

        api_key = models.ApiKey.objects.get(
            name="TestApiKey1",
            url="TestApiKeyURL1"
        )
        api_key.delete()

        user = models.AlphaUser.objects.get(
            username="TestUser",
        )
        user.delete()

    def test_authenticated_detail(self):
        """
            This method tests an authenticated get
            to model/apikey/1/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "name": "TestApiKey0",
            "url": "TestApiKeyURL0",
            "id": 1,
        }
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/apikey/1/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ApiKeyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=1)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_x_authenticated_detail_404(self):
        """
            This method tests an authenticated get
            to model/apikey/99/ (404), and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Not found."
        }
        exp_status_code = 404

        # Set up request
        url_string = "/api/v1/model/apikey/99/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ApiKeyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=99)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)


    def test_unauthenticated_detail(self):
        """
            This method tests an unauthenticated get
            to model/apikey/3/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/apikey/3/"
        request = APIRequestFactory().get(url_string)
        viewset = views.ApiKeyViewSet.as_view({"get": "retrieve"}, detail=True)

        # Fake api call
        response = viewset(request, pk=3)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_authenticated_list(self):
        """
            This method tests an authenticated call
            to model/apikey/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation (We need to remember to increment the
        # primary key, as there will already have been a
        # company record added and removed by the time this test
        # is excecuted).
        exp_data = [
            OrderedDict(
                [
                    ("name", "TestApiKey0"),
                    ("url", "TestApiKeyURL0"),
                    ("id", 3),
                ],
            ),
            OrderedDict(
                [
                    ("name", "TestApiKey1"),
                    ("url", "TestApiKeyURL1"),
                    ("id", 4),
                ],
            ),
        ]
        exp_status_code = 200

        # Set up request
        url_string = "/api/v1/model/apikey/"
        request = APIRequestFactory().get(url_string)
        user = USER.objects.get(username="TestUser")
        force_authenticate(request, user=user)
        viewset = views.ApiKeyViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_list(self):
        """
            This method tests an unauthenticated get
            to model/apikey/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        url_string = "/api/v1/model/apikey/"
        request = APIRequestFactory().get(url_string)
        viewset = views.ApiKeyViewSet.as_view({"get": "list"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)

    def test_unauthenticated_create(self):
        """
            This method tests an unauthenticated get
            to model/apikey/, and so the response body
            is checked. This test fails if the response
            body is misconfigured.
        """

        # Expectation
        exp_data = {
            "detail": "Authentication credentials were not provided.",
        }
        exp_status_code = 401

        # Set up request
        body = dict()
        url_string = "/api/v1/model/apikey/"
        request = APIRequestFactory().post(url_string, body)
        viewset = views.ApiKeyViewSet.as_view({"post": "create"})

        # Fake api call
        response = viewset(request)

        # Assertions RE: response body.
        self.assertEqual(exp_status_code, response.status_code)
        self.assertEqual(exp_data, response.data)
