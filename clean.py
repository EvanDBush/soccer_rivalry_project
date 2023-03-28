import argparse
import json
import logging
from pathlib import Path
import pandas as pd
import numpy as np


# Clean data for Spanish League Data
#
# Usage: 
# $ python clean.py data/spain.csv results/spain_clean.csv
#
# where:
#   data/spain.csv              = path to the input file
#   results/spain_clean.csv     = path to the output file
#
# input file provided: data/spain.csv

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
    EXPECTED_COLUMNS = ['Date', 'Season', 'home', 'visitor', 'HT', 'FT', 'hgoal', 'vgoal',
       'tier', 'round', 'group', 'notes']
    if not all(item in list(df.columns) for item in EXPECTED_COLUMNS):
       logging.error('Input file does not have the expected columns.')
       exit(1)
    return None


def main() -> None:
    """Main cleaning logic
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


    # 1. TODO: Remove games with phase2 in round column.
    logging.info('Step 1: Removing games with phase2 in "round" column.')
    # spain_df = spain_df[spain_df['round'] != 'phase2']

    # 2. TODO: Remove unneeded columns (tier, round, notes, ht)
    logging.info('Step 2: Removing unneeded columns.')
    spain_df.drop(['tier', 'round', 'group', 'notes', 'HT'], axis=1, inplace=True)


    # 3. TODO: Update column names
    logging.info('Step 3: Improving column readability.')
    spain_df.rename(columns={
            'FT': 'score'
        }, inplace=True)


    # 4. TODO: Adding hpoints and vpoints columns
    logging.info('Step 4: Adding hpoints and vpoints columns.')
    
    # determines if home team won and assigns them 3 points
    home_wins_df = spain_df[spain_df['hgoal'] > spain_df['vgoal']]
    home_wins_df = home_wins_df.assign(hpoint = 3, vpoint = 0)
    
    # determines if visiting team won and assigns them three points
    visitor_wins_df = spain_df[spain_df['hgoal'] < spain_df['vgoal']]
    visitor_wins_df = visitor_wins_df.assign(hpoint = 0, vpoint = 3)

    # evaluates ties and assigns each team a single point
    teams_tie_df = spain_df[spain_df['hgoal'] == spain_df['vgoal']]
    teams_tie_df = teams_tie_df.assign(hpoint = 1, vpoint = 1)

    # combines three data frames above into a list of data frames and back into a single dataframe.
    point_df_list = [teams_tie_df, visitor_wins_df, home_wins_df]
    spain_df = pd.concat(point_df_list).sort_values( by= 'Date')
    
 
    logging.info('Saving output file.')
    output_path = Path(output_file)
    if output_path.suffix == '.csv.gz':
        spain_df.to_csv(output_path, index=False, compression="gzip")
    else:
        spain_df.to_csv(output_path, index=False)
    
    return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    main()