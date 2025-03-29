FROM sagemath/sagemath:latest

RUN sudo apt-get update && sudo apt-get install -y socat
RUN sage -pip install pycryptodome

WORKDIR /home/ctfuser
COPY *.py ./
# COPY *.crs .
RUN sudo sage -python3 -m compileall .

ENV FLAG=bsideshk{D0nt_trU5t_tH3_3m0j1c0n5}
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'stdbuf -i0 -o0 -e0 sage -python3 chal.py'"]
