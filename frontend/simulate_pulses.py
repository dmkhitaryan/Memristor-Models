import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import scipy.stats as stats
import os
import multiprocessing as mp
import argparse
from block_timer.timer import Timer

from functions import *
from models import *
from experiments_new import *

###############################################################################
#                                  Setup
###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument("-e", '--experiment', type=str, default="yakopcic pulse",
                    help="The input shape to use.")
parser.add_argument('-s', '--solvers', nargs="+", default=["Euler"],
                    help="The solvers to use to simulate the model's evolution.")
parser.add_argument('--video', dest="video", action="store_true",
                    help="Generate video of the simulation.")
parser.set_defaults(new=False)
args = parser.parse_args()

experiments = {
    "yakopcic triangle": yakopcic_triangle,
    "yakopcic pulse": yakopcic_pulse
}

experiment = experiments[args.experiment]()

time = experiment.simulation["time"]
dt = experiment.simulation["dt"]
x0 = experiment.simulation["x0"]
dxdt = experiment.functions["dxdt"]
V = experiment.functions["V"]
I = experiment.functions["I"]

####

###############################################################################
#                         ODE simulation
###############################################################################

# Plot simulated memristor behaviour
for solv in args.solvers:
    # Solve ODE iteratively using Euler's method
    if solv == "Euler":
        with Timer(title="Euler"):
            print("Simulating with Euler solver")
            x_euler = solver(dxdt, time, dt, x0, method="Euler")
            x = x_euler
            t = time
            title = "Euler"

    print("Checking:\n")
    v = V(t)
    i = I(t, x)
    R = [np.mean(v) / np.mean(i)]
    #fig1, _, _ = plot_memristor( v, i, t, f"simulated - {title}" )
    x_old = x[-1]


    for i in range(1,30):
        x_new = solver(dxdt, time, dt, x_old)
        t1 = time
        v1 = V(t)
        i1 = I(t, x_new)
        # plot_memristor(v1, i1, t1, f"simulated - {title}")
        R.append(np.mean(v1) / np.mean(i1))
        x_old = x_new[-1]

    plt.plot(range(1,31), R, "o")
    plt.xlabel("Number of pulses")
    plt.ylabel("Resistance")
    plt.show()
    # make video of simulation
    if args.video:
        try:
            os.mkdir("./videos")
        except:
            pass
        if not os.path.exists(f"./videos/{experiment.name}_{solv}.mp4"):
            with Timer(title="Video"):
                plot_memristor(v, i, t, solv, (10, 4), True, True, f"{experiment.name} - {solv}", True)


