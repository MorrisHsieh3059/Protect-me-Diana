
import re

def extract(x):
    y = re.findall("no=([^&]+)", x)
    z = y[0]
    z = str(z)

    return z
