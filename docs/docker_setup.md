
# Testing a REDCap docker image on Mac OS

Useful info [http://docs.docker.com/installation/mac/](http://docs.docker.com/installation/mac/)

## Steps

1) Update the brew cask


    $ brew update && brew upgrade brew-cask

    $ brew cleanup && brew cask cleanup


2) Install the docker stuff (it installs VirtualBox-5.0.4-102546-OSX.dmg)

    $ brew cask install dockertoolbox


3) Create a docker VM (so we can use it to run Docker images)


    $ bash --login '/Applications/Docker/Docker Quickstart Terminal.app/Contents/Resources/Scripts/start.sh'

<pre>
Yous should get something like:
                        ##         .
                  ## ## ##        ==
               ## ## ## ## ##    ===
           /"""""""""""""""""\___/ ===
      ~~~ {~~ ~~~~ ~~~ ~~~~ ~~~ ~ /  ===- ~~~
           \______ o           __/
             \    \         __/
              \____\_______/
docker is configured to use the default machine with IP 192.168.99.100
For help getting started, check out the docs at https://docs.docker.com
</pre>

4) View the VM

    $ docker-machine ls

5) Try to run a demo

    $ docker run hello-world

It will probably fail...

6) Display the commands for setup

    $ docker-machine env default

<pre>
export DOCKER_TLS_VERIFY="1"
export DOCKER_HOST="tcp://192.168.99.100:2376"
export DOCKER_CERT_PATH="/Users/asura/.docker/machine/machines/default"
export DOCKER_MACHINE_NAME="default"
# Run this command to configure your shell:
# eval "$(docker-machine env default)”
</pre>

7) Run the config command suggested

    $ eval "$(docker-machine env default)”


8) Now verify the config

    $ docker run hello-world

<pre>
Hello from Docker.
This message shows that your installation appears to be working correctly.
</pre>


9) Download the image from ... where it is


    $ mkdir ~/docker && cd ~/docker 
    $ cp ../Share/taeber_docker-redcap.tar.gz .


10) Extract the image

    $ gzip -d taeber_docker-redcap.tar.gz


11) Load the image

    $ docker load -i taeber_docker-redcap.tar


12) Run it

    $ docker run taeber/docker-redcap


13)  Find the container id

    $ DOCKER_ID=`docker ps -n=1 | cut -d ' ' -f 1 | tail -1`


14) Start the apache, mysql and test the redcap

    $ docker exec $DOCKER_ID service mysql start
    $ docker exec $DOCKER_ID mysql redcap -e 'select project_id, project_name FROM redcap_projects’

    $ docker exec $DOCKER_ID service apache2 start
    $ docker exec $DOCKER_ID service apache2 status

    $ docker exec $DOCKER_ID curl -s http://localhost/redcap/ | grep -i welcome


You should get:
<pre>
<b>Welcome to REDCap!</b>
</pre>

14) ssh into the docker

    $ docker exec -it $DOCKER_ID bash 

