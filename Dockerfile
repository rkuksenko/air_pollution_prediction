FROM ubuntu
RUN apt-get update

# install python environment
RUN apt-get install -y python --fix-missing
RUN apt-get install -y python3-pip
RUN pip3 install requests
RUN pip3 install django
RUN pip3 install pandas
RUN pip3 install sklearn

ENV LC_ALL='en_US.utf8'

COPY air_pollution_project /root/air_pollution_project

CMD python3 /root/air_pollution_project/manage.py runserver 0.0.0.0:80