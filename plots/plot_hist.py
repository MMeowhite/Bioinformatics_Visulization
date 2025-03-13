import matplotlib.pyplot as plt

def plot(data, **kwargs):
    plt.hist(data['y'], **kwargs)
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()