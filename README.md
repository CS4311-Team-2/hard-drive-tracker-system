# Hard Drive Tracker System
LETS EAT

## Contributions

Never push to the main. Always create pull requests. 

### Before Working

* Make sure your repo is synced.
* Make sure you create a new branch.
* Run the commands:
```
pip install -r requirements.txt
```

### During Work tips 
* Commit often. If you mess something up you can revert to the previous commit using the command. <B>This can also work if you accidently work on the main rather than a seperate branch</b>.
```
git reset --hard head
```  


* Keep your branch updated, if you are working in your branch and notice that the main is getting ahead to add the main additions to your branch
```
git fetch
git merge origin/master
```  

### After Work

* Once all your commits are in place, its best practice to go to the <B>main branch</b> and pull any new changes. Then merge these changes with your <b>working branch</b>. 
* Once all merge conflicts are resolved, and you're completely synced with <b>main repo</b> you can run the command(make sure you are in the top level directory):
```
pip freeze > requirements.txt
```

## Database

### Prepare Database

* Use this command to prepare the database with the default data, this will delete everything on the database and updload the csv files into the database using both the makemigrations and migrate commands.
```
python manage.py resetdatabase
```

* This command will make a new migration file to update the database if the models in the model table had been modified. 
```
python manage.py makemigrations
```

* This command will make a update your local SQLite database with the migration files
```
python manage.py migrate
```

### Populate Database

* Run the following to command to load the data into the database so far only 3 hard drives are added from the hard_drive.csv file but adding more rows will add more hard drives to the system and to users
```
python manage.py updatemodels
```

* Once this command runs successfully two users would be created Maintainer and Requestor with their usernames and roles being the same. Use these to sign in with the password 'pass' and you should be able to see their respected pages

### Create users
* Run this command to create an admin user in your database and have access to all the model data at once in your computer.
```
python manage.py createsuperuser
```