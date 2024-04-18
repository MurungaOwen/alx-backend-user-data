# Simple API

Simple HTTP API for playing with `User` model.


## Files

### `models/`

- `base.py`: base of all models of the API - handle serialization to file
- `user.py`: user model

### `api/v1`

- `app.py`: entry point of the API
- `views/index.py`: basic endpoints of the API: `/status` and `/stats`
- `views/users.py`: all users endpoints


## Setup

```
$ pip3 install -r requirements.txt
```


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
```


## Routes

- `GET /api/v1/status`: returns the status of the API
- `GET /api/v1/stats`: returns some stats of the API
- `GET /api/v1/users`: returns the list of users
- `GET /api/v1/users/:id`: returns an user based on the ID
- `DELETE /api/v1/users/:id`: deletes an user based on the ID
- `POST /api/v1/users`: creates a new user (JSON parameters: `email`, `password`, `last_name` (optional) and `first_name` (optional))
- `PUT /api/v1/users/:id`: updates an user based on the ID (JSON parameters: `last_name` and `first_name`)

### alx tasks

#### setup
setup: Download and start your project from this archive.zip
In this archive, you will find a simple API with one model: User. Storage of these users is done via a serialization/deserialization in files.

#### 1
What the HTTP status code for a request unauthorized? 401 of course!

Edit api/v1/app.py:

Add a new error handler for this status code, the response must be:
a ```JSON: {"error": "Unauthorized"}```
status code 401
you must use jsonify from Flask
For testing this new error handler, add a new endpoint in api/v1/views/index.py:
```Route: GET /api/v1/unauthorized```
This endpoint must raise a 401 error by using abort - Custom Error Pages
By calling abort(401), the error handler for 401 will be executed.

#### 2
Error handler: Forbidden
What the HTTP status code for a request where the user is authenticate but not allowed to access to a resource? 403 of course!
```Edit api/v1/app.py:```
Add a new error handler for this status code, the response must be:
a ```JSON: {"error": "Forbidden"}```
status code 403
you must use jsonify from Flask
For testing this new error handler, add a new endpoint in api/v1/views/index.py:
```Route: GET /api/v1/forbidden```
This endpoint must raise a 403 error by using abort - Custom Error Pages
By calling abort(403), the error handler for 403 will be executed

#### 3
3. Auth class
mandatory
Now you will create a class to manage the API authentication.
Create a folder ```api/v1/auth```
Create an empty file ```api/v1/auth/__init__.py```
Create the class Auth:
in the file ```api/v1/auth/auth.py```
import request from flask
class name Auth
public method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: that returns False - path and excluded_paths will be used later, now, you don’t need to take care of them
public method def authorization_header(self, request=None) -> str: that returns None - request will be the Flask request object
public method def current_user(self, request=None) -> TypeVar('User'): that returns None - request will be the Flask request object

### 4
Define which routes don't need authentication
mandatory
Update the method def require_auth(self, path: str, excluded_paths: List[str]) -> bool: in Auth that returns True if the path is not in the list of strings excluded_paths:
```
Returns True if path is None
Returns True if excluded_paths is None or empty
Returns False if path is in excluded_paths
You can assume excluded_paths contains string path always ending by a /
This method must be slash tolerant: path=/api/v1/status and path=/api/v1/status/ must be returned False if excluded_paths contains /api/v1/status/
```

#### 5
Request validation!
mandatory
Now you will validate all requests to secure the API:

Update the method def authorization_header(self, request=None) -> str: in api/v1/auth/auth.py:

If request is None, returns None
If request doesn’t contain the header key Authorization, returns None
Otherwise, return the value of the header request Authorization
Update the file api/v1/app.py:

Create a variable auth initialized to None after the CORS definition
Based on the environment variable AUTH_TYPE, load and assign the right instance of authentication to auth
if auth:
import Auth from api.v1.auth.auth
create an instance of Auth and assign it to the variable auth
Now the biggest piece is the filtering of each request. For that you will use the Flask method before_request

Add a method in api/v1/app.py to handler before_request
if auth is None, do nothing
if request.path is not part of this list ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'], do nothing - you must use the method require_auth from the auth instance
if auth.authorization_header(request) returns None, raise the error 401 - you must use abort
if auth.current_user(request) returns None, raise the error 403 - you must use abort
In the first terminal:

```hood@DESKTOP-OACK3HP:~$ API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=auth python3 -m api.v1.app```
```
In a second terminal:

bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status/"
{
  "status": "OK"
}
bob@dylan:~$ 
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users"
{
  "error": "Unauthorized"
}
bob@dylan:~$
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/users" -H "Authorization: Test"
{
  "error": "Forbidden"
}
bob@dylan:~$
```

#### 6
Basic auth
mandatory
Create a class BasicAuth that inherits from Auth. For the moment this class will be empty.
Update api/v1/app.py for using BasicAuth class instead of Auth depending of the value of the environment variable AUTH_TYPE, If AUTH_TYPE is equal to basic_auth:
import BasicAuth from api.v1.auth.basic_auth
create an instance of BasicAuth and assign it to the variable auth
Otherwise, keep the previous mechanism with auth an instance of Auth.

#### 7
Basic - Base64 part
mandatory
Add the method def extract_base64_authorization_header(self, authorization_header: str) -> str: in the class BasicAuth that returns the Base64 part of the Authorization header for a Basic Authentication:
Return None if authorization_header is None
Return None if authorization_header is not a string
Return None if authorization_header doesn’t start by Basic (with a space at the end)
Otherwise, return the value after Basic (after the space)
You can assume authorization_header contains only one Basic

#### 8
Basic - Base64 decode
mandatory
Add the method def decode_base64_authorization_header(self, base64_authorization_header: str) -> str: in the class BasicAuth that returns the decoded value of a Base64 string base64_authorization_header:
```
Return None if base64_authorization_header is None
Return None if base64_authorization_header is not a string
Return None if base64_authorization_header is not a valid Base64 - you can use try/except
Otherwise, return the decoded value as UTF8 string - you can use decode('utf-8')
```
#### 9
Basic - User credentials
mandatory
Add the method ```def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str)```in the class BasicAuth that returns the user email and password from the Base64 decoded value.
This method must return 2 values
```
Return None, None if decoded_base64_authorization_header is None
Return None, None if decoded_base64_authorization_header is not a string
Return None, None if decoded_base64_authorization_header doesn’t contain :
```
Otherwise, return the user email and the user password - these 2 values must be separated by a :
You can assume decoded_base64_authorization_header will contain only one :

#### 10
Basic - User object
mandatory
Add the method ```def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User')```: in the class BasicAuth that returns the User instance based on his email and password.

```
Return None if user_email is None or not a string
Return None if user_pwd is None or not a string
Return None if your database (file) doesn’t contain any User instance with email equal to user_email - you should use the class method search of the User to lookup the list of users based on their email. Don’t forget to test all cases: “what if there is no user in DB?”, etc.
Return None if user_pwd is not the password of the User instance found - you must use the method is_valid_password of User
Otherwise, return the User instance
```
#### 11
Basic - Overload current_user - and BOOM!
Now, you have all pieces for having a complete Basic authentication.
Add the method def current_user(self, request=None) -> TypeVar('User') in the class BasicAuth that overloads Auth and retrieves the User instance for a request:

You must use authorization_header
You must use extract_base64_authorization_header
You must use decode_base64_authorization_header
You must use extract_user_credentials
You must use user_object_from_credentials
With this update, now your API is fully protected by a Basic Authentication. Enjoy!

#### 12
Basic - Allow password with ":"
#advanced
Improve the method def extract_user_credentials(self, decoded_base64_authorization_header) to allow password with :.

#### 13
Require auth with stars
advanced
Improve def require_auth(self, path, excluded_paths) by allowing * at the end of excluded paths.
Example for excluded_paths = ["/api/v1/stat*"]:
/api/v1/users will return True
/api/v1/status will return False
/api/v1/stats will return False