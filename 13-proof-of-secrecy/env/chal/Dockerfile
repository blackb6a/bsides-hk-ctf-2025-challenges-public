FROM sagemath/sagemath:latest

RUN sudo apt-get update && sudo apt-get install -y socat
RUN sage -pip install pycryptodome

WORKDIR /home/ctfuser
COPY *.py ./
COPY *.crs .
RUN sudo sage -python3 -m compileall .

ENV FLAG=bsideshk{H0p3_Y0u_L1k3d_Th15_K2g_Qu1z}
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'stdbuf -i0 -o0 -e0 sage -python3 chal.py'"]
