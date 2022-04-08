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
        super().setUpClass()
        # Create Database
        Command.handle(self)


class UpdateModelTests(HDTRTests):
    def test_deliquent_hard_drives(self):
        # The database should have only 4 overdue hard drives.
        requests = Request.objects.filter(request_status=Request.Request_Status.OVERDUE)
        hard_drives = HardDrive.objects.none()
        for r in requests:
            hard_drives |= HardDrive.objects.filter(request=r)

        self.assertEqual(len(hard_drives), 3)

class URLTests(HDTRTests):

    def test_login_page_maintainer(self):
        c = Client()
        response = c.post('/login/', {USERNAME:MAINTAINER_USERNAME, PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)

    def test_login_page_requestor(self):
        c = Client()
        response = c.post('/login/', {USERNAME: REQUESTOR_USERNAME, 
                                        PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)

    def test_login_page_admin(self):
        c = Client()
        response = c.post('/login/', {USERNAME: ADMIN_USERNAME, 
                                        PASSWORD_STR:PASSWORD})
        self.assertEqual(response.status_code, REDIRECT)
    
    def test_view_request_authenticated(self):
        c = Client()
        c.login(username=MAINTAINER_USERNAME, password=PASSWORD)
        response = c.post('/view_request/')
        self.assertEqual(response.status_code, 200)

    def test_view_request_non_authenticated(self):
        c = Client()
        response = c.post('/view_request/')
        self.assertEqual(response.status_code, REDIRECT)
