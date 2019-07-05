# Name: Aiden Liu   
# UW NetID: liucc96
# Section: AD
# CSE 160
# Homework 7: Final Project

import csv
from operator import itemgetter
import matplotlib.pyplot as plt


def read_csv(path):
    """Reads the CSV file at path, and returns a list of rows from the file.

    Parameters:
        path: path to a CSV file. 

    Returns:
        list of dictionaries: Each dictionary maps the columns of the CSV file
        to the values found in one row of the CSV file.
    """
    output = []
    csv_file = open(path)
    for row in csv.DictReader(csv_file):
        output.append(row)
    csv_file.close()    
    return output
        

def filter_data(data_lst):
    """Given a data list from (read_csv), filter out repeated player's names.
    Take the data row where the player has played the most number of games.
    (Each player can have multiple dictionaries in data_lst as a player can play
    for different teams throughout the season.)
    
    Parameters:
        data_lst: list of dictionaries with each dictionary representing data
        from each row.
        
    Returns:
        output: list of dictionaries with each dictionary's dict["Player"]
        being unique. (no repeated players)
    """
    output = {}
    # Filter out players whose team is "TOT".
    # If player's data is already in the output, compare the number of games
    # the player played, update the row of data which the "G"
    # (Games played) is higher.
    for row in data_lst:
        player = row["Player"]
        if row["Tm"] == "TOT":
            continue
        elif player in output:
            if row["G"] > output[player]["G"]:
                output[player] = row
                
        output[player] = row
            

    return output.values()
            
         
def extract_data(players_data, column):
    """Given the data of the players and the column of interest, return
    a dictionary mapping each player to his specific stat read from the column.
    
    Parameters:
        players_data: list of dictionaries with each row representing data about
        one player
        
        column: string, a common key in all dictionaries
    
    Returns:
        player_col_dict: dictionary mapping player to his specific stat
    """
    player_col_dict = {}
    for player_dict in players_data:
        player_col_dict[player_dict["Player"]] = player_dict[column]
    
    return player_col_dict


def sorting_rank(player_stat_dict):
    """Given a dictionary mapping each player to his stat, return a dictionary
    mapping each player to the rank of his stat in the entire league.
    
    Parameters:
        player_stat_dict: dictionary mapping player to his stat
    
    Returns:
        player_rank_dict: dictionary mapping player to the rank of his stat
    """
    # Create a list of tuples, each tuple is (player, stat)    
    tuple_lst = player_stat_dict.items()
    # Sort the tuple list according to the stat number, from highest to smallest.
    sorted_tuple_lst = sorted(tuple_lst, key = itemgetter(1), reverse = True)
    # Empty dictionary for player and rank
    player_rank_dict = {}
    # Map each player to his stat rank (stat rank = index + 1)
    for index in range(len(sorted_tuple_lst)):
        player_stat_tuple = sorted_tuple_lst[index]
        player_rank_dict[player_stat_tuple[0]] = index + 1
    
        
    return player_rank_dict


def find_differential(dictionary_one, dictionary_two):
    """Given two dictionaries that contains the same keys,
    find the difference in each key's value. Return a dictionary
    mapping the key to the difference. The length of the given dictionaries 
    and the dictionary to return should be equal.
    
    Parameters:
        dictionary_one: dictionary mapping each player to his stat
        
        dictionary_two: dictionary mapping each player to his stat
        
    Returns:
        differential_dict: dictionary mapping each player to the
        differential of his two stats
    """
    differential_dict = {}
    # For each player in the dictionary, find the difference of his values in
    # the two dictionaries, and map it in the differential dict.
    for player in dictionary_one:
        difference = float(dictionary_one[player]) - float(dictionary_two[player])
        differential_dict[player] = difference
    
    return differential_dict


