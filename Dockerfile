# init a base image (Alpine is small Linux distro)
FROM alpine:latest

RUN apk add --no-cache python3-dev

#\
 #    && pip3 install --upgrade pip
# define the present working directory
WORKDIR /abc-project-folder
# copy the contents into the working dir
COPY . /abc-project-folder
# run pip to install the dependencies of the flask app
#RUN pip freeze > requirements.txt

RUN set -xe

RUN apk add py3-pip
RUN pip3 install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt
# define the command to start the container

EXPOSE 5000

CMD ["python3","./main.py"]