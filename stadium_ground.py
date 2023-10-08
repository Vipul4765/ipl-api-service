import pandas as pd
import numpy as np
import json
from connect_database import load_cached_data


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


# To load the data in balls and matches
load_cached_data()
from connect_database import balls_data, matches_data

def stadium_vs_batsman(batsman_name):
    try:
        # Read CSV data from stadium file
        #matches = pd.read_csv('stadium_column_add.csv')
        matches = matches_data

        # Read CSV file from ball by ball
        #ipl_ball = "IPL_Ball_by_Ball_2008_2022 - IPL_Ball_by_Ball_2008_2022.csv"
        #balls = pd.read_csv(ipl_ball)
        balls = balls_data

        # Merge both CSV files
        balls_match = pd.merge(balls, matches, on='ID')

        # Filter the DataFrame for the specified batsman
        batsman_data = balls_match[balls_match['batter'] == batsman_name]

        # Create a list of unique stadiums where the batsman played
        unique_stadiums = batsman_data['Stadium'].unique()

        result_dict = {}  # Initialize an empty dictionary to store results

        for stadium in unique_stadiums:
            # Filter data for the current stadium and batsman
            specific_data = batsman_data[batsman_data['Stadium'] == stadium]

            # Calculate statistics
            total_runs = specific_data['batsman_run'].sum()
            total_balls = specific_data.shape[0]
            wide_balls = (specific_data['extra_type'] == 'wides').sum()
            balls_faced_by_batsman = total_balls - wide_balls
            strike_rate = round((total_runs / balls_faced_by_batsman) * 100, 2)
            fours = len([run for run in specific_data['batsman_run'] if run == 4])
            sixes = len([run for run in specific_data['batsman_run'] if run == 6])
            dismissals = (specific_data['isWicketDelivery'] == 1).sum()
            total_innings = len(specific_data['ID'].unique())

            # Store results in the dictionary
            result_dict[stadium] = {
                'Total_Runs': total_runs,
                'Fours': fours,
                'Sixes': sixes,
                'Strike_Rate': strike_rate,
                'Dismissals': dismissals,
                'Total_Innings': total_innings
            }

        data = {
            batsman_name: {'against': result_dict}
        }

        return json.dumps(data, cls=NpEncoder)

    except Exception as e:
        return str(e)  # Handle exceptions and return an error message if necessary





