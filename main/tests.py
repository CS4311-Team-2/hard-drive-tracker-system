from django.test import TestCase, Client

from main.management.commands.updatemodels import (ADMINISTRATOR_USERNAME, Command, PASSWORD,
                                                    ADMIN_USERNAME, 
                                                    MAINTAINER_USERNAME, 
                                                    REQUESTOR_USERNAME)
from main.models.hard_drive import HardDrive
from main.models.request import Request
from main.models.event import Event
from main.models.amendment import Amendment
from main.models.log import Log
from users.models import UserProfile

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


class IntegrationTests(HDTRTests):

    def test_edit_hard_drive(self):
        c = Client()
        c.login(username=MAINTAINER_USERNAME, password=PASSWORD)
        response = c.post('/view_hard_drive/2', {"manufacturer":"HP"})
        hard_drive = HardDrive.objects.get(id=2)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(hard_drive.manufacturer, "HP")

    def test_edit_hard_drive_log(self):
        c = Client()
        c.login(username=MAINTAINER_USERNAME, password=PASSWORD)
        response = c.post('/view_hard_drive/2', {"manufacturer":"HP"})
        log = Log.objects.get(user=UserProfile.objects.get(username=MAINTAINER_USERNAME))
        self.assertEqual(response.status_code, 301)
        self.assertIsNotNone(log)

    def view_user(self):
        c = Client()
        c.login(username=ADMINISTRATOR_USERNAME, password=PASSWORD)
        response = c.post('/view_user/2', {"branch_chief_email":"None"})
        user = UserProfile.objects.get(username=ADMINISTRATOR_USERNAME)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(user.branch_chief_email, "None")


    # Fails because its not implemented. 
    # def test_edit_request(self):
    #     c = Client()
    #     c.login(username=MAINTAINER_USERNAME, password=PASSWORD)
    #     response = c.post('/view_request/2', {"event_location":"Utep"})
    #     request = HardDrive.objects.get(id=2)
    #     event = Event.objects.get(request=request)
    #     self.assertEqual(response.status_code, 301)
    #     self.assertEqual(event.event_location, "Utep")

    def test_submit_admendment(self):
        c = Client()
        c.login(username=REQUESTOR_USERNAME, password=PASSWORD)
        amendment_post = {
            "description":"Simple Admendment", 
            "decision_date":"12-01-22",
            "comment":"Comment",
            "status": Amendment.Status.PENDING
            }
        response = c.post('/view_request/2', amendment_post)
        request = HardDrive.objects.get(id=2)
        amendment = Amendment.objects.get(request=request)
        self.assertEqual(response.status_code, 301)

        self.assertEqual(amendment.description, amendment_post["description"])
        self.assertEqual(amendment.comment, amendment_post["comment"])
        self.assertEqual(amendment.status, amendment_post["status"])

