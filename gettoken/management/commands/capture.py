from django.core.management.base import BaseCommand, CommandError
from gettoken.models import User
from time import gmtime, strftime
import json
import pprint
import requests


"""
python manage.py
closepoll --server=pyserver --port=8080,443,25,22,21 --keyword=pyisgood
python manage.py capture --type=pages --user=<user_id>
"""


class Command(BaseCommand):
    help = 'Ingrese el id del usuario'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--type', type=str, help='Type ',
                            required=True)
        parser.add_argument('-u', '--user', type=int, help='User ID',
                            required=True)

    def handle(self, *args, **options):
        user = None
        token = None
        if 'user' in options:
            try:
                user = User.objects.get(pk=options['user'])
                token = user.fb_token.token
            except User.DoesNotExist:
                string = 'User "%s" does not exist' % options['user']
                raise CommandError(string)
            res = self.style.SUCCESS('Successfully "%s"' % options['user'])
            self.stdout.write(res)
        if 'type' in options and options['type'] == "pages":
            if user is not None:
                url = "https://graph.facebook.com/v2.7/me/likes?access_token="
                url += token
                pages = []
                while url is not None:
                    r = requests.get(url)
                    data = r.json()
                    pages += data['data']
                    if 'paging' in data and 'next' in data['paging']:
                        url = data['paging']['next']
                    else:
                        url = None
                data['data'] = pages
                pprint.pprint(len(data['data']))
                url = "https://graph.facebook.com/v2.7/me/?access_token="
                url += token
                profile = requests.get(url).json()
                self.createfileprofile(data, profile )
                pprint.pprint(requests.get(url).json())

    def createfileprofile(self, likes, profile):
        namefile = profile["id"]
        namefile += "_likes_"  # api
        # ISO 8601
        namefile += strftime("%Y-%m-%dT%H:%M:%S%z", gmtime())
        namefile += ".json"
        data = json.dumps(likes, indent=4)
        f = open(namefile, 'w')
        f.write(data)
        f.close()
        # putfile(namefile)
        with open(namefile) as data_file:
            data = json.load(data_file)
            likes = data
