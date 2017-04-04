# Skeleton Service

Flask Microservice Skeleton

## How to start

### GitHub Project

To start a new project, we are going to create a new project and pull the skeleton code inside it.

* [Create a new GitHub repository](https://help.github.com/articles/creating-a-new-repository/) (eg: git@github.com:uBiome/uBiome-NEW-SERVICE.git)
* Clone the new repository locally
```
	> git clone git@github.com:uBiome/ubiome-NEW-SERVICE.git --recursive
	> cd uBiome-NEW-SERVICE
```
* Add Skeleton remote location
```
	> git remote add skeleton git@github.com:uBiome/uBiome-flask-skeleton.git
```
* Pull data from Skeleton branch (eg. from master)
```
    > git pull skeleton master
```
* Update submodule for a secure environment configuration
```
    > git submodule update --init --recursive
    > cd private/setup/common/security
    > git checkout master
```

### Local Project
* Create a new Git project
```
    > mkdir uBiome-NEW-SERVICE
    > cd uBiome-NEW-SERVICE
    > git init
```
* Create a remote location to Skeleton project
```
    > git remote add skeleton git@github.com:uBiome/uBiome-flask-skeleton.git
```
* Pull data from Skeleton branch (eg. from master)
```
    > git pull skeleton master
```
* Update submodule for a secure environment configuration
```
    > git submodule update --init --recursive
    > cd private/setup/common/security
    > git checkout master
```

## Renaming - IMPORTANT !!!

Every single file, specialy under /private directory, must be checked and the project name must
replace the current place holder: _uBiome-flask-skeleton-service_

## Lets go !!

### SetUp Tools & Environment
```
    > ./private/setup/development/setup.sh
```
### Run service

```
    > ./private/setup/development/execute.sh
```

## Add Environment Configuration

All environment setting must be done in env folder's file. _But_ those files are encrypted so,
[this project](https://github.com/uBiome/ubiome-security) provides tools to do the task a bit easier.

Please read carefully the readme, but for start now just run the next command for edit all env's files in one shot:
```
    > ./private/setup/common/security/local/utils/edit_properties.sh
```

## Trouble Shooting

* If you're using [conda](http://conda.pydata.org/docs/) is possible you have some [problems](https://github.com/uBiome/uBiome-flask-skeleton/issues/9) related to `pip`/`virtualenv`, to fix this you could [downgrade python version](https://github.com/conda/conda/issues/1367#issue-86590167), and execute:

```
sudo easy_install pip
sudo pip install virtualenv
```

__Note:__ Remember to remove ve/venv folders before running setup command.