def find_high_deviation_players(differential_dict, search):
    """Given a dictionary mapping each player to his difference in two stats,
    as well as the search (keyword), find the list of players with high difference.
    
    Parameters:
        differential_dict: dictionary mapping players to their differences in two stats
        search: string of a keyword to search for
        
    Returns:
        high_deviation_lst: list of players that have high difference value
    """
    # If search word is PER/WS, and if the difference in player's ranks in two
    # stats is higher than 80 (absolute), add player to the list
    # If search word is Underpaid/Overpaid, and if the difference in player's
    # deserved and actual salaries is more than $10000000, add player to the list.
    high_deviation_lst = []
    for player in differential_dict:
        difference = differential_dict[player]
        if search == "PER":
            if difference >= 80:
                high_deviation_lst.append(player)
        elif search == "WS":
            if difference <= -80:
                high_deviation_lst.append(player)
        elif search == "Underpaid":
            if difference >= 10000000:
                high_deviation_lst.append(player)
        elif search == "Overpaid":
            if difference <= -10000000:
                high_deviation_lst.append(player)
                 
    return high_deviation_lst
    

def process_team_record_data(team_data_file):
    """Given the filepath to nba team data, return a dictionary mapping each team to
    its team record in a tuple, with first element of the tuple being the
    number of wins and the second element being the number of losses.
    
    Parameters:
        team_data: path to the team record file.
        
    Returns:
        team_record_dict: dictionary, mapping each team (name converted) to
        their wins and losses (as a tuple). 
    """
    team_data = read_csv(team_data_file)
    team_record_dict = {}
    # Take the first three characters of the string if the length of the
    # team's name is 2.
    # Take the first letter of each of the three words if the length of the
    # team's name is 3.
    for team_dict in team_data:
        team_name = team_dict["Team"].upper()
        name_split = team_name.split()
        if name_split == ['PORTLAND', 'TRAIL', 'BLAZERS']:
            team_name_converted = "POR"
        elif name_split == ['OKLAHOMA', 'CITY', 'THUNDER']:
            team_name_converted = "OKC"
        elif name_split == ['BROOKLYN', 'NETS']:
            team_name_converted = "BRK"
        elif name_split == ['CHARLOTTE', 'HORNETS']:
            team_name_converted = "CHO"
        elif len(name_split) == 2:
            team_name_converted = team_name[0 : 3]
        elif len(name_split) == 3:
            team_name_converted = ""
            for i in name_split:
                team_name_converted += i[0]
        else:
            continue
        
        team_record = team_dict["Overall"].split("-")
        team_record_tuple = (int(team_record[0]), int(team_record[1]))
        team_record_dict[team_name_converted] = team_record_tuple
    
    return team_record_dict
    

def calculate_winning_percentage(high_rank_differential_lst, team_record, player_team_dict):
    """Given a list of players, return the overall winning percentage of the players
    in the list.
    
    Parameters:
        high_rank_differential_lst: list of players that have high rank difference
        team_record: dictionary mapping name of each team to his record tuple (wins, losses)
        player_team_dict: dictionary mapping each player to his team name
    
    Returns:
        winning_percentage: overall winning percentage of the teams that the players
        on the list play for
    """
    total_wins = 0
    total_losses = 0 
    # For each player, find out which team he plays for, and find out the
    # team's win loss record.
    # Sum up all the wins and losses and calculate the winning percentage.
    for player in high_rank_differential_lst:
        team = player_team_dict[player]
        wins = team_record[team][0]
        losses = team_record[team][1]
        
    total_wins += wins
    total_losses += losses
    winning_percentage = float(total_wins) / (total_wins + total_losses)
    return winning_percentage
    
    
def compare_winning_percentage(larger_per_winning, larger_ws_winning):
    """Given two winning percentages, compare which winning percentage is
    higher, and conclude which stat is better.
    
    Parameters:
        larger_per_winning: the winning percentage of players with much higher
        PER rank number (PER ranks them worse)
        
        larger_ws_winning: the winning percentage of players with much higher
        WS rank number (WS ranks them worse)
    
    Returns:
        None
    """
    # If winning percentage for players with high PER rank number is higher than
    # that of players with high WS rank number, it shows that WS is more accurate.
    # (since lower rank number = more impactful players)
    ws_stat = "Win Shares(WS)"
    per_stat = "PER"
    better_stat = ""
    worse_stat = ""
    if larger_per_winning > larger_ws_winning:
        better_stat = ws_stat
        worse_stat = per_stat
    else:
        better_stat = per_stat
        worse_stat = ws_stat
    
    print "Winning percentage of players whose PER ranks are much lower than their " + \
            "WS ranks (better PER stat) = " + str(larger_ws_winning)
    print
    print "Winning percentage of players whose WS ranks are much lower than their " + \
            "PER ranks (better WS stat) = " + str(larger_per_winning)
    print
    print "From this result, we can conclude that " + better_stat + " is the more " + \
           "accurate statistic in measuring a player's impact on winning as for" + \
           " players with much lower rank number (ranks great) of " + better_stat + \
           ", their winning percentage is better than that of the players who have lower" + \
           " rank number of " + worse_stat + "."


