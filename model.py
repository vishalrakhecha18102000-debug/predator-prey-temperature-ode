"""
ODE system definition for temperature-dependent predator-prey model.
"""

import numpy as np
from config import r0, alpha_r, K, a0, b, d0, alpha_d

def r_temp(T):
    """Temperature-dependent prey growth rate."""
    return r0 * np.exp(alpha_r * T)

def d_temp(T):
    """Temperature-dependent predator mortality rate."""
    return d0 * np.exp(alpha_d * T)

def ode_system(t, y, T):
    """
    ODE system for temperature-dependent predator-prey dynamics.
    
    Parameters:
    -----------
    t : float
        Time (days)
    y : array
        State vector [R, P] where:
        - R: prey density (individuals/m^3)
        - P: predator density (individuals/m^3)
    T : float
        Temperature (°C)
    
    Returns:
    --------
    dydt : array
        Time derivatives [dR/dt, dP/dt]
    
    Equations:
    ----------
    dR/dt = r(T) * R * (1 - R/K) - a0 * R * P
    dP/dt = b * a0 * R * P - d(T) * P
    """
    R, P = y
    
    # Temperature-dependent rates
    r = r_temp(T)
    d = d_temp(T)
    
    # Prey dynamics: logistic growth - predation
    dR_dt = r * R * (1 - R / K) - a0 * R * P
    
    # Predator dynamics: reproduction from predation - mortality
    dP_dt = b * a0 * R * P - d * P
    
    return np.array([dR_dt, dP_dt])

def ode_system_wrapper(t, y, T):
    """
    Wrapper for scipy.integrate.solve_ivp (returns array).
    """
    return ode_system(t, y, T)

if __name__ == "__main__":
    # Test the ODE system at a single temperature
    print("Testing ODE system at T = 15°C...")
    T_test = 15.0
    R_test = 50.0
    P_test = 10.0
    y_test = np.array([R_test, P_test])
    
    dydt_test = ode_system(0, y_test, T_test)
    print(f"At (R, P) = ({R_test}, {P_test}) and T = {T_test}°C:")
    print(f"  dR/dt = {dydt_test[0]:.4f} individuals/m³/day")
    print(f"  dP/dt = {dydt_test[1]:.4f} individuals/m³/day")
    print(f"  r(T) = {r_temp(T_test):.4f} day⁻¹")
    print(f"  d(T) = {d_temp(T_test):.4f} day⁻¹")