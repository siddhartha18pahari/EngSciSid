import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt

def parabolic_func(x, a, b, c):
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
    ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt=".", label="data", color="black", lw=1)
    ax1.plot(xs, curve, label="best fit", color="black")
    ax1.legend(loc='upper right')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    residual = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt=".", color="black", lw=1)
    ax2.axhline(y=0, color="black")    
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel("Residuals")

    fig.tight_layout()
    plt.show()
    fig.savefig("graph.png")

# Given data points (converted to radians from degrees)
xdata = [80, 60, 40, 20, -20, -40, -60, -80]
xdata_radians = [np.deg2rad(degree) for degree in xdata]
ydata = [1.68, 1.12, 1.07, 1.05, 1.03, 1.08, 1.11, 1.67]
yerror = [0.65, 0.45, 0.35, 0.25, 0.25, 0.35, 0.45, 0.65]
xerror = [0.05] * len(xdata_radians)  # I assumed the same error in x data as before.

# Plotting the graph
plot_fit(parabolic_func, xdata_radians, ydata, xerror, yerror, xlabel="Angle (radians)", ylabel="Period")
