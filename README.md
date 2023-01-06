# European_Soccer_Stats
This repository scraps data of all the biggest 5 competitions in Europe and passes the data to a csv file, where will be shown in a dashboard gerated by DASH-PLOTLY.

The general idea for the project was, to create a tool able to support sports betting analysis in fields like: Corners, Cards and Goals, given TEAM A vs TEAM B in a range of n_matches played, either they were playing in home, away, or both.

This starting files contests the following leagues:
La-Liga, Premier-League, Italiy - A, League One, Bundesliga.

Is easy to add more leagues to the repository, you just have to add more links to the web scrapping file "scrap_football.py".

The data download are much more larger than the showed in the dashboard, in the data.csv you can file much more information as: ball-possession, sides, shots, etc.
To update the file with the most recent data, just click Update Matches button, or than call the method "scrap_football.update_csv_matches()"

The idea of the dashboard is to show the most frequent stats in the past n-th games by team.
The chosen graphs were Scatter Plots, where each plot will mean a match.
