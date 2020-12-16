import seaborn as sns
import matplotlib.pyplot as plt


def plot_correlation(dyn):
    plt.figure(figsize=(16, 9))
    plot = sns.heatmap(dyn.corr(), vmin=0.0, vmax=1.0, cmap="Spectral", annot=True)
    plt.subplots_adjust(top=0.9, bottom=0.2, left=0.15, right=1.0)
    plot.set_title("Correlation")
    plt.show()


def plot_lag_correlation(ldf, cdf, lag):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 9))
    sns.heatmap(ldf, vmin=-lag, vmax=lag, cmap="PiYG", center=0, annot=True, ax=ax1)
    sns.heatmap(cdf, vmin=0.0, vmax=1.0, cmap="Spectral", annot=True, annot_kws={"size": 7}, ax=ax2)
    plt.subplots_adjust(top=0.9, bottom=0.2, left=0.085, right=1.0, wspace=0.15)
    fig.suptitle("Lag correlation (max = " + str(lag) + ")")
    plt.show()


def plot_prediction(pred, area):
    pred.plot()
    plt.title("Covid-19 active confirm")
    plt.xlabel("Date")
    plt.ylabel("Cases")
    plt.show()
