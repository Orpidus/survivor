# Survivor


## Components

### Users

Optional entries are parenthesized

* Register
    * URL: /user[/survivor, /advocate]
    * Method: post
    * Body: {"username": string, "email": string, "password": string, ("device_token": string)}
    * Response: {"id": integer, "username": string, "email": string, "device_token": string}

* View
    * URL: /user/${user_id}
    * Method: get
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Response: {"id": integer, "username": string, "email": string, "device_token": string}

* Update
    * URL: /user/${user_id}
    * Method: put
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {("username": string), ("email": string), ("password": string), ("device_token": string)}
    * Response: {"id": integer, "username": string, "email": string, "device_token": string}

* Delete
    * URL: /user/${user_id}
    * Method: delete
    * Header: {"Authorization": "Bearer ${access_token}"}

### Tokens

* Generate
    * URL: /token
    * Method: post
    * Body: {"username": string, "password": string}
    * Response: {"refresh": string, "access": string}

* Refresh
    * URL: /token/refresh
    * Method: post
    * Body: {"refresh": ${refresh_token}}
    * Response: {"access": string}
