# Job Application Portal

**By:** Daksh Gupta

**Language:** Python 3.5

**Database:** PostgreSQL

**Web framework:** Pyramid

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
2. Databse name
3. Port
4. Username
5. Password

**Note:** All this information is necessary in order to make a connection with the database.

Here is an example `config` file:

```
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