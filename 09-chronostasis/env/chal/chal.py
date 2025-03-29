import random
import time
import os
from math import floor

FLAG = os.getenv("FLAG") or "bsideshk{placeholder_flag}"

def genrandom():
    r = random.randint(0, 3)
    t = time.time()
    
    if r == 0:
        # Get current hour from t
        res = (floor(t) // 3600) % 24
    elif r == 1:
        # Get current minute from t
        res = (floor(t) // 60) % 60
    elif r == 2:
        # Get current second from t
        res = floor(t) % 60
    else:
        # Get first two digits of current millisecond from t
        res = round((t - floor(t)) * 100)
    
    return int(res)

while True:
    random.seed(int(time.time()))
    print("Predict the sequence!")
    succeed = True
    for attempts in range(10):
        tar = genrandom()
        res = int(input("Your prediction? "))
        if res != tar:
            print(f"You guessed {res}, but it was {tar}!")
            succeed = False
            break
        else:
            print(f"You guessed {res}, correct!")
    if succeed:
        print(f"Congratulations! Here's your flag: {FLAG}")
        exit(0)