def calculate_percentage_better(stat1, stat2):
    """Given two statistics, calculate and return the how much (in percentage) that 
    one stat is higher than the other. If stat1 is 20% higher than stat2,
    it means that stat1's percentage_better to stat2 is 0.2.
    
    Parameters:
        stat1: float 
        stat2: float
        
    Returns:
        percentage_better: float indicating how much better is one stat
        over the other.
    """
    larger_num = max(stat1, stat2)
    smaller_num = min(stat1, stat2)
    percentage_better = (larger_num - smaller_num) / smaller_num
    
    return percentage_better
           

def calculate_weighted_stat(high_per_winning, high_ws_winning):
    """Given the two stats, calculate how much higher is one stat over the other.
    Calculate and return the weightage of each of the PER/WS stat
    that should be allocated in calculating the True Impact (TI) of a player.
    
    Parameters:
        high_per_winning: float of winning percentage of players with much high PER rank number
        high_ws_winning: float of winning percentage of players with much higher WS rank number
    
    Returns:
        (weighted_per, weighted_ws): tuple of how much (in %) should PER and WS be used
        in calculating TI. weighted_per + weighted_ws = 1
    """
    # By default, weighted_ws/weighted_per = 0.5
    percentage_better = calculate_percentage_better(high_per_winning, high_ws_winning)
    if high_per_winning > high_ws_winning:
        weighted_ws = 0.5 * percentage_better + 0.5
        weighted_per = 1 - weighted_ws
    else:
        weighted_per = 0.5 * percentage_better + 0.5
        weighted_ws = 1 - weighted_per
    
    return (weighted_per, weighted_ws)
    
    
def calculate_league_average(player_stat_dict):
    """Given a dictionary mapping each player to a particular stat of his,
    sum up all the players' stat and return the average of the stat throughout
    the entire league.
    
    Parameters:
        player_stat_dict: dictionary mapping each player to his stat
        
    Returns:
        league_average: float of average of that particular stat in the league
    """
    # Sum up the stat number and divide by the number of players in the league
    stat_sum = 0
    for player in player_stat_dict:
        stat = player_stat_dict[player]
        stat_sum += float(stat)
        
    league_average = stat_sum / len(player_stat_dict)
    return league_average


def compute_stat_index(player_stat_dict):
    """Given a dictionary mapping players and his stat, return a dictionary
    mapping each player to how far his stat is from the league average of that
    particular stat. e.g ({"Lebron James": 1.0} = Lebron James's stat is 100%
    higher than the league average of that stat.
    
    Parameters:
        player_stat_dict: dictionary mapping each player to his stat
        
    Returns:
        stat_index_dict: dictionary mapping each player to the deviation
        of his stat.
    """
    # Calculate the league average of stat.
    avg_stat = calculate_league_average(player_stat_dict)
    stat_index_dict = {}
    for player in player_stat_dict:
        stat_value = player_stat_dict[player]
        deviation = float(stat_value) - avg_stat
        deviation_percentage = deviation / avg_stat
        stat_index_dict[player] = deviation_percentage

    return stat_index_dict

   
def calculate_stat_factor(average_per, average_ws):
    """Given the average PER and average Win Shares(WS) of the league, calculate
    how many times higher the average PER is. Returns a factor that will be used
    in calculating a player's TI.
    
    Parameters:
        average_per: float
        average_ws: float
    
    Returns: stat_factor: float of the multiple
    """
    stat_factor = float(average_per) / average_ws
    
    return stat_factor 
      

