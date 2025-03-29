FROM python:3.12

RUN apt-get update && apt-get install -y socat
RUN pip install pycryptodome

COPY *.py /home/ctfuser/
RUN python3 -m compileall /home/ctfuser/

ENV FLAG=bsideshk{g0D_cr34t3S_34rTh_gCd_cr34t35_d4T4}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 python3 /home/ctfuser/chal.py"
