import hashlib
from pandas import Series

def ser2hash(series):
    result = []
    for item in series:
        if isinstance(item,int):
            item = str(item)
        item = item.encode("utf-8")
        item = hashlib.sha3_512(item).hexdigest()
        result.append(item)
    return Series(result)