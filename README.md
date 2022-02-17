# Hard Drive Tracker System
LETS EAT

## Contributions

Never push to the main. Always create pull requests. 

### Before Working

* Make sure your repo is synced.
* Make sure you create a new branch.
* Run the commands:
```
pip install requirements
```

### During Work tips 
* Commit often. If you mess something up you can revert to the previous commit using the command. <B>This can also work if you accidently work on the main rather than a seperate branch</b>.
```
git reset --hard head
```  

### After Work

* Once all your commits are in place, its best practice to go to the <B>main branch</b> and pull an new changes. Then merge these changes with your <b>working branch</b>. 
* Once all merge conflicts are resolved, and you're completely synced with <b>main repo</b> you can run the command(make sure you are in the top level directory):
```
 pip freeze > requirements
 ```