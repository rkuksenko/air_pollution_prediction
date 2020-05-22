FROM ubuntu
RUN apt-get update

# install python environment
RUN apt-get install -y python --fix-missing
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN pip3 install django
ENV LC_ALL='en_US.utf8'
