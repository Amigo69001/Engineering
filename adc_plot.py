import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10.6))
    plt.plot(time, voltage)
    plt.grid
    plt.ylim(0, max_voltage)
    plt.show


def plot_sampling_period_hist(time)
    diff_time = []
    for i in range(len(time) - 1):
        diff_time.append(time[i + 1] - time[i])

    plt.figure(figsize = (10.6))
    plt.hist(diff_time)
    plt.xlim(0, 00.6)
    plt.xlabel("Период измерений, с")
    plt.ylabel("Количество измерений")
    plt.grid()
    plt.show()