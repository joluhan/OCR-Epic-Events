
# Epic Events - CRM

Customer Relationship Management (CRM) software that organizes events (parties, professional meetings,
off-site events) for its clients while facilitating communication between the different divisions of the
company.




## Installation
To begin, clone the rpository by running the following command in your terminal
Install my-project with npm

```bash
  git clone https://github.com/hire-blac/EpicEventsCRM.git
```
Navigate into the project directory, create a virtual environment and activate it with the following commands
```bash
  python -m venv .venv
  source .venv/bin/activate   #Linux/MacOS

  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
  .\env\Scripts\activate or \env\Scripts\activate.bat  #Windows
```
Install project dependencies and packages
```bash
  pip install -r requirements.txt
```

## Create Superuser
To create new users, apply migrations to initialize the database by running the following command:

```bash
  python manage.py migrate
```
Then create a new superuser with the following command

```bash
  python manage.py createsuperuser
```
Once the superuser is created, you can use it to log into the application admin backend.

Start up the server and log in to the admin backend with the the command

```bash
  python manage.py runserver
```
Go to http://127.0.0.1:8000/admin/ in your browser and log in with the superuser information you just created.

With superuser, you will be able to manage all aspects of the application, including creating, modifying and deleting users, customers, contracts, and events.

In order to use the command line application, all you have to do is create a user with management role.

## Commands
To get help with a command use the following: 

```bash
  python manage.py <command> --help
```

### User Commands
To login:

```bash
  python manage.py login
```
To logout:

```bash
  python manage.py logout
```
To create a new user:

```bash
  python manage.py create_new_user
```
To view all or a single user:

```bash
  python manage.py read_users <optional: user_id>
```
To update a user info:

```bash
  python manage.py update_user <user_id> --[field name] [new value]
```
To delete a user:

```bash
  python manage.py delete_user <user_id>
```


### Client Commands

To create a new client:

```bash
  python manage.py create_client
```
To view all or a single client:

```bash
  python manage.py read_clients <optional: client_id>
```
To update a client info:

```bash
  python manage.py update_client <client_id> --[field name] [new value]
```
To delete a client:

```bash
  python manage.py delete_client <client_id>
```


### Contract Commands

To create a new contract:

```bash
  python manage.py create_contract
```
To view all or a single contract:

```bash
  python manage.py read_contracts <optional: contract_id>
```
To update a contract info:

```bash
  python manage.py update_contract <contract_id> --[field name] [new value]
```
To delete a contract:

```bash
  python manage.py delete_contract <contract_id>
```


### Event Commands

To create a new event:

```bash
  python manage.py create_event
```
To view all or a single event:

```bash
  python manage.py read_events <optional: event_id>
```
To update a event info:

```bash
  python manage.py update_event <event_id> --[field name] [new value]
```
To delete a event:

```bash
  python manage.py delete_event <event_id>
```