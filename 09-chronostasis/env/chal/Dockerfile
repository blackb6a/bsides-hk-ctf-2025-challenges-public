FROM python:3.12

RUN apt-get update && apt-get install -y socat

COPY *.py /home/ctfuser/
RUN python3 -m compileall /home/ctfuser/

ENV FLAG=bsideshk{m4573r_0f_71m3_4nd_ch4nc3}
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"stdbuf -i0 -o0 -e0 python3 /home/ctfuser/chal.py"
