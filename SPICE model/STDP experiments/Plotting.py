import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("./exp_replicate.txt", sep="	")


# plt.plot(data["time"], data["V(pre)/Ix(U1:TE)"])

def remove_duplicates(x):
    return list(dict.fromkeys(x))


def plot_function(time, r):
    avgResistance = []
    for i in range(35, len(r) - 1):
        if r[i] == r[i + 1]:
            avgResistance.append(r[i])
    avgResistance = remove_duplicates(avgResistance)

    for item in avgResistance:
        print(item)
    plt.plot(range(0, len(avgResistance)), avgResistance, "o")
    plt.xlabel("Pulse Number")
    plt.ylabel("Resistance")
    plt.yscale("log")
    plt.title("Log measurement of resistance over time")
    plt.autoscale()
    plt.show()
    return 0


t = data["time"]
R = data["V(pre)/Ix(U1:TE)"]

plot_function(t, R)
