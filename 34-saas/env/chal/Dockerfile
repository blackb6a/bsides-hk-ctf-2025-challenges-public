FROM ubuntu:noble-20250127

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
        tini xinetd \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --no-create-home pwn && mkdir -p /home/pwn

COPY ./src /home/pwn/
COPY ./app.xinetd /etc/xinetd.d/app

# Flag is in the flag.txt file
COPY --chown=root:root ./flag.txt /flag.txt

RUN chown -R root:root /home && \
    find /home -type d -exec chmod 555 {} \; && \
    find /home -type f -exec chmod 444 {} \; && \
    chmod 444 /flag.txt

RUN chmod +x /home/pwn/chal

WORKDIR /home/pwn
EXPOSE 1337

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/sbin/xinetd","-dontfork"]
