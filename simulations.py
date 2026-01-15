"""
ODE integration and bifurcation analysis.
"""

import numpy as np
from scipy.integrate import solve_ivp
import os
from config import (
    temperatures_scenarios, T_bifurcation_min, T_bifurcation_max,
    num_bifurcation_points, t_start, t_end, num_time_points,
    R0_scenarios, P0_scenarios, rtol, atol, max_step,
    data_dir, scenario_filenames, bifurcation_filename
)
from model import ode_system_wrapper
from analysis import equilibrium_coexistence

def integrate_ode(T, R0, P0):
    """
    Integrate ODE system from initial conditions (R0, P0) at temperature T.
    
    Parameters:
    -----------
    T : float
        Temperature (°C)
    R0 : float
        Initial prey density
    P0 : float
        Initial predator density
    
    Returns:
    --------
    t : array
        Time points
    R : array
        Prey density at each time
    P : array
        Predator density at each time
    """
    # Time points for output
    t_eval = np.linspace(t_start, t_end, num_time_points)
    
    # Solve ODE
    y0 = [R0, P0]
    
    def ode_func(t, y):
        return ode_system_wrapper(t, y, T)
    
    sol = solve_ivp(ode_func, (t_start, t_end), y0, t_eval=t_eval,
                    method='RK45', dense_output=True,
                    max_step=max_step, rtol=rtol, atol=atol)
    
    return sol.t, sol.y[0], sol.y[1]  # t, R, P

def run_scenario_simulations():
    """
    Run 4 scenario simulations at different temperatures.
    Save results to CSV files.
    """
    print("\n" + "="*70)
    print("NUMERICAL SIMULATIONS")
    print("="*70)
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    for i, T in enumerate(temperatures_scenarios):
        print(f"\nRunning simulation {i+1}/4: T = {T}°C...")
        
        # Integrate ODE
        t, R, P = integrate_ode(T, R0_scenarios, P0_scenarios)
        
        # Save to CSV
        filename = scenario_filenames[i]
        data = np.column_stack([t, R, P])
        np.savetxt(filename, data, delimiter=',', 
                   header='time(days),prey(ind/m3),predator(ind/m3)',
                   comments='')
        
        print(f"  Saved to {filename}")
        print(f"  Final state: R = {R[-1]:.2f}, P = {P[-1]:.2f}")

def run_bifurcation_analysis():
    """
    Compute bifurcation diagram over temperature range.
    Save equilibrium populations as function of temperature.
    """
    print("\n" + "="*70)
    print("BIFURCATION ANALYSIS")
    print("="*70)
    
    # Temperature array
    T_array = np.linspace(T_bifurcation_min, T_bifurcation_max, 
                         num_bifurcation_points)
    
    # Arrays to store results
    R_bifurc = np.zeros_like(T_array)
    P_bifurc = np.zeros_like(T_array)
    exists_bifurc = np.ones_like(T_array, dtype=bool)  # True if coexistence exists
    
    print(f"\nComputing equilibria over T ∈ [{T_bifurcation_min}, {T_bifurcation_max}]°C...")
    print(f"Number of temperature points: {num_bifurcation_points}")
    
    for i, T in enumerate(T_array):
        eq = equilibrium_coexistence(T)
        
        if eq is not None:
            R_bifurc[i] = eq[0]
            P_bifurc[i] = eq[1]
            exists_bifurc[i] = True
        else:
            R_bifurc[i] = np.nan
            P_bifurc[i] = np.nan
            exists_bifurc[i] = False
    
    # Save bifurcation data
    os.makedirs(data_dir, exist_ok=True)
    bifurc_data = np.column_stack([T_array, R_bifurc, P_bifurc, exists_bifurc])
    np.savetxt(bifurcation_filename, bifurc_data, delimiter=',',
               header='temperature(C),prey_equilibrium(ind/m3),predator_equilibrium(ind/m3),coexistence_exists',
               comments='')
    
    print(f"Saved to {bifurcation_filename}")
    
    # Print summary
    num_coexist = np.sum(exists_bifurc)
    num_no_coexist = np.sum(~exists_bifurc)
    
    print(f"\nBifurcation Summary:")
    print(f"  Temperature range: {T_bifurcation_min}–{T_bifurcation_max}°C")
    print(f"  Points with coexistence: {num_coexist}/{num_bifurcation_points}")
    print(f"  Points without coexistence: {num_no_coexist}/{num_bifurcation_points}")
    
    return T_array, R_bifurc, P_bifurc, exists_bifurc

def main():
    """Run all simulations."""
    # Run scenario simulations
    run_scenario_simulations()
    
    # Run bifurcation analysis
    T_array, R_bifurc, P_bifurc, exists = run_bifurcation_analysis()
    
    print("\n" + "="*70)
    print("SIMULATIONS COMPLETE")
    print("="*70 + "\n")
    
    return T_array, R_bifurc, P_bifurc, exists

if __name__ == "__main__":
    main()