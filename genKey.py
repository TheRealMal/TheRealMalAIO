import random

for _ in range(0, 20):
    key = "TRM"
    for x in range(0, 4):
        key += "-" + str(random.randint(10000, 100000))
    print(key)
input()