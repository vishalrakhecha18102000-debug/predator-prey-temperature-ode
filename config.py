"""
Configuration file for temperature-dependent predator-prey model.
All numerical parameters are defined here.
"""

import numpy as np

# ============================================================================
# MODEL PARAMETERS
# ============================================================================

# Prey parameters
r0 = 0.5                    # day^-1, baseline prey growth rate
K = 100.0                   # individuals/m^3, carrying capacity
alpha_r = 0.02              # °C^-1, prey growth temperature sensitivity

# Predator parameters
a0 = 0.01                   # per predator per day, attack rate
b = 0.2                     # dimensionless, conversion efficiency
d0 = 0.1                    # day^-1, baseline predator mortality
alpha_d = 0.05              # °C^-1, predator mortality temperature sensitivity

# Critical temperature (computed from report)
Tc = (1.0 / alpha_d) * np.log((b * a0 * K) / d0)

# ============================================================================
# SIMULATION PARAMETERS
# ============================================================================

# Temperature scenarios (4 representative temperatures)
temperatures_scenarios = np.array([10.0, 15.0, 20.0, 22.0])  # °C

# Bifurcation analysis temperature range
T_bifurcation_min = 10.0    # °C
T_bifurcation_max = 25.0    # °C
num_bifurcation_points = 200 # Number of temperature points in bifurcation

# ============================================================================
# ODE INTEGRATION PARAMETERS
# ============================================================================

# Initial conditions for time-series
R0_scenarios = 50.0         # individuals/m^3, initial prey density
P0_scenarios = 10.0         # individuals/m^3, initial predator density

# Time span for integration
t_start = 0.0               # days
t_end = 500.0               # days, long enough to reach equilibrium
num_time_points = 5000      # number of output points

# ODE solver parameters (scipy.integrate.solve_ivp with RK45)
max_step = 1.0              # maximum step size for RK45
rtol = 1e-6                 # relative tolerance
atol = 1e-9                 # absolute tolerance

# ============================================================================
# PLOTTING PARAMETERS
# ============================================================================

# Time-series plot
plot_t_start = 0.0          # start plotting from t=0
plot_t_end = 500.0          # end plotting at t=500
plot_t_transient = 100.0    # show transient behavior up to this time

# Phase portrait plot
R_min_plot = 0.0
R_max_plot = K * 1.2        # 120% of carrying capacity
P_min_plot = 0.0
P_max_plot = 30.0

# Bifurcation plot
T_plot_min = 10.0
T_plot_max = 25.0
R_bifurc_min = 0.0
R_bifurc_max = K * 1.2
P_bifurc_min = 0.0
P_bifurc_max = 30.0

# ============================================================================
# OUTPUT PARAMETERS
# ============================================================================

# Data output directory
data_dir = "data"
figures_dir = "figures"

# CSV file names for scenarios
scenario_filenames = [
    f"{data_dir}/scenario_T{int(T)}.csv" 
    for T in temperatures_scenarios
]

# Bifurcation data filename
bifurcation_filename = f"{data_dir}/bifurcation.csv"

# Figure filenames
timeseries_figure = f"{figures_dir}/timeseries.png"
phase_portraits_figure = f"{figures_dir}/phase_portraits.png"
bifurcation_figure = f"{figures_dir}/bifurcation.png"
stability_metrics_figure = f"{figures_dir}/stability_metrics.png"

# ============================================================================
# PRINT SUMMARY
# ============================================================================

def print_parameters():
    """Print a summary of all parameters."""
    print("=" * 70)
    print("TEMPERATURE-DEPENDENT PREDATOR-PREY MODEL PARAMETERS")
    print("=" * 70)
    print("\nPrey Parameters:")
    print(f"  r₀ = {r0} day⁻¹")
    print(f"  K = {K} individuals/m³")
    print(f"  αᵣ = {alpha_r} °C⁻¹")
    print("\nPredator Parameters:")
    print(f"  a₀ = {a0} per predator per day")
    print(f"  b = {b}")
    print(f"  d₀ = {d0} day⁻¹")
    print(f"  αd = {alpha_d} °C⁻¹")
    print("\nCritical Temperature:")
    print(f"  Tc = {Tc:.2f} °C")
    print("\nSimulation Parameters:")
    print(f"  Temperature scenarios: {temperatures_scenarios}")
    print(f"  Bifurcation range: {T_bifurcation_min}–{T_bifurcation_max}°C")
    print(f"  Time integration: {t_start}–{t_end} days")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    print_parameters()