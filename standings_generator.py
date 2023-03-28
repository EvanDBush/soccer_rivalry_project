import argparse
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np


# Generate standings data for Spanish League. 
# After cleaning data and adding points with clean.py,
# use this script to generate a csv file containing 
# the results of each season for each team involved.
#
# Usage: 
# $ python standings_generator.py results/spain_clean.csv results/season_standings.csv
#
# where:
#   results/spain_clean.csv              = path to the input file
#   results/season_standings.csv         = path to the output file
#
# input file provided: results/spain_clean.csv

def get_file_names() -> tuple:
    """Get the input and output file names from the arguments passed in
    @return a tuple containing (input_file_name, output_file_name)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Name of the original data file.")
    parser.add_argument("output_file", help="Name of the file for cleaned data.")
    args = parser.parse_args()
    return args.input_file, args.output_file


def validate_columns(df: pd.DataFrame) -> None:
    """Validates that the data in the input file has the expected columns. \
    Exits with an error if the expected columns are not present.
    @param df - The DataFrame object with the data from the input file.
    """
    EXPECTED_COLUMNS = ['Date', 'Season', 'home', 'visitor', 'score', 'hgoal', 'vgoal','hpoint', 'vpoint']
    if not all(item in list(df.columns) for item in EXPECTED_COLUMNS):
       logging.error('Input file does not have the expected columns.')
       exit(1)
    return None


def main() -> None:
    """Main logic
    """
    logging.info('Getting file names from arguments.')
    input_file, output_file = get_file_names()
    logging.info(f'Input file is: {input_file}')
    logging.info(f'Output file is: {output_file}')
 
    logging.info('Loading data from input file.')
    input_path = Path(input_file)
    if not input_path.exists():
        logging.error(f'Input file not found: {input_file}')
        exit(1)
    spain_df = pd.read_csv(input_path)

    logging.info('Validating columns in input file.')
    validate_columns(spain_df)


    season_list = spain_df['Season'].unique()
    all_season_standings_list = []
    for season in season_list:
        season_records = spain_df[spain_df['Season'] == season]
        team_list = season_records['home'].unique()
        empty_list = []
        for team in team_list:
            # gets team records
            team_home_record = season_records[season_records['home'] == team]
            team_visitor_record = season_records[season_records['visitor'] == team]
            team_season_records_df = [team_home_record, team_visitor_record]
            team_season_records_df = pd.concat(team_season_records_df).sort_values( by= 'Date')
                
            #gets team points
            team_home_points = team_home_record['hpoint'].sum()
            team_visitor_points = team_visitor_record['vpoint'].sum()
            team_season_points = team_home_points + team_visitor_points
                
            #adds team goals
            team_home_goals = team_home_record['hgoal'].sum()
            team_visitor_goals = team_visitor_record['vgoal'].sum()
            team_total_goals = team_home_goals + team_visitor_goals
            
            #gets goal totals
            team_home_goals_allowed = team_home_record['vgoal'].sum()
            team_visitor_goals_allowed = team_visitor_record['hgoal'].sum()
            team_total_goals_allowed = team_home_goals_allowed + team_visitor_goals_allowed
            team_goal_differential = team_total_goals - team_total_goals_allowed

            #gets team home WLT records
            team_home_wins = team_home_record[team_home_record['hgoal'] > team_home_record['vgoal']].shape[0]
            team_home_losses = team_home_record[team_home_record['hgoal'] < team_home_record['vgoal']].shape[0]
            team_home_ties = team_home_record[team_home_record['hgoal'] == team_home_record['vgoal']].shape[0]

            #gets team away WLT records
            team_away_wins = team_visitor_record[team_visitor_record['hgoal'] < team_visitor_record['vgoal']].shape[0]
            team_away_losses = team_visitor_record[team_visitor_record['hgoal'] > team_visitor_record['vgoal']].shape[0]
            team_away_ties = team_visitor_record[team_visitor_record['hgoal'] == team_visitor_record['vgoal']].shape[0]

            #gets team WLT totals
            team_total_wins = team_home_wins + team_away_wins
            team_total_losses = team_home_losses + team_away_losses
            team_total_ties = team_home_ties + team_away_ties

            team_stats = {'Season': season, 'Team': team, 'Points': team_season_points, 
                            'GS': team_total_goals, 'GA': team_total_goals_allowed, 
                            'GD': team_goal_differential, 'Wins': team_total_wins, 
                            'Losses': team_total_losses, 'Ties': team_total_ties}
            empty_list.append(team_stats)
        
        season_standings_df = pd.DataFrame(empty_list)
        season_standings_df = season_standings_df.sort_values(by= 'Points', ascending= False).reset_index(drop=True)
        all_season_standings_list.append(season_standings_df)
    all_season_standings_df = pd.concat(all_season_standings_list)
 
    logging.info('Saving output file.')
    output_path = Path(output_file)
    if output_path.suffix == '.csv.gz':
        all_season_standings_df.to_csv(output_path, index=False, compression="gzip")
    else:
        all_season_standings_df.to_csv(output_path, index=False)
    
    return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    main()