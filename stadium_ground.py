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


#matches['Stadium'] = matches['Venue'].str.split(', ', n=1).str[0] #create new_csv file to add stadium column
#new_csv_file_path = "stadium_column_add.csv"
#matches.to_csv(new_csv_file_path, index=False)

def stadium_vs_batsman():
    #read_csv_data_from_stadium_file
    matches = pd.read_csv('stadium_column_add.csv')

    #read_csv_file_from_ball_by_ball
    ipl_ball = "IPL_Ball_by_Ball_2008_2022 - IPL_Ball_by_Ball_2008_2022.csv"
    balls = pd.read_csv(ipl_ball)

    #Merge both csv_file
    balls_match = pd.merge(balls, matches, on='ID')


     #Column in data frame of the stadium


    result_dict = {}  # Initialize an empty dictionary to store results.
    grouped = balls_match.groupby(['Stadium', 'batter'])  # Group the DataFrame by 'Stadium' and 'batter'.

    # Filter the DataFrame for 'V Kohli' as the batter.
    all_stadium = balls_match[balls_match['batter'] == 'V Kohli']

    # Create a list of unique stadiums where 'V Kohli' played.
    all_stadium = list(all_stadium['Stadium'].unique())

    for stadium in all_stadium:
        # Get the specific group for the current stadium and 'V Kohli'.
        specific_group = grouped.get_group((stadium, 'V Kohli'))

        # Calculate the total runs scored by 'V Kohli'.
        total_run = specific_group['batsman_run'].sum()

        # Filter for fours and sixes.
        fours = specific_group[specific_group['batsman_run'] == 4]
        six = specific_group[specific_group['batsman_run'] == 6]

        # Calculate the total number of balls faced by 'V Kohli'.
        total_balls = specific_group.shape[0]

        # Count the wide balls (balls with 'extra_type' == 'wides').
        wide_balls = (specific_group['extra_type'] == 'wides').sum()

        # Calculate the number of balls faced by 'V Kohli' excluding wides.
        balls_faced_by_batsmen = total_balls - wide_balls

        # Calculate the strike rate.
        strike_rate = round((total_run / balls_faced_by_batsmen) * 100, 2)

        # Count the dismissals (wickets taken).
        out = (specific_group['isWicketDelivery'] == 1).sum()

        # total Inning
        total_inning = len(specific_group['ID'].unique())

        # Store the results in the result_dict.
        result_dict[stadium] = {
            'Total_Runs': total_run,
            'Fours': len(fours),  # Count of fours
            'Six': len(six),  # Count of sixes
            'Strike_rate': strike_rate,
            'Dismissal': out,
            'Total_inning': total_inning
        }

    data = {
        'V Kohli': {'against': result_dict
                  }
    }
    return json.dumps(data, cls=NpEncoder)

