# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from gettoken.models import User, Snapshot
from time import gmtime, strftime
import json
import requests
import datetime
import boto3
import os


"""
python manage.py capture --type=pages --user=<user_id>
python manage.py capture --type=contacts --user=<user_id>
"""


class Command(BaseCommand):
    help = 'Ingrese el id del usuario'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--user', type=str, help='User ID o name',
                            required=True)
        parser.add_argument('-t', '--type', type=str, help='Type ',
                            required=True)
        parser.add_argument('-o', '--token', type=str, help='Type ',
                            required=False)
        parser.add_argument('--print', action='store_true', dest='print',
                            default=False,
                            help='Show all information user',)

    def handle(self, *args, **options):
        user = self.getUser(args, options)
        token = self.getToken(user, args, options)
        url_api = "https://graph.facebook.com/v2.7/me/"
        url_api += self.getType(args, options)
        url_api += "access_token=" + token
        url = url_api
        data = None
        pages = []
        while url is not None:
            data = requests.get(url).json()
            if 'data' in data:
                pages += data['data']
                if 'paging' in data and 'next' in data['paging']:
                    url = data['paging']['next']
                else:
                    url = None
            else:
                url = None
        data['data'] = pages
        url = "https://graph.facebook.com/v2.7/me/?access_token=" + token
        profile = requests.get(url).json()
        data = self.createfile(data, profile, options['type'])
        if 'print' in options and options['print']:
            parsed = json.loads(data)
            print json.dumps(parsed, indent=4, sort_keys=True)

    def getToken(self, user,  args, options):
        token = ""
        if options['token'] is not None:
            token = options['token']
        else:
            token = user.fb_token.token
        return token

    # Falta Token Expirado
    def getUser(self, args, options):
        user = None
        if 'user' in options:
            try:
                if User.objects.filter(fb_name=options['user']).exists():
                    user = User.objects.get(fb_name=options['user'])
                else:
                    if User.objects.filter(fb_id=options['user']).exists():
                        user = User.objects.get(fb_id=options['user'])
                    else:
                        user = User.objects.get(fb_id=options['user'])
            except User.DoesNotExist:
                string = 'User "%s" does not exist' % options['user']
                user = None
                raise CommandError(string)
            res = self.style.SUCCESS('Successfully "%s"' % options['user'])
            self.stdout.write(res)
        return user

    def getType(self, args, options):
        url_api = ""
        if options['type'] == "pages":
            url_api += "likes?"
        else:
            if options['type'] == "contacts":
                url_api += "friends?"
                url_api += "fields=id,first_name,last_name,email,birthday,"
                url_api += "education,gender,locale,location,hometown&"
            else:
                string = 'type "%s" does not exist' % options['user']
                raise CommandError(string)
        return url_api

    def createfile(self, likes, profile, query_type):
        if 'id' in profile:
            filename = query_type + "-" + profile["id"] + "@"
            # ISO 8601
            format_date = "%Y-%m-%dT%H:%M:%S"
            format_date_utc = format_date + "%z"
            created_at = strftime(format_date_utc, gmtime())
            filename += created_at
            filename += ".json"

            if not os.path.exists(os.getcwd()+"/"+query_type+"/"):
                os.makedirs(os.getcwd()+"/"+query_type+"/")
            os.chdir(os.getcwd()+"/"+query_type+"/")

            data = json.dumps(likes, indent=4)
            f = open(filename, 'w')
            f.write(data)
            f.close()

            created_at = datetime.datetime.utcnow()
            snapshot = Snapshot(filename=filename, query_type=query_type,
                                created_at=created_at)
            snapshot.save()
            self.pushfile(snapshot)
            return data
        else:
            string = 'Error update token'
            raise CommandError(string)

    def pushfile(self, snapshot):
        filename = snapshot.filename
        path = snapshot.query_type + '/' + snapshot.filename
        data = open(filename, 'r')
        s3 = boto3.resource('s3')
        s3.Bucket('usersfacebook').put_object(Key=path, Body=data)
        data.close()
        os.remove(filename)