def compute_player_ti(weightage_tuple, per_dict, ws_dict, factor):
    """Given the weightage tuple and the dictionaries of the players'
    PER and WS stats, compute each player's True Impact(TI) and return a
    dictionary mapping players to their ti values.
    (TI formula: weightedPER * player's PER + weightedWS * factor * player's WS)
    
    Parameters:
        weightage_tuple: tuple showing the weightage of each stat
        per_dict: dictionary mapping players to their per
        ws_dict: dictionary mapping players to their ws
        
    Returns:
        ti_values_dict: dictionary mapping players to their TI values
    """
    # For each player, find his PER and WS values, and compute his TI value.
    # Map player with his TI value.
    ti_values_dict = {}
    for player in per_dict:
        player_per = per_dict[player]
        player_ws = ws_dict[player]
        player_ws_factored = float(player_ws) * factor
        ti_value = weightage_tuple[0] * float(player_per) + weightage_tuple[1] * player_ws_factored
        ti_values_dict[player] = ti_value
    return ti_values_dict
    

def compute_players_salary_deserved(players_ti_index, avg_salary):
    """Given the TI index dictionary and the league average salary,
    return a dictionary mapping each player to his deserved salary according
    to their TI index (how far the player's TI value is from the league average TI)
    
    Parameters:
        players_ti_index: dictionary mapping each player to his ti index
        avg_salary: float of the league average salary
    
    Returns:
        players_salary_deserved_dict: dictionary mapping each player to his
        deserved salary
    """
    # deserved salary = average salary * ti_index + average salary
    players_salary_deserved_dict = {} 
    for player in players_ti_index:
        ti_index = players_ti_index[player]
        deserved_salary = avg_salary * ti_index + avg_salary
        players_salary_deserved_dict[player] = deserved_salary
    
    return players_salary_deserved_dict


def convert_string_to_float(salary_dict):
    """Given a dictionary, convert the values in the dictionary from strings
    to floats.
    
    Parameters:
        salary_dict: dictionary mapping player to his salary
        
    Returns:
        converted_dict: dictionary mapping player to his converted salary
    """
    converted_dict = {}
    # Replace each "," and "$" with an empty string
    # Convert to float by calling float
    for player in salary_dict:
        salary = salary_dict[player]
        replaced = salary.replace(",", "")
        replaced_salary = replaced.replace("$", "")
        converted_dict[player] = float(replaced_salary)
        
    return converted_dict


def find_datasets_intersection(dict1, dict2):
    """Given two dictionaries, returns a set of the common keys in the two
    dictionaries.
    
    Parameters:
        dict1: dictionary mapping player and stat
        dict2: dictionary mapping player and stat
    
    Returns:
        intersection_set: set containing the players that are in both the dictionaries
    """
    # Add the keys in the two dictionaries to two separate sets.
    # Find their intersection
    set1 = set()
    set2 = set()
    for element in dict1:
        set1.add(element)
    
    for element in dict2:
        set2.add(element)
    
    intersection_set = set1 & set2
    return intersection_set


def filter_dictionary(unique_set, player_stat_dict):
    """Given a set and dictionary mapping player to stat,
    filter the dictionary and return a new dictionary made up of keys
    that are in both the set and the dictionary.
    
    Parameters:
        unique_set: set of players
        player_stat_dict: dictionary mapping player to stat
    
    Returns:
        output: dictionary of players(keys) that are in both unique_set
        and player_stat_dict
    """
    output = {}
    # Check if the player is in the unique_set
    for player in player_stat_dict:
        if player in unique_set:
            output[player] = player_stat_dict[player]
    
    return output


# This function was supposed to plot out a bar chart of the underpaid/overpaid
# players with their salary difference (deserved salary vs actual)
# I was able to plot the bar chart. However, there were too many names and it
# doesn't really show anything.
# I really hope that I would be able to create a proper bar chart in the future.
# At this point of time, I do not have the knowledge and time to plot it out.

