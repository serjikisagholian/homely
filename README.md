## Homely's README

### run server
]$ python manage.py runserver
### browse
```
http://127.0.0.1:8000/admin
Username: admin
Password: admin@123
```
### StartUp
```
$ cd homely  # project directory
$ pip install -r requirements.txt
$ python manage.py makemigrations rentals  // already included
$ python manage.py migrate                 // already done
```

### Commands
- Delete all data in database
```
$ python manage.py clearalldata
```
- Create Fakes records in count of specified number
```
python manage.py createfakedata count
```
- Example
```
$ python manage.py createfakedata 25
```

### Authentication
- I have created user/password combination as password==user for convenience
- Users cellphone are restricted to (818)xxx-xxxx as a sample vaildation

### Get Token
- Before this get a fake created user
```
$ python manage.py shell
>>> from rentals.models import UserProfile
>>> u = UserProfile.objects.first()
>>> u.username
```
- or you can browse http://127.0.0.1:8000 to get list of users
- if you want to login in admin panel
```
>>> u.is_staff = True
>>> u.is_superuser = True
>>> u.save()
```
### run server
```
$ python manage.py runserver
```
- Now login with username & password

(same as username -- fake creator used equivalent string for convenience)

- Don't forget the trailing slash in Url
```
$ curl -X POST -H "Content-Type: application/json"
-d '{"username":"youruser","password":"yourpassword"}' http://127.0.0.1:8000/api-token-auth/
```
- Access Protected urls
```
$ curl -H "Authorization: JWT <your_token>" http://127.0.0.1:8000/protected-url/
```

### Endpoints
- Get list of users without Authentication (good for hackers)
- This is an security exploit, I leave this to find users and explore the app
```
$ curl http://127.0.0.1:8000/rentals/homeowners/
$ curl http://127.0.0.1:8000/rentals/renters/
```
- Get list of all properties (This is just to compare results with actual search with comes next)
```
$ curl -H  "Authorization: JWT <your_token>" http://127.0.0.1:8000/rentals/properties/
```
- Add new Property
```
$ curl  -X POST -H  "Content-Type: application/json" -H  "Authorization: JWT <your_token>"
-d '{"homeowner": <homeowner.id>, "address":"address-text","baths":<count>,"rooms":<count>,"furnished":<0|1>}'
 http://127.0.0.1:8000/rentals/properties/
```
- Edit Property
```
$ curl  -X PATCH -H  "Content-Type: application/json" -H  "Authorization: JWT <your_token>"
-d '{"homeowner": <homeowner.id>, "address":"address-text","baths":<count>,"rooms":<count>,"furnished":<0|1>}'
 http://127.0.0.1:8000/rentals/properties/<id>/
```
- Delete Property
``` 
$ curl  -X DELETE -H  "Authorization: JWT <your_token>" http://127.0.0.1:8000/rentals/properties/<id>/
```

- Create, Edit, Delete the same way can be applied on Homeowner and Renter
- I excluded permission for Homeowner and Renter due to easy run of sample application

- Get list of properties available from start to end
```
$ curl -H  "Authorization: JWT <your_token>" http://127.0.0.1:8000/rentals/properties/?start=<yyyymmdd>&end=<yyyymmdd>
$ curl -H  "Authorization: JWT <your_token>" http://127.0.0.1:8000/rentals/properties/?start=20180110&end=20180111
```

-  Get only one Property, consider leading slash /
```
$ curl -H  "Authorization: JWT <your_token>" http://127.0.0.1:8000/rentals/properties/<pk>/
```
- Make a reservation
```
$ curl -X POST -H  "Content-Type: application/json" -H  "Authorization: JWT <your_token>"
-d '{"property": <property.id>, "renter":<renter.id>,"start_date": "<yyyy-mm-dd>", "end_date":"<yyyy-mm-dd>"}'
http://127.0.0.1:8000/rentals/reserves/
```

- Example
```
curl -X POST -H  "Content-Type: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTU2NjM0MTIsImVtYWlsIjoiem9lb3J0aXpAZ21haWwuY29tIiwidXNlcl9pZCI6NTIsInVzZXJuYW1lIjoiY2FsZWJtY2tpbm5leSJ9.X71-JaubFaiaetQBhqoBe7eqEOjLj2v_UChdeCC92MU" -d '{"property": 33, "renter": 75,"start_date": "2018-03-01", "end_date":"2018-03-02"}' http://127.0.0.1:8000/rentals/reserves/
```
- Change reservation (Only bring fileds that should be changed)
```
$ curl -X POST -H  "Content-Type: application/json" -H  "Authorization: JWT <your_token>"
-d '{"property": <property.id>, "renter":<renter.id>,"start_date": "<yyyy-mm-dd>", "end_date":"<yyyy-mm-dd>"}'
http://127.0.0.1:8000/rentals/reserves/<id>
```
- Example
```
curl -X PATCH -H "Content-Type: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTU2NjM0MTIsImVtYWlsIjoiem9lb3J0aXpAZ21haWwuY29tIiwidXNlcl9pZCI6NTIsInVzZXJuYW1lIjoiY2FsZWJtY2tpbm5leSJ9.X71-JaubFaiaetQBhqoBe7eqEOjLj2v_UChdeCC92MU" -d '{"property": 33, "renter": 75,"start_date": "2018-05-01", "end_date":"2018-05-02"}' http://127.0.0.1:8000/rentals/reserves/6/
```

- Instead of curl, chrome app postman, or httpie can be used
- djangoresetframework also got browse-able API

- Create Dump data for test
```
$ python manage.py dumpdata -e contenttypes -e sessions -e admin -e auth.Permission > rentals/fixtures/homely_test.json
```
