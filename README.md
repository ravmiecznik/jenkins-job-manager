# Jenkins Job Manager

## This presentation will show how to create basic Jenkins setup with use of *freestyle* and *pipeline* jobs. It will also demonstrate how to use exising Python tools and modules to make Jenkins management simpler. You will learn how to create, delete and reconfigure jobs. It will also highlight another Jenkins related features. I will demonstrate low level features of Python which can be useful in many different applications.
<br>

## Here are topic covered in this demo:
## [Jenkins setup](##Jenkins-setup)
* [Jenkins documentation](#Jenkins-documentation)
* [Jenkins controllers and agents](#More-detailed-information-on-Jenkins-controllers)
* [Jenkins installation](#instructions-how-to-install-jenkins-can-be-found-here-httpswwwjenkinsiodocbookinstalling)
* [Running jenkins in docker](#this-tutorial-will-be-based-on-jenkins-on-decker-and-it-will-slightly-differ-from-the-examples-mentioned-in-referred-links-the-point-of-this-tutorial-is-to-show-how-to-create-a-basic-setup-and-manage-it-with-python)

## Jenkins setup

* #### Jenkins documentation: https://www.jenkins.io/doc/ <br>
* #### More detailed information on Jenkins controllers and agents: https://www.jenkins.io/doc/book/managing/nodes/ 

* #### Instructions how to install Jenkins can be found here: https://www.jenkins.io/doc/book/installing/

* #### This tutorial will be based on Jenkins on Decker and it will slightly differ from the examples mentioned in referred links. The point of this tutorial is to show how to create a basic setup and manage it with Python.

## Running and initial configuration of jenkins with docker compose.
* This project includes [docker-compose.yaml](./docker/docker-compose.yaml) file to start with
* To run Jenkins do:
```bash
$ cd docker
$ docker compose up -d
```
* This should start Jenkins:
```bash
$ docker ps
CONTAINER ID   IMAGE                 COMMAND                  CREATED          STATUS          PORTS                                                                                      NAMES
c1e959b02bb6   jenkins/jenkins:lts   "/usr/bin/tini -- /u…"   37 minutes ago   Up 37 minutes   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp, 0.0.0.0:50000->50000/tcp, :::50000->50000/tcp   jenkins-controller
```

* for more details check:
```bash
$ docker logs jenkins-controller

2024-04-10 20:33:01.117+0000 [id=80]	INFO	jenkins.install.SetupWizard#init: 

*************************************************************
*************************************************************
*************************************************************

Jenkins initial setup is required. An admin user has been created and a password generated.
Please use the following password to proceed to installation:

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    <--- PASSWORD

This may also be found at: /var/jenkins_home/secrets/initialAdminPassword

*************************************************************
*************************************************************
*************************************************************

2024-04-10 20:33:23.841+0000 [id=80]	INFO	jenkins.InitReactorRunner$1#onAttained: Completed initialization

```

* You should be able to access Jenkins managment web UI with [localhost:8080](localhost:8080)
* Provide the password from log output above or follow instructions:

<p align="center">
<img src="pictures/jenkins-initial-config.png" border=2, width=50%>
</p>


TODO: describe plugins installation, agent configuration, docker compose details
TODO: for python project which will do unittests and packaging you mast prepare docker file based on agent image:

```
FROM jenkins/inbound-agent:latest

USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install any other dependencies you might need
# RUN pip3 install <your-dependencies-here>

USER jenkins
```

```
docker build -t my-custom-jenkins-agent .
```
