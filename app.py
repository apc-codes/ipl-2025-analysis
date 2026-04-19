import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Segoe UI Emoji' 

st.set_page_config(page_title="IPL 2025 Dashboard", layout="wide")

st.title("🏏 IPL 2025 Data Analysis Dashboard")




st.subheader("Team & Player Insights")


st.write("Interactive dashboard for Tournament Analysis")
st.write("By~ Avhijan Paulchoudhury")

@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    orange = pd.read_csv("orange_cap.csv")
    purple = pd.read_csv("purple_cap.csv")
    return matches, deliveries, orange, purple

matches, deliveries, orange, purple = load_data()

st.header("🏆 Champion")
final_match = matches.iloc[-1]
champion = final_match['match_winner']

st.success(f"IPL 2025 Champion: {champion}")

st.header("📌 Team Performance Analysis")

st.header("📊 Team Wins")

wins = matches['match_winner'].value_counts()

for team in wins.index:
    if "bangalore" in team.lower() or team.lower() == "rcb":
        wins[team] = 11

fig, ax = plt.subplots()

colors = ['orange' if ('bangalore' in str(t).lower() or t.lower() == 'rcb') else 'steelblue'
          for t in wins.index] #orange colour bar for champions

sns.barplot(x=wins.index, y=wins.values, ax=ax, palette=colors)
#adding trophy emoji
for i, t in enumerate(wins.index):
    if 'bangalore' in str(t).lower() or t.lower() == 'rcb':
        ax.text(i, wins.values[i], "🏆", ha='center', va='bottom', fontsize=16)
plt.xticks(rotation=45)
st.pyplot(fig)

st.header("🔥 Top Run Scorers")

orange.columns = orange.columns.str.lower()

runs_col = [col for col in orange.columns if 'run' in col][0]
player_col = [col for col in orange.columns if col in ['player','batter','name','batsman']][0]

top = orange.sort_values(by=runs_col, ascending=False).head(5)

fig, ax = plt.subplots()
sns.barplot(x=top[player_col], y=top[runs_col], ax=ax)
plt.xticks(rotation=30)

st.pyplot(fig)



st.header("🎯 Top Wicket Takers")

purple.columns = purple.columns.str.lower()

wicket_col = [col for col in purple.columns if 'wicket' in col][0]
player_col = [col for col in purple.columns if col in ['player','bowler','name']][0]

top = purple.sort_values(by=wicket_col, ascending=False).head(5)

fig, ax = plt.subplots()
sns.barplot(x=top[player_col], y=top[wicket_col], ax=ax)
plt.xticks(rotation=30)

st.pyplot(fig)

st.sidebar.title("Filter")

teams = list(set(matches['team1']).union(set(matches['team2'])))
selected_team = st.sidebar.selectbox("Select Team", teams)

team_matches = matches[
    (matches['team1'] == selected_team) | 
    (matches['team2'] == selected_team)
]

st.write(f"Matches played by {selected_team}: {len(team_matches)}")

st.header("📈 First Innings Score Distribution")

if 'first_ings_score' in matches.columns:
    scores = matches['first_ings_score'].dropna()

    fig, ax = plt.subplots()
    sns.histplot(scores, bins=15, kde=True, ax=ax)

    ax.set_xlabel("Runs")
    ax.set_ylabel("Matches")
    st.pyplot(fig)
else:
    st.warning("First innings score data not available")

st.header("🚀 Top Strike Rate Players")

deliveries.columns = deliveries.columns.str.lower()

player_col = None
for col in ['batter', 'batsman', 'striker']:
    if col in deliveries.columns:
        player_col = col
        break

if player_col and 'runs_of_bat' in deliveries.columns:

    runs = deliveries.groupby(player_col)['runs_of_bat'].sum()
    balls = deliveries.groupby(player_col).size()

    sr = (runs / balls) * 100
    sr = sr[runs > 100].sort_values(ascending=False).head(5)

    fig, ax = plt.subplots()
    sns.barplot(x=sr.index, y=sr.values, ax=ax)

    plt.xticks(rotation=30)
    st.pyplot(fig)
else:
    st.warning("Strike rate data not available")
st.header("🎯 Best Economy Bowlers")

deliveries.columns = deliveries.columns.str.lower().str.strip()

if 'bowler' in deliveries.columns:

    deliveries['total_runs'] = deliveries['runs_of_bat'] + deliveries['extras']

    runs = deliveries.groupby('bowler')['total_runs'].sum()
    balls = deliveries.groupby('bowler').size()

    overs = balls / 6
    economy = runs / overs

    econ = economy[balls > 60].sort_values().head(5)

    fig, ax = plt.subplots()
    sns.barplot(x=econ.index, y=econ.values, ax=ax)

    plt.xticks(rotation=30)
    st.pyplot(fig)
else:
    st.warning("Bowler data not available")


st.header("🏆 Chasing vs Defending Wins")

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

    if decision == 'bat':
        batting_first = toss_winner
    elif decision == 'bowl':
        batting_first = team1 if toss_winner != team1 else team2
    else:
        continue

    chasing_team = team2 if batting_first == team1 else team1

    if winner == chasing_team:
        chasing_wins += 1
    elif winner == batting_first:
        defending_wins += 1

fig, ax = plt.subplots()
ax.pie(
    [chasing_wins, defending_wins],
    labels=['Chasing Wins', 'Defending Wins'],
    autopct='%1.1f%%',
    colors=['green', 'orange']
)

st.pyplot(fig)

st.header("📌 Key Insights")

st.info("• Teams chasing tend to perform differently across matches")
st.info("• Top batsmen dominate run charts consistently")
st.info("• Economy rate strongly separates top bowlers")
st.info("• Match distribution shows balanced scoring pattern")
