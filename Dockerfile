FROM myflask
WORKDIR /web/api
CMD python loadingdb.py
#RUN adduser -D myuser
#USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]