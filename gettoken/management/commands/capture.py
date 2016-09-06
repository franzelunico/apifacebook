# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gettoken.models import User, Snapshot
from time import gmtime, strftime
from fabric.operations import local
import json
import pprint
import requests
import datetime


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
        boolean_q = options['type'] == "pages"
        boolean_q = boolean_q or options['type'] == "contacts"
        boolean_q = boolean_q and 'type' in options and user is not None
        if boolean_q:
            query_type = options['type']
            url_api = "" + "https://graph.facebook.com/v2.7/me/"
            if options['type'] == "pages":
                url_api += "likes"
            if options['type'] == "contacts":
                url_api += "friends"
            url = url_api + "?access_token="
            url += token
            pages = []
            while url is not None:
                r = requests.get(url)
                data = r.json()
                if 'data' in data:
                    pages += data['data']
                    if 'paging' in data and 'next' in data['paging']:
                        url = data['paging']['next']
                    else:
                        url = None
                else:
                    url = None
            url = "https://graph.facebook.com/v2.7/me/?access_token="
            url += token
            profile = requests.get(url).json()
            self.createfileprofile(data, profile, url_api, query_type)
            pprint.pprint(requests.get(url).json())

    def createfileprofile(self, likes, profile, url_api, query_type):
        filename = query_type + "-" + profile["id"] + "@"
        # ISO 8601
        format_date = "%Y-%m-%dT%H:%M:%S"
        format_date_utc = format_date + "%z"
        created_at = strftime(format_date_utc, gmtime())
        filename += created_at
        filename += ".json"
        data = json.dumps(likes, indent=4)
        f = open(filename, 'w')
        f.write(data)
        f.close()
        # self.pushfile(filename)
        with open(filename) as data_file:
            data = json.load(data_file)
            likes = data
        created_at = datetime.datetime.utcnow()
        snapshot = Snapshot(query_url=url_api, filename=filename,
                            query_type=query_type, created_at=created_at)
        snapshot.save()

    def pushfile(self, filename):
        command = "aws s3 cp " + filename + " s3://usersfacebook/"
        local(command)
