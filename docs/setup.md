### Project Setup

1. Clone the project from GitHub  
```
    git clone @coherent.github.com
```
2. Install and setup MySQL database locally  
Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql/).  
You may optionally also download [Workbench](https://dev.mysql.com/downloads/workbench/) to visualise the database.  
During installation, it will ask you for a `root` password - don't use this user in your apps.  
Instead, create a user with the admin permissions. Remember the username and password for later.

4. Set up `virtualenv`  
`virtualenv` provides Python package isolation.  
This is critical when running multiple projects which may need different versions of the same library.  
Also is useful for testing new packages, eg to see if a newer version of Django works with your app.  
```commandline
    virtualenv --python3=python3.exe ~/virtualenv/env_dj_testing
    source ~/virtualenv/env_dj_testing/Scripts/activate
```

Use `which python` to show which Python your virtualenv is running.  
Use `deactivate` to disable the virtualenv.  
Install the packages from `requirements.txt` into your virtual environment.  

5. Set up Django to communicate with your database
Refer to the [docs](https://docs.djangoproject.com/en/1.11/ref/databases/#connecting-to-the-database) on how to connect.  
Create an admin user to ensure it worked
