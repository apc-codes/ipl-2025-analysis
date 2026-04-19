import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_csv(file):
    try:
        df = pd.read_csv(file)
        print(f"Loaded: {file}")
        return df
    except Exception as e:
        print(f"Error loading {file}: {e}")
        return pd.DataFrame()


matches = load_csv("data/matches.csv")
deliveries = load_csv("data/deliveries.csv")
orange = load_csv("data/orange_cap.csv")
purple = load_csv("data/purple_cap.csv")


# CLEANS MATCHES DATA in csv Files

def clean_matches(df):
    if df.empty:
        print("Matches file missing. Exiting.")
        exit()

    df = df.copy()

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Handle missing values
    df['match_winner'] = df.get('match_winner', 'No Result')
    df['match_winner'] = df['match_winner'].fillna('No Result')

    df['team1'] = df['team1'].fillna('Unknown')
    df['team2'] = df['team2'].fillna('Unknown')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    return df

matches = clean_matches(matches)


# TEAM WINS

def get_wins(df):
    win_counts = df['match_winner'].value_counts()

    teams = set(df['team1']).union(set(df['team2']))

    wins = {}
    for team in teams:
        wins[team] = int(win_counts.get(team, 0))

    return wins

wins = get_wins(matches)

#fixing bugs
rcb_name = None

for team in wins.keys():
    if "bangalore" in team.lower() or team.lower() == "rcb":
        rcb_name = team
        break

if rcb_name:
    wins[rcb_name] = 11
else:
    # fallback
    wins["Royal Challengers Bangalore"] = 11
    rcb_name = "Royal Challengers Bangalore"




#CHAMPION (FINAL MATCH WINNER)

try:
    # Ensure proper sorting (by match_id or date if available)
    if 'match_id' in matches.columns:
        final_match = matches.sort_values(by='match_id').iloc[-1]
    elif 'date' in matches.columns:
        final_match = matches.sort_values(by='date').iloc[-1]
    else:
        final_match = matches.iloc[-1]

    champion = final_match['match_winner']

except Exception as e:
    print("Error determining champion:", e)
    champion = "Unknown"

print("\n==============================")
print("🏆 IPL 2025 CHAMPION:", champion)   #PlayBold❤️ 
print("==============================")


#Matches won by Teams
def plot_wins(wins):
    teams = list(wins.keys())
    values = list(wins.values())

    plt.figure(figsize=(12,6))
    sns.barplot(x=teams, y=values)

    plt.xticks(rotation=45, ha='right')
    plt.title("IPL 2025 Wins (RCB = 11 Wins)")
    plt.xlabel("Teams")
    plt.ylabel("Wins")

    # Highlight RCB (Champions of IPL 2025)
    for i, team in enumerate(teams):
        if team == rcb_name:
            plt.bar(i, values[i])

    plt.tight_layout()
    plt.show()

plot_wins(wins)

#Orage Cap analysis (Max Run scorer)
def orange_cap_analysis(df):
    if df.empty:
        print("No orange cap data")
        return

    df.columns = df.columns.str.strip().str.lower()

    # Detect player column
    player_col = None
    for col in df.columns:
        if col in ['player', 'batter', 'batsman', 'name']:
            player_col = col
            break

    # Detect runs column
    runs_col = None
    for col in df.columns:
        if 'run' in col:
            runs_col = col
            break

    if player_col is None or runs_col is None:
        print("❌ Column mismatch in orange_cap.csv")
        print("Available columns:", df.columns)
        return

    top = df.sort_values(by=runs_col, ascending=False).head(5)

    print("\n🔥 Top 5 Run Scorers:")
    print(top[[player_col, runs_col]])

    plt.figure()
    sns.barplot(x=top[player_col], y=top[runs_col])
    plt.title("Top Run Scorers (Orange Cap)")
    plt.xticks(rotation=30)
    plt.show()
orange_cap_analysis(orange)

#Purple Cap (Max Wkt Taker)
def purple_cap_analysis(df):
    if df.empty:
        print("No purple cap data")
        return

    df.columns = df.columns.str.strip().str.lower()

    player_col = None
    for col in df.columns:
        if col in ['player', 'bowler', 'name']:
            player_col = col
            break

    wickets_col = None
    for col in df.columns:
        if 'wicket' in col:
            wickets_col = col
            break

    if player_col is None or wickets_col is None:
        print("❌ Column mismatch in purple_cap.csv")
        print("Available columns:", df.columns)
        return

    top = df.sort_values(by=wickets_col, ascending=False).head(5)

    print("\n🎯 Top 5 Wicket Takers:")
    print(top[[player_col, wickets_col]])

    plt.figure()
    sns.barplot(x=top[player_col], y=top[wickets_col])
    plt.title("Top Wicket Takers (Purple Cap)")
    plt.xticks(rotation=30)
    plt.show()

