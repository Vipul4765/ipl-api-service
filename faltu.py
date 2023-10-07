import numpy as np
import pandas as pd
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

ipl_ball = "IPL_Ball_by_Ball_2008_2022 - IPL_Ball_by_Ball_2008_2022.csv"
balls = pd.read_csv(ipl_ball)


def bowler_vs_batsmen():
    mask = (balls['batter'] == 'V Kohli') & (balls['bowler'] == 'Rashid Khan')
    selected_rows = balls[mask]['MOHAMMED Shami'].sum()

    print(selected_rows)



# Call the function
bowler_vs_batsmen()
