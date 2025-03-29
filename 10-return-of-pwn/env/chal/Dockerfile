FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \ 
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -M blackb6a

WORKDIR /app
COPY --chown=root src/chall .
COPY --chown=root src/flag.txt .
RUN chmod 755 /app && chmod 755 chall && chmod 644 flag.txt

USER blackb6a
CMD ["socat", "TCP-LISTEN:1337,fork,reuseaddr", "EXEC:./chall,stderr"]
EXPOSE 1337
