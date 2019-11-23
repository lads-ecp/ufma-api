FROM python:3.7-alpine
RUN apk add --update gcc libc-dev libxml2-dev libxslt-dev
COPY . /web
#WORKDIR /web/scripts
#RUN pip install -r ./requirements.txt
#RUN python script.py
WORKDIR /web/api
RUN pip install -r ./requirements.txt
#RUN python -m pip install pipenv
#RUN pipenv install
#RUN pipenv shell
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]