import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.optimize
import scipy.integrate

# Define functions for fitting
def damped_exp(t, a0, tau):
    if tau < 0:
        return float('nan')
    return a0 * np.exp(-t/tau)

def damped_rat(t, a0, tau):
    if tau < 0:
        return float('nan')
    return a0 / (1.0 + t/tau)

def fit_amplitude(model, t, amp, amp_error):
    popt, popv = scipy.optimize.curve_fit(
        model, t, amp,
        sigma=amp_error*np.ones(len(amp)),
        p0=(0.4, 60.))
    return popt, np.diagonal(popv)**0.5

def damped_harmonic(t, a0, tau, period, phase):
    a = damped_exp(t, a0, tau)
    return a * np.cos(2.*np.pi*t/period + phase)

def fit_data(t, a, a_error, a0_guess=0.4, tau_guess=60.):
    init_guess = (a0_guess, tau_guess, 2.0*np.sqrt(L), 0.0)
    init_guess = scipy.optimize.curve_fit(
        damped_harmonic, t[:100], a[:100], p0=init_guess)[0]
    init_guess = scipy.optimize.curve_fit(
        damped_harmonic, t[:300], a[:300], p0=init_guess)[0]
    popt, popv = scipy.optimize.curve_fit(
        damped_harmonic, t, a,
        p0=init_guess, sigma=a_error*np.ones(len(a)))
    return popt, popv.diagonal()**0.5

def get_amplitudes(t, a):
    t_amp = []
    a_amp = []
    for i in range(1, len(a)-1):
        if (a[i]-a[i-1]) * (a[i]-a[i+1]) <= 0:
            continue
        if False:  # naive approach
            ti, ai = t[i], a[i]
        else:  # quadratic fit - doesn't improve much?
            coes = np.polyfit(t[i-1:i+2], a[i-1:i+2], 2)
            ti = -coes[1]/(2*coes[0])
            ai = coes[2]+ti*(coes[1]+ti*coes[0])
        if len(a_amp) == 0 or abs(ai / a_amp[-1]) > 0.8:
            t_amp.append(ti)
            a_amp.append(abs(ai))
    return np.interp(t, t_amp, a_amp)

def plot_angle_time_graph(l, l_error, t, a, amps, params):
    a_pred = damped_harmonic(t, *params)
    residual = a - a_pred

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})

    ax1.set_title("Angle-Time Plot of a {:.2f}m±{:.2f}m Pendulum".format(l, l_error))
    ax2.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Angle (radians)")

    ax1.plot(t, a, '-')
    ax1.plot(t, a_pred, '--')
    ax1.plot(t, amps, '-')
    ax1.legend(['measured', 'fitted', 'amplitudes'])

    ax2.plot(t, residual)
    ax2.legend(["residual"])
    ax2.plot(t, np.zeros(len(t)), '--')
    plt.show()

# Generate sample data
random.seed(0)

def trig_distribution(center, spread):
    return center + spread * (random.random() + random.random() - 1)

def random_sphere(spread):
    u = 2.0*np.pi * random.random()
    v = 2.0*random.random()-1.0
    r = np.sqrt(1-v*v)
    n = np.array([r*np.cos(u), r*np.sin(u), v])
    return trig_distribution(0.0, spread) * n

# Assuming you have already defined L and xs as your data
L = 0.28  # Length of the pendulum (update with your actual data)
xs = np.array([[ 0.44131233, 32.46510112,  1.07821458, -0.34726394],
               [ 0.47206582, 42.47469918,  1.16121299, -0.38493863],
               [ 0.51057299, 57.33593469,  1.24531895, -0.32115567],
               [ 0.4607001,  83.47463692,  1.31806644, -0.20514355],
               [ 0.49997242, 87.91770813,  1.39318434, -0.21177709],
               [ 0.51463242, 95.17749397,  1.52663931, -0.18254302]])

ts = np.arange(len(xs))  # Assuming you have equally spaced time points

l = np.hypot(xs[:, 0], xs[:, 2])
l = np.mean(l)
l_error = np.sqrt(np.var(l) + 0.01**2)
a = np.arctan2(xs[:, 0], -xs[:, 2])
a -= np.mean(a)
a_error = 0.01 * np.maximum(np.abs(xs[:, 2]), np.abs(xs[:, 0])) / (xs[:, 0]**2 + xs[:, 2]**2)

params, perror = fit_data(ts, a, a_error)
print("Fitted Parameters:", params)
print("Parameter Errors:", perror)
print("Period: {:.5f} ± {:.5f}".format(params[2], perror[2]))

q = 2.0*np.pi * params[1] / params[2]
q_e = 2.0*np.pi * max(abs(perror[1] / params[2]), abs(perror[2] * params[1] / params[2]**2))
print("Q factor: {:.1f} ± {:.1f}".format(q, q_e))

amps = get_amplitudes(ts, a)
plot_angle_time_graph(l, l_error, ts, a, amps, params)
