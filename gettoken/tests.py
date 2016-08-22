from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
import views
from models import User as UserFacebook


class SimpleTest(TestCase):
    def setUp(self):
        self.c = Client()
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

    def test_index(self):
        # Create an instance of a GET request.
        request = self.factory.get('/token/')
        request.user = self.user
        request.user = AnonymousUser()
        response = views.index_view(request)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        # Create an instance of a GET request.
        youtoken = "EAANOJKNjQEABAI9POE2NtPl2UQEgA6aTXRN1MTzKoeMmVmhJxkoZAP"
        youtoken += "JaSlrZCAaigKE7DyZA19E51Xz4BTB8DlbQAjjrYSZAAq1Nem2UXzZ"
        youtoken += "AkrL8cSXbCDG1VV3ZB4EU4g4ZAXkKDk4qTvxZCk4maymr6NhEENC0A"
        youtoken += "CnwE0Fm1mYtbwZDZD"
        youexpires = "4616"
        url = '/token/savetoken/' + youtoken + '/' + youexpires + '/'
        data = {
                # 'first_name': 'Testprueba',
                # 'last_name': 'Api Code',
                # 'name': 'Testprueba Api Code',
                # 'id': '131088583997853',
                # 'birthday': '09/25/1987',
                # 'email': 'franz.lopez@webeando.me',
                # 'location': {
                #     'id': '106257366076550',
                #     'name': 'Cochabamba, Bolivia'
                # },
                # 'education': [
                #     {
                #         'type': 'High School',
                #         'id': '146735779099800',
                #         'school':
                #         {
                #             'id': '324467527686872',
                #             'name': 'Colegio Marista Nuestra Sef1ora del Pilar'
                #         }
                #     },
                #     {
                #         'type': 'College',
                #         'id': '141975276242517',
                #         'concentration': [
                #             {
                #                 'id': '454248364650135',
                #                 'name': 'Information system'
                #             }
                #         ],
                #         'school': {
                #             'id': '106106219420905',
                #             'name': 'University of San Simn'
                #         }
                #     }
                # ]
        }
        print UserFacebook.objects.all()
        request = self.factory.post(url, data)
        response = views.savetoken(request, youtoken, youexpires)
        # self.assertRedirects(response, 'token')
        self.assertEqual(response.status_code, 302)