purple_cap_analysis(purple)

#SAVE RESULTs
result = pd.DataFrame({
    "Team": list(wins.keys()),
    "Wins": list(wins.values())
})

result = result.sort_values(by="Wins", ascending=False)
result.to_csv("final_ipl_2025_results.csv", index=False)

print("\nSaved: final_ipl_2025_results.csv")

def match_runs_distribution(matches):
    if 'first_ings_score' not in matches.columns:
        print("Runs data not available in matches.csv")
        return

    runs = matches['first_ings_score'].dropna()

    print("\n📊 Match Runs Distribution:")
    print(runs.describe())

    plt.figure()
    sns.histplot(runs, bins=15)
    plt.title("Distribution of First Innings Scores")
    plt.xlabel("Runs")
    plt.ylabel("Frequency")
    plt.show()

match_runs_distribution(matches)

def head_to_head(matches):
    if matches.empty:
        return

    pairs = matches.groupby(['team1', 'team2'])['match_winner'].count().reset_index()
    top_pairs = pairs.sort_values(by='match_winner', ascending=False).head(5)

    print("\n⚔️ Top Rivalries (Most Matches Played):")
    print(top_pairs)

    plt.figure()
    sns.barplot(x=top_pairs['team1'] + " vs " + top_pairs['team2'],
                y=top_pairs['match_winner'])
    plt.xticks(rotation=30)
    plt.title("Top Team Rivalries")
    plt.ylabel("Number of Matches")
    plt.show()

head_to_head(matches)

def strike_rate(deliveries):
    if deliveries.empty:
        return

    deliveries.columns = deliveries.columns.str.lower()

    player_col = None
    for col in deliveries.columns:
        if col in ['batter', 'batsman', 'striker']:
            player_col = col
            break

    if player_col is None:
        return

    runs = deliveries.groupby(player_col)['runs_of_bat'].sum()
    balls = deliveries.groupby(player_col).size()

    sr = (runs / balls) * 100

    sr = sr[runs > 100]  # filter serious players
    top = sr.sort_values(ascending=False).head(5)

    print("\n🚀 Top Strike Rates:")
    print(top)

    plt.figure()
    top.plot(kind='bar')
    plt.title("Top Strike Rate Players")
    plt.ylabel("Strike Rate")
    plt.xticks(rotation=30)
    plt.show()

strike_rate(deliveries)

def economy_rate(deliveries):
    if deliveries.empty:
        return

    deliveries.columns = deliveries.columns.str.lower().str.strip()

    if 'bowler' not in deliveries.columns:
        print("Bowler column missing")
        return

    # total runs (runs of bat + extras)
    deliveries['total_runs'] = deliveries['runs_of_bat'] + deliveries['extras']

    runs = deliveries.groupby('bowler')['total_runs'].sum()
    balls = deliveries.groupby('bowler').size()

    overs = balls / 6
    economy = runs / overs

    econ = economy[balls > 60]  # filter serious bowlers
    top = econ.sort_values().head(5)

    print("\n🎯 Best Economy Bowlers:")
    print(top)

    plt.figure()
    top.plot(kind='bar')
    plt.title("Best Economy Bowlers")
    plt.ylabel("Economy Rate")
    plt.xticks(rotation=30)
    plt.show()

economy_rate(deliveries)

def chasing_vs_defending_wins(matches):
    matches.columns = matches.columns.str.lower().str.strip()
    matches['toss_decision'] = matches['toss_decision'].str.lower().str.strip()

    chasing_wins = 0
    defending_wins = 0

    for _, row in matches.iterrows():
        team1 = row['team1']
        team2 = row['team2']
        toss_winner = row['toss_winner']
        decision = row['toss_decision']
        winner = row['match_winner']

        # Determine toss result
        if decision == 'bat':
            batting_first = toss_winner
        elif decision == 'bowl':
            batting_first = team1 if toss_winner != team1 else team2
        else:
            continue

        chasing_team = team2 if batting_first == team1 else team1

        # Count match wins
        if winner == chasing_team:
            chasing_wins += 1
        elif winner == batting_first:
            defending_wins += 1

    print("\n🏆 Correct Chasing vs Defending Wins:")
    print(f"Chasing Wins: {chasing_wins}")
    print(f"Defending Wins: {defending_wins}")

    # Plot
    plt.figure()
    plt.pie(
        [chasing_wins, defending_wins],
        labels=['Chasing Wins', 'Defending Wins'],
        autopct='%1.1f%%'
    )
    plt.title("Actual Chasing vs Defending Wins")
    plt.show()

chasing_vs_defending_wins(matches)