#def plot_players(player_lst, salary_diff_dict):
    #"""
    #"""
    #player_set = set()
    #for player in player_lst:
        #player_set.add(player)
        
    #player_dict = filter_dictionary(player_set, salary_diff_dict)
    #lst1 = []
    #lst2 = []
    #x = []
    #for player in player_dict:
        #lst1.append(player)
        #lst2.append(player_dict[player])
            
    #for index in range(len(player_dict)):
        #x.append(index)
        
    #plt.xticks(x, lst1)
    #plt.bar(x, lst2, 1000)
    #plt.show()
    
    
    
def main():
    
    # Read in the file
    unfiltered_data = read_csv("2017-2018-nba-players-stats-advanced.csv")
    # Filter data
    filtered_data = filter_data(unfiltered_data)
    
    # Finding player and his PER rank
    player_per_dict = extract_data(filtered_data, "PER")
    player_per_rank_dict = sorting_rank(player_per_dict)
    
    # Finding player and his WS rank
    player_ws_dict = extract_data(filtered_data, "WS")
    player_ws_rank_dict = sorting_rank(player_ws_dict)
    
    # Finding every player's rank differential (PER rank number - WS rank number)
    player_rank_differential_dict = find_differential(player_per_rank_dict, player_ws_rank_dict)
    
    # Finding players with high deviation (PER rank num > WS rank num & WS rank num > PER rank num)
    high_per_players_lst = find_high_deviation_players(player_rank_differential_dict, "PER")
    high_ws_players_lst = find_high_deviation_players(player_rank_differential_dict, "WS")
    
    # Finding team_data
    team_data = process_team_record_data("2017-2018-nba-team-record.csv")
    player_team_dict = extract_data(filtered_data, "Tm")
    
    # Calculate winning percentage for players with high deviation
    high_per_wp = calculate_winning_percentage(high_per_players_lst, team_data, player_team_dict)
    high_ws_wp = calculate_winning_percentage(high_ws_players_lst, team_data, player_team_dict)
    
    # Comparing winning percentages
    compare_winning_percentage(high_per_wp, high_ws_wp)
    
    # Find weighted tuple
    weighted_stat_tuple = calculate_weighted_stat(high_per_wp, high_ws_wp)
    
    # Compute players' TI values
    league_avg_per = calculate_league_average(player_per_dict)
    league_avg_ws = calculate_league_average(player_ws_dict)
    factor = calculate_stat_factor(league_avg_per, league_avg_ws)
    player_ti_dict = compute_player_ti(weighted_stat_tuple, player_per_dict, player_ws_dict, factor)
    
    # Process player's salary data
    players_salary_data = read_csv("nba-players-salary.csv")
    # Removing the last empty row
    if (players_salary_data[-1]["2017-18"] == ""):
        players_salary_data = players_salary_data[:-1]
    # Extract player's 2017-2018 salary data
    players_salary_dict_unconverted = extract_data(players_salary_data, "2017-18")
    # Convert the data string to float
    players_salary_dict = convert_string_to_float(players_salary_dict_unconverted)
    
    # Focus on players who are both in nba stats and nba salary data
    intersection_set = find_datasets_intersection(player_ti_dict, players_salary_dict)
    filtered_players_salary_dict = filter_dictionary(intersection_set, players_salary_dict)
    filtered_player_ti_dict = filter_dictionary(intersection_set, player_ti_dict)
    
    # Find out players' TI index and his deserved salary
    league_avg_salary = calculate_league_average(filtered_players_salary_dict)
    ti_index_dict = compute_stat_index(filtered_player_ti_dict)
    deserved_salary_dict = compute_players_salary_deserved(ti_index_dict, league_avg_salary)
    
    # Find out the difference between what players should be making with what he actually makes.
    salary_difference_dict = find_differential(deserved_salary_dict, players_salary_dict)
    
    # List out underpaid/overpaid players (in $, $10000000 difference)
    underpaid_lst = find_high_deviation_players(salary_difference_dict, "Underpaid")
    overpaid_lst = find_high_deviation_players(salary_difference_dict, "Overpaid")
    
    print
    print "Underpaid players (> $10000000 difference): ", underpaid_lst
    print
    print "Overpaid players (> $10000000 difference): ", overpaid_lst


if __name__ == "__main__":
    main()

        
                    
                    
                 
    
    
    
    


        
         
       
        
    
    
        
    
    

        
            
    
    
    
     


