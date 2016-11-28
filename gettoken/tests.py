from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.six import StringIO
from django.core.management.base import CommandError
from django.core.management import call_command
from gettoken.models import Snapshot
import os
"""
Antes de realizar los test actualizar el token de los usuarios
"""


class SimpleTest(TestCase):
    fixtures = ['gettoken/fixtures/users.json', 'gettoken/fixtures/data.json']

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.assertNotEqual(self.user, None, msg="User is None")
        self.client.login(username=self.user.username,
                          password=self.user.password)

    def require_autentication(self):
        response = self.client.get('/useradmin/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/listsnapshot/')
        self.assertEqual(response.status_code, 200)

    def command_capture(self):
        out = StringIO()
        self.assertRaises(CommandError,
                          call_command('capture',
                                       '--user=131088583997853',
                                       '--type=contacts', verbosity=3,
                                       interactive=False, stdout=out),
                          )
        self.assertRaises(CommandError,
                          call_command('capture',
                                       '--user=131088583997853',
                                       '--type=pages', verbosity=3,
                                       interactive=False, stdout=out),
                          )
        out = StringIO()
        self.assertRaises(CommandError,
                          call_command('capture',
                                       '--user=Testprueba Api Code',
                                       '--type=contacts', verbosity=3,
                                       interactive=False, stdout=out),
                          )
        out = StringIO()
        self.assertRaises(CommandError,
                          call_command('capture',
                                       '--user=Testprueba Api Code',
                                       '--type=pages', verbosity=3,
                                       interactive=False, stdout=out),
                          )

    """
    To run the test is necessary comment the line 137 in capture.py
    """
    def get_file_s3(self):
        snapshot = Snapshot.objects.get(pk=1)

        os.chdir(os.getcwd()+"/"+snapshot.query_type+"/")

        datafile = open(snapshot.filename, 'r')
        res = datafile.read()
        datafile.close()

        self.assertEqual(res, snapshot.getDataS3())
