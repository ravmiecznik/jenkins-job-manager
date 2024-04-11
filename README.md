# Jenkins Job Manager

## This presentation will show how to create basic Jenkins setup with use of *freestyle* and *pipeline* jobs. Here you will also find a basic introduction to Docker. It will also demonstrate how to use exising Python tools and modules to make Jenkins management simpler. You will learn how to create, delete and reconfigure jobs. It will also highlight another Jenkins related features. I will demonstrate low level features of Python which can be useful in many different applications. This demo assumes you have docker installed and working: [docker installation](https://docs.docker.com/get-docker/).<br>
## We will create a Jenkins stages which will test and release THIS PROJECT contents. There will be steps to perform:
* ## linting and static analysis (*pylint*, *flake8*, *mypy*)
* ## unit-tests (*pytest*, *coverage*)
* ## relase (*setuptools*, *wheel*)
## Each stage should report and archive its results.<br><br>

## Here are topic covered in this demo:
## [Jenkins setup](##Jenkins-setup)
* [Jenkins documentation](#Jenkins-documentation)
  * [Jenkins controllers and agents](#More-detailed-information-on-Jenkins-controllers)
  * [Jenkins installation](#instructions-how-to-install-jenkins-can-be-found-here-httpswwwjenkinsiodocbookinstalling)

* [Running jenkins in docker](#this-tutorial-will-be-based-on-jenkins-on-decker-and-it-will-slightly-differ-from-the-examples-mentioned-in-referred-links-the-point-of-this-tutorial-is-to-show-how-to-create-a-basic-setup-and-manage-it-with-python)
  * [Docker file and docker compose file overwiew](#dockerfile-and-docker-compose-file-overwiew)


## [Python and Jenkins](#python-and-jenkins)
* [Jenkins API/CLI](#jenkins-apicli)
* [*python-jenkins* module](#python-jenkins-module)
* [xml parsing and unparsing with *xmltodict* module](#xml-parsingunparsing-with-xmltodict-module)
* [Low-level Python to make things easier](#how-to-make-xml-parsing-simpler-with-python-low-level-feateures)
* [Putting it all together](#putting-it-all-together-with-cli-based-script-argparse-with-subparsers)



## Jenkins setup
Refer to below documentation to get more details on Jenkins but I beleive this article should contain everything to make this demo run just by follwing the steps and use resources added here.
* #### Jenkins documentation: https://www.jenkins.io/doc/ <br>
* #### More detailed information on Jenkins controllers and agents: https://www.jenkins.io/doc/book/managing/nodes/ 

* #### Instructions how to install Jenkins can be found here: https://www.jenkins.io/doc/book/installing/

* #### This tutorial will be based on Jenkins on Decker and it will slightly differ from the examples mentioned in referred links. The point of this tutorial is to show how to create a basic setup and manage it with Python.
 ## *Dockerfile* and *docker-compose* file overwiew
 If you have no docker installed and running refer to [docker installation](https://docs.docker.com/get-docker/).<br>
 **This project was prepared on Ubuntu 22.04 with docker running as a service*<br>
 <br>
 Jenkins can be deployed in few different ways as described in [Jenkins setup](##Jenkins-setup) section but here I am going to use Docker becuase of the following reasons:<br>
 Docker can make your life much easier if you have to create a system which depends and few services. It also lets you keep your host system clean and run other servies in isolation. Docker approach will help you to maintain and manage "system" you are going to deploy. It is fairly easy to revert changes, do a step back or modify anything "from the past". This example also shows how easly you can communicate a system where there is a controller and agent(s), something similar to server-client relation. Docker compose encpsulates this system in single network. Modules like *docker swarm* can monitor your setup and keep it alive but this is not part of this presentation.<br>
 We are going to deploy CI/CD system for this project which will perform thress stages:
 * linting and static analysis
 * unit testing
 * packaging and relase

 All the work will be done of one of the agents, here there will be only one. For this task the agent should contain all the required tools and applications like:
 * Python
 * static analysis tools
 * packaging tools

Since this example is mostly based on Python we need to prepare an enviroment to performa all those actions. Luckly there is ready to use [jenkins/inbound-agent](https://hub.docker.com/layers/jenkins/inbound-agent/latest/images/sha256-8742a4fce1bb6664f5e4f6b133a2673eeeb0cf35e6a00fc8ffec8531bf9c18d3?context=explore) docker file. If you open the link [jenkins/inbound-agent](https://hub.docker.com/layers/jenkins/inbound-agent/latest/images/sha256-8742a4fce1bb6664f5e4f6b133a2673eeeb0cf35e6a00fc8ffec8531bf9c18d3?context=explore) you can get more details which steps there are performed to run the agent. We will get back to it later when will try to connect *agent* to *Jenkins controller*. For higlight I reccomend to review *IMAGE LAYERS* steps and corresponding commands:

<p align="center">
<img src="pictures/docker-layers.png" border=2, width=50%>
</p>

The most important will be the last one.<br>
Using that image as a base for this project we need to add few more things which are shown in the [dockerfile-python-agent](./docker/dockerfile-python-agent)
```docker
FROM jenkins/inbound-agent:latest

USER root

# Install Python 3 and tools
RUN apt-get update
RUN apt-get install -y python3.11 python3.11-dev python3.11-distutils python3-pip
RUN apt install -y python3-pytest python3-flake8 pylint python3-mypy

CMD /usr/bin/bash

USER jenkins
```
As we can see it is going to 'extend' exisiting image with the tools required for the project.
All the `RUN` entries could be joined with `&&` but in this case I prefer to have each `RUN` separate. In case there is a need to remove one step or add something new build of such image will be much faster but on the other hand it will cause image to grow in size. Each `RUN` instruction in a Dockerfile adds a new layer to the image. Docker images are made up of multiple layers, and each layer represents a set of differences from the previous layer. More layers can lead to a larger overall image size, as each RUN command adds some overhead. In this case I care more about speed and time. But note this matters only if you are building the image for the first time or you want to modify it. By the way all instructions in our docker are just extending *IMAGE LAYERS* shown on the picture of *jenkins/inbound-agent* above. It is possible to see all layers and layer sizes with:
```bash
$ docker history -H <image-name>
```

You can build customized image now with:
```bash
$ docker build -t python-agent -f ./dockerfile-python-agent .
```
but lets skip it as this will be part of `docker-compose` file which should simplify mainatance of the system.


 * add docker files overwiew here

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
docker build -t my-custom-jenkins-agent .


<br>

## Python support for Jenkins 
#### Jenkins API/CLI
#### *python-jenkins* module
#### XML parsing/unparsing with *xmltodict* module
#### How to make XML parsing simpler with Python low level feateures
#### Putting it all together with CLI based script (*argparse* with subparsers)