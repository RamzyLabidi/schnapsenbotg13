import matplotlib.pyplot as plt

# heights of bars
f = open("tournament_results.txt", "r").read()
lines = f.splitlines()
bot_names = []
wins = []
for line in lines:
    line_split = line.split(".")
    bot_name = line_split[1]
    bot_names.append(bot_name)
    last_part = line_split[-1]
    last_part_split = last_part.split()
    win_number = last_part_split[-1]
    wins.append(int(win_number))

height = wins
left = bot_names
# labels for bars

tick_label = bot_names

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label,
        width=0.5, color=['red', 'pink'])

# naming the x-axis
plt.xlabel('bots')
# naming the y-axis
plt.ylabel('wins')
# plot title
plt.title('My bar chart!')

# function to show the plot
plt.show()

plt.savefig('our_experiment_tournament.pdf')
