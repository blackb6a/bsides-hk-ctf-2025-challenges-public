FROM ubuntu:bionic-20210930

ADD https://github.com/krallin/tini/releases/download/v0.19.0/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        xinetd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home blackb6a && mkdir -p /home/blackb6a

COPY ./src /home/blackb6a/
COPY ./app.xinetd /etc/xinetd.d/app
COPY ./src/flag.txt /

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \;

RUN chmod +x /home/blackb6a/chall

WORKDIR /home/blackb6a
EXPOSE 1337

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]