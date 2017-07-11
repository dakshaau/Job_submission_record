# Job Application Portal

**By:** Daksh Gupta

**Language:** Python 3.5

**Database:** PostgreSQL

**Web framework:** Pyramid

## Introduction:

This is a python web application which can be used by job applicants to keep a track of their job applications. The portal allows you to:

- Add an application to the job database
- Search for already applied job by, *company name*, *position name*, and/or *position_id*.
- Update status of any job in the search results

#### Screen Shots:

- [Page to add a record]('screens/Add record.png')
- [Search page]('screens/search page.png')
- [Search Results]('screens/search results.png')
- [Display application details]('screens/job details.png')
- [Update status]('screens/update_1.png')
- [Update success]('screens/update_2.png')

## Requirements:
1. pyramid
2. pyramid_jinja2
3. psycopg2
	- This requires PostgreSQL to be installed and operational before installation
4. sqlalchemy
	- This is an ORM which is used to make life easier when using Databases specially SQL

## Running Instructions:

To run this web application, you need to first have a database ready in PostgreSQL. It can be created using Postgres Enterprise Manager or using the shell.

Once the databse has been created, a file with the name `config` should be placed with the main python files. This file contains the connection information for the database. Each line should be a valid string containing only the relavent information. Below are the order of information:

1. Host or IP address
2. Database name
3. Port
4. Username
5. Password

**Note:** All this information is necessary in order to make a connection with the database.

Here is an example `config` file:

```text
localhost
trial_database
5432
postgres
password
```

The IP address and port on which the server runs are hardcoded into `main.py`. The server runs at `127.0.0.1:6543`. You can change that in `line 158` of [main.py]('main.py').

To finally run the server, run the command:

```shell
python main.py
```

**NOTE:** Close the server using `CTRL+C` to safely close the connection with the database.