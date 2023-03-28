# El Classico: World's Biggest Sports Rivalry

A data analysis project for Code Louisville Data Analysis Course 1.

This project uses spanish soccer league data from 1929-2022 to examine the head-to-head records between the leagues biggest two clubs: Real Madrid and FC Barcelona.

All packages to run the project are located in the *requirements.txt* file. Pandas and Matplotlib are the primary libraries used.

**Setup Instructions**


First, run the *clean.py* script in the terminal to remove unnescessary columns and calculate point values for each match record.

`$ python clean.py data/spain.csv results/spain_clean.csv`

 Once the points are calculated and added to the data, a new csv file is created in the *results* folder.

The next step is to run the *standings_generator.py* script to calculate the results of each season and write them to a csv file.

`$ python standings_generator.py results/spain_clean.csv results/season_standings.csv`

This data file contains the season totals for each team including: points, wins, losses, ties, goals scored, goals conceeded and goal differential.

### 5 features included:
    
    1. Read in data from a local csv.
        
        - In *clean.py* data is read in from data/spain.csv on line 57 and converted to a pandas dataframe for manipulation.
        
        `spain_df = pd.read_csv(input_path)`

    2. Use built in pandas or numpy functions to handle data (drop columns, remove null values)
        
        - In *clean.py* built in pandas funtions are used to remove columns and calculate and add new ones. on line 69:

        `spain_df.drop(['tier', 'round', 'group', 'notes', 'HT'], axis=1, inplace=True)`

        on line 74:

        `spain_df.rename(columns={'FT': 'score'}, inplace=True)`


    3. Do 5 basic calculations with pandas.
        
        i. Get unique values for a column
            -in *standings_generator.py*, line 65:
            `season_list = spain_df['Season'].unique()` 
        ii. Concatenate 3 dataframes into one
            - in *standings_generator.py*, line 94:
            `spain_df = pd.concat(point_df_list).sort_values( by= 'Date')`
        iii. Write dataframe to CSV
            - in *standings_generator.py*, line 100:
            `spain_df.to_csv(output_path, index=False, compression="gzip")`
        iv. Get the sum of a column in a pandas dataframe
            - in *standings_generator.py* line 82:
            `team_home_points = team_home_record['hpoint'].sum()`
        v. Create a new dataframe from calculate results
            - in *standings_generator.py* line 118:
            `season_standings_df = pd.DataFrame(empty_list)`

    4. Make 2 basic plots with matplotlib.


    5. Write markdown cells in Jupyter explaining your thought process and code.