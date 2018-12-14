
import pandas as pd

def read_csv(file):
    mapping = pd.read_csv(file)[["index", "words"]].set_index("index").T.to_dict('list')
    res = []

    for v in mapping.values():
        res.append(v[0] + ' .')

    return res

