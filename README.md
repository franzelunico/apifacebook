### Only Docker:
Uncomment lines configs/sites-enabled/fl.code.bo.conf
```sh
$ docker-compose build
$ docker-compose up
```

### Another way (without Docker):
In /etc/hosts include
127.0.0.1   local.fl.code.bo

### Nginx
In nginx.conf include configs/sites-enabled/fl.code.bo.conf

### Packages and Libraries
```sh
$ pip install -r requirements.txt
$ bower install
$ npm install
```

### Init and Reset
```sh
$ sh script_reload.sh
```

### Deployment:
The browser refresh any change in frontend or backend synchronized with nginx
```sh
$ gulp serve
$ python manage.py runserver 127.0.0.1:8001
```

### Run Test with Django:
Create the directory fixtures 
```sh
$ python manage.py dumpdata gettoken --indent 4 > gettoken/fixtures/data.json
$ python manage.py test gettoken.tests.SimpleTest
```
