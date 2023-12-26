# -*- coding: utf-8 -*-

import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
import cv2

def linear_func(x, m, c):
    return m * np.array(x) + c

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
    
    # Scatter plot
    ax1.scatter(xdata, ydata, color='blue', marker='o', s=60, label='data points')
    
    ax1.plot(xs, curve, label="best fit", color="darkorange", linewidth=2, linestyle='-', alpha=0.8)
    
    ax1.legend(loc='upper right')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    residual = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt="o", color="black", markersize=5)
    ax2.axhline(y=0, color="darkgray")
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel("Residuals")

    fig.tight_layout()

    # Convert the Matplotlib figure to a format OpenCV can use
    fig.canvas.draw()
    img_array = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    img_array = img_array.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)  # Convert RGB to BGR
    cv2.imwrite('graph_cv2.png', img_array)

    plt.show()

# Earlier data points, removed the zero data point
xdata = [-1.57, -1.31, -1.04, -0.79, -0.52, -0.26, 0.26, 0.52, 0.79, 1.04, 1.31, 1.57]
ydata = [2.03, 2.01, 2.00, 1.99, 2.01, 2.00, 2.01, 2.01, 2.00, 1.99, 2.01, 2.03]

# Introducing uncertainties
xerror = [0.05] * len(xdata)
yerror = np.random.normal(0.02, 0.005, len(xdata))

# Plotting the graph
plot_fit(linear_func, xdata, ydata, xerror, yerror, xlabel="Angle (radians)", ylabel="Moment")
