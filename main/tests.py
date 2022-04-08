from django.test import TestCase, Client

from main.management.commands.updatemodels import (Command, PASSWORD,
                                                    ADMIN_USERNAME, 
                                                    MAINTAINER_USERNAME, 
                                                    REQUESTOR_USERNAME)
from main.models.hard_drive import HardDrive
from main.models.request import Request

REDIRECT = 302
USERNAME = 'username'
PASSWORD_STR = 'password'

class HDTRTests(TestCase):
    @classmethod
    def setUpClass(self):
        # Popluate the database in the test environment. 
        super().setUpClass()
        # Create Database
        Command.handle(self)


class UpdateModelTests(HDTRTests):
    def test_deliquent_hard_drives(self):
        # Tests that the database only has 3 overdue hard drives.
        requests = Request.objects.filter(request_status=Request.Request_Status.OVERDUE)
        hard_drives = HardDrive.objects.none()
        for r in requests:
            hard_drives |= HardDrive.objects.filter(request=r)

        self.assertEqual(len(hard_drives), 3)

class URLTests(HDTRTests):

    def test_login_page_maintainer(self):
        # Tests that the Maintainer logins and succesfully redirects. 
        c = Client()
        response = c.post('/login/', {USERNAME:MAINTAINER_USERNAME, PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)

    def test_login_page_requestor(self):
        # Tests that the Requestor logins and succesfully redirects. 
        c = Client()
        response = c.post('/login/', {USERNAME: REQUESTOR_USERNAME, 
                                        PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)

    def test_login_page_admin(self):
        # Tests that the Admin logins and succesfully redirects. 
        c = Client()
        response = c.post('/login/', {USERNAME: ADMIN_USERNAME, 
                                        PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)

    def test_login_page(self):
        # Tests that incorrect login info does not redirect.
        c = Client()
        response = c.post('/login/', {USERNAME: '', 
                                        PASSWORD_STR:''})
        self.assertEqual(response.status_code, 200)
    
    def test_view_request_authenticated(self):
        # Tests that the view request pages renders if user is authenticated.
        c = Client()
        c.login(username=MAINTAINER_USERNAME, password=PASSWORD)
        response = c.post('/view_request/')
        self.assertEqual(response.status_code, 200)

    def test_view_request_non_authenticated(self):
        # Tests that the view request pages redirects if user is not authenicated.
        c = Client()
        response = c.post('/view_request/')
        self.assertEqual(response.status_code, REDIRECT)
