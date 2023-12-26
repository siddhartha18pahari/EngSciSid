import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt

def function(x, a, b, c):
    return a * np.array(x)**2 + b * np.array(x) + c

def plot_fit(my_func, xdata, ydata, xerror=None, yerror=None, init_guess=None, font_size=14,
             xlabel="Independant Variable (units)", ylabel="Dependent Variable (units)"):

    plt.rcParams.update({'font.size': font_size})
    plt.rcParams['figure.figsize'] = 10, 9

    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess)
    puncert = np.sqrt(np.diagonal(pcov))

    print("Best fit parameters, with uncertainties, but not rounded off properly:")
    for i in range(len(popt)):
        print(popt[i], "+/-", puncert[i])

    start = min(xdata)
    stop = max(xdata)
    xs = np.arange(start, stop, (stop-start)/1000)
    curve = my_func(xs, *popt)

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]})

    # Data and Fit lines
    ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt="o", markersize=5, capsize=3, label="Data", color="blue", lw=1)
    ax1.plot(xs, curve, label="Best Fit", color="red", linewidth=2)

    # Grids
    ax1.grid(True, linestyle='--', which='both', color='lightgrey', zorder=-10)

    # Legend
    ax1.legend(loc='upper right', fontsize='medium')

    # Labels
    ax1.set_xlabel(xlabel, fontsize=font_size)
    ax1.set_ylabel(ylabel, fontsize=font_size)
    ax1.set_title("Curve Fitting of Data", fontsize=font_size+2)

    # Residuals
    residual = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt="o", markersize=5, capsize=3, color="blue", lw=1)
    ax2.axhline(y=0, color="red", linewidth=1.5)
    ax2.grid(True, linestyle='--', which='both', color='lightgrey', zorder=-10)
    ax2.set_xlabel(xlabel, fontsize=font_size)
    ax2.set_ylabel("Residuals", fontsize=font_size)

    fig.tight_layout()
    plt.show()
    fig.savefig("graph_beautiful.png")

# Given data points with asymmetry introduced (converted to radians from degrees)
xdata = [80, 60, 40, 20, -20, -40, -60, -80]
xdata_radians = [np.deg2rad(degree) for degree in xdata]
ydata = [1.89, 1.16, 1.09, 1.01, 1.03, 1.10, 1.29, 1.63]  # Adjusted the y-data for angles -40 and -60
yerror = [0.63, 0.41, 0.34, 0.25, 0.26, 0.36, 0.44, 0.64]
xerror = [0.05] * len(xdata_radians)

# Plotting the graph
plot_fit(function, xdata_radians, ydata, xerror, yerror, xlabel="Angle (radians)", ylabel="Period")
