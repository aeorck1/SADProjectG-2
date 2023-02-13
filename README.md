# Time-Table Management System CSC 302 Project (Backend)

## Available Endpoints

> ### User Management
| Endpoint      | Method    | Description   |
| :---------     | :---------: | :------        |
| ***api/user/create*** | _POST_ | To create a regular user account|
| ***api/user/createmanager***  | _POST_ | To create a manager account (i.e account for the resource management officer) |
|***api/user/authenticate*** | _POST_ | To authenticate a user to access private endpoints. It responds with an authetication token
|***api/user/me***| _GET_ | To update user data (authentication is required) |

>#### User Data Fields
| Field | Comment |
| --- | --- |
| _email_ | The primary user identification field. Required for user creation and authentication |
| *password* | User password. Required for user creation and authentication |
| *name* | The full name of the user. Not required at registration, can be updated |
| _department_ | The department of the user



***

> ### Resource Allocation Endpoints
raise NotImplemented("Endpoints are yet to be implemented. TBDone soon. Na algorithm we dey look for ooo")



