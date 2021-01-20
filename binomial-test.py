from scipy.stats import binom
import matplotlib.pyplot as plt

file = open("tournament_results.txt", "r").read()
lines = file.splitlines()
total = 0
p = 1
our_bot_won_list = lines[0].split(">")
our_bot_won = int(our_bot_won_list[1])
print(our_bot_won)
for line in lines:
    line_split = line.split(">")
    total += int(line_split[1])
p = our_bot_won / total
# setting the values
# of n and p
n = 6  # <--how many games were played

# defining the list of r values
r_values = list(range(n + 1))
# obtaining the mean and variance
mean, var = binom.stats(n, p)
# list of pmf values
dist = [binom.pmf(r, n, p) for r in r_values]
# printing the table
print("r\tp(r)")
for i in range(n + 1):
    print(str(r_values[i]) + "\t" + str(dist[i]))
# printing mean and variance
print("mean = " + str(mean))
print("variance = " + str(var))
# defining list of r values
# list of pmf values
dist = [binom.pmf(r, n, p) for r in r_values]
# plotting the graph
plt.bar(r_values, dist)
plt.show()
