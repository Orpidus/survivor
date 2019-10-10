# Survivor


## Components

### Users

Optional entries are parenthesized

* Register
    * URL: /user[/survivor, /advocate]
    * Method: post
    * Body: {"username": string, "email": string, "password": string, "user_token": string, ("device_token": string)}
    * Response: {"username": string, "email": string, "user_token": string, "device_token": string}

* View
    * URL: /user/${user_id}
    * Method: get
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Response: {"username": string, "email": string, "user_token": string, "device_token": string}

* Update
    * URL: /user/${user_id}
    * Method: put
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {("username": string), ("email": string), ("password": string), ("user_token": string), ("device_token": string)}
    * Response: {"username": string, "email": string, "user_token": string, "device_token": string}

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
    
### Connection

* Request
    * URL: /connection/request
    * Method: post
    * Header: {"Authorization": "Bearer ${access_token}"}
    
* Accept
    * URL: /connection/accept
    * Method: post
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {"survivor_id": string}
    * Response: Success: 200, Failure: 204

* View
    * URL: /connection
    * Method: get
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Response: [{"survivor": string, "advocate": string}]
    
### Chat

* Send
    * URL: /chat/send
    * Method: post
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {"receiver": string, "message": string}
    
* History
    * URL: /chat/${user_id}
    * Method: get
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Response: [{"time": string, "sender_id": string, "receiver_id": string, "message": string}] ordered by "time"
    
 ### Tasks

* Assign
    * URL: /task/${survivor_id}
    * Method: post
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {"details": string}    
    * Response: {"id": integer, "survivor": string, "advocate": string, "details": string, "status": string}

* View
    * URL: /task/${survivor_id}
    * Method: get
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Response: [{"id": integer, "survivor": string, "advocate": string, "details": string, "status": string}]

* Update
    * URL: /task/${user_id}
    * Method: put
    * Header: {"Authorization": "Bearer ${access_token}"}
    * Body: {"task_id": integer, "status": string}
    * Response: {"id": integer, "survivor": string, "advocate": string, "details": string, "status": string}
