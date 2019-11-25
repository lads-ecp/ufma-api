FROM myflask
COPY . /web
WORKDIR /web/api
RUN ls -la| grep base
RUN python --version
#RUN python loadingdb.py
RUN ls -la| grep base
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]