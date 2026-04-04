import os
path="data"

with os.scandir(path) as es:
    for e in es:
        print(str(e)[11:-2])
