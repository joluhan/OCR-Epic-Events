
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

  \env\Scripts\activate.bat  #Windows
```
Install project dependencies and packages
```bash
  pip install -r requirements.txt
```

## Environment Variables
Generate a secret key that is unique for this deployment of the Django app by runnig this command in your terminal
```bash
  python -c 'from django.core.management.utils import  get_random_secret_key; print(get_random_secret_key())'
```
Create a file named `.env` in the project's root director. Copy the generated secret key and add to your `.env` file as `SECRET_KEY = <YOUR_GENERATED_KEY>`.

Generate a another random secret key to be used by JWT for user authentication.
```bash
  python -c 'from django.core.management.utils import  get_random_secret_key; print(get_random_secret_key())'
```
Copy the generated secret key and add to your `.env` file as `TOKEN_KEY = <YOUR_GENERATED_KEY>`.

Finally, add the DSN for Sentry error logging to `.env` file as `SENTRY_DSN = <Sentry DSN>`. You’ll need the DSN (Data Source Name) from your Sentry project, which you can find in your Sentry project settings under "Client Keys (DSN)" after you sign in at https://sentry.io/welcome/.


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



### Coverage

Follow these steps to install Coverage.py and configure it for your Django project:

1. **Install Coverage.py**

   Open your terminal and run the following command to install Coverage.py:

   ```bash
   pip install coverage

2. **Configure Coverage.py**

   Create a file named `.coveragerc` in your project directory to specify Coverage.py settings:

   ```plaintext
   [run]
   source = .
   omit =
       */migrations/*
       manage.py
   ```

   - `source`: This setting includes all directories under the current directory for coverage reporting.
   - `omit`: This setting excludes files or directories that you do not want to include in the coverage report, such as migrations and `manage.py`.

## Running the Tests

### Using Django's manage.py

Django's `manage.py` script provides a convenient way to interact with your Django project. To run your tests without coverage, simply execute:

```bash
python manage.py test
```

### With Coverage

To run your tests with coverage, use the following commands:

```bash
coverage run -m pytest
```

This command will start the Django test suite under the coverage monitor.

## Generating Coverage Reports

After running the tests, you can generate coverage reports in two formats:

- **Command-line Report:**

  Generate a simple coverage report in your terminal:

  ```bash
  coverage report
  ```

- **HTML Report:**

  Generate a detailed HTML coverage report:

  ```bash
  coverage html
  ```

  This command generates an HTML report that you can view in a browser to see a detailed breakdown of coverage by file.

## Viewing the HTML Report

After generating the HTML report, you can find it in the `htmlcov` directory at the root of your project. Open the `index.html` file in a web browser to view the coverage report.
