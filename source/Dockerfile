FROM pcraster/emis_base:latest

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

COPY cmd.sh server.py server_flask.py uwsgi.ini /
COPY emis_aggregate_method /emis_aggregate_method
COPY test /test

CMD ["/cmd.sh"]
