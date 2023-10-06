import pandas as pd
import numpy as np
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

ipl_matches = "ipl-matches.csv"
matches = pd.read_csv(ipl_matches)

ipl_ball = "IPL_Ball_by_Ball_2008_2022 - IPL_Ball_by_Ball_2008_2022.csv"
balls = pd.read_csv(ipl_ball)