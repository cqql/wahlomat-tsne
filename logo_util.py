import os

import pandas as pd
from scipy.misc import imread

INDEX_CSV = pd.read_csv("logos/index.csv")
INDEX = {party: filename for party, filename in INDEX_CSV.itertuples(index=False)}

def read_logo(party):
    if not party in INDEX:
        raise Exception("There is no logo for party {}".format(party))

    return imread(os.path.join("logos", INDEX[party]))
