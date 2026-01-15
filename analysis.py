"""
Equilibrium analysis and stability calculations.
"""

import numpy as np
from scipy.optimize import fsolve
from config import r0, alpha_r, K, a0, b, d0, alpha_d, Tc
from model import r_temp, d_temp

def equilibrium_coexistence(T):
    """
    Compute coexistence equilibrium (R*, P*) at temperature T.
    Returns None if coexistence does not exist.
    
    From report: coexistence exists if d(T) < b*a0*K
    R* = d(T) / (b*a0)
    P* = r(T)/a0 * (1 - R*/K)
    """
    d = d_temp(T)
    
    # Check existence condition
    if d >= b * a0 * K:
        return None  # Coexistence does not exist
    
    # Compute R*
    R_star = d / (b * a0)
    
    # Compute P*
    P_star = (r_temp(T) / a0) * (1 - R_star / K)
    
    if P_star <= 0:
        return None
    
    return np.array([R_star, P_star])

def equilibrium_prey_only(T):
    """
    Prey-only equilibrium: (K, 0)
    Always exists.
    """
    return np.array([K, 0.0])

def equilibrium_extinction(T):
    """
    Extinction equilibrium: (0, 0)
    Always exists.
    """
    return np.array([0.0, 0.0])

def jacobian_general(R, P, T):
    """
    Compute Jacobian matrix at arbitrary point (R, P).
    From report equation (33):
    
    J = [[r(T)*(1 - 2R/K) - a0*P,    -a0*R        ],
         [b*a0*P,                     b*a0*R - d(T)]]
    """
    r = r_temp(T)
    d = d_temp(T)
    
    J11 = r * (1 - 2*R/K) - a0*P
    J12 = -a0 * R
    J21 = b * a0 * P
    J22 = b * a0 * R - d
    
    return np.array([[J11, J12], [J21, J22]])

def jacobian_coexistence(T):
    """
    Compute Jacobian at coexistence equilibrium.
    From report equation (45):
    
    J = [[-r(T)*R*/K,     -a0*R*],
         [b*a0*P*,        0     ]]
    """
    eq = equilibrium_coexistence(T)
    if eq is None:
        return None
    
    R_star, P_star = eq
    r = r_temp(T)
    
    J11 = -r * R_star / K
    J12 = -a0 * R_star
    J21 = b * a0 * P_star
    J22 = 0.0
    
    return np.array([[J11, J12], [J21, J22]])

def stability_coexistence(T):
    """
    Classify stability at coexistence using trace-determinant criterion.
    Returns: (tau, delta, eigenvalues, classification)
    
    tau = trace(J) = J11 + J22
    delta = det(J) = J11*J22 - J12*J21
    
    Returns: (tau, delta, lambda1, lambda2, stability_type)
    """
    J = jacobian_coexistence(T)
    if J is None:
        return None
    
    tau = np.trace(J)
    delta = np.linalg.det(J)
    
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvals(J)
    lambda1, lambda2 = sorted(eigenvalues, key=lambda x: x.real, reverse=True)
    
    # Classify stability
    if delta < 0:
        stability = "saddle"
    elif delta > 0 and tau < 0:
        stability = "stable"
    elif delta > 0 and tau > 0:
        stability = "unstable"
    elif delta > 0 and np.isclose(tau, 0):
        stability = "center"
    else:
        stability = "unknown"
    
    return tau, delta, lambda1, lambda2, stability

def equilibrium_summary(T):
    """
    Print summary of all equilibria and their stability at temperature T.
    """
    print(f"\n{'='*70}")
    print(f"EQUILIBRIUM ANALYSIS AT T = {T}°C")
    print(f"{'='*70}")
    
    # Extinction
    eq_ext = equilibrium_extinction(T)
    print(f"\n1. Extinction: {eq_ext}")
    
    # Prey-only
    eq_prey = equilibrium_prey_only(T)
    print(f"2. Prey-only: {eq_prey}")
    
    # Coexistence
    eq_coex = equilibrium_coexistence(T)
    if eq_coex is not None:
        print(f"3. Coexistence: R* = {eq_coex[0]:.4f}, P* = {eq_coex[1]:.4f}")
        result = stability_coexistence(T)
        if result is not None:
            tau, delta, lambda1, lambda2, stab = result
            print(f"   Stability: {stab} (tau={tau:.4f}, det={delta:.4f})")
            print(f"   Eigenvalues: λ₁={lambda1:.4f}, λ₂={lambda2:.4f}")
    else:
        print(f"3. Coexistence: Does not exist (d(T) >= b*a0*K)")
    
    print(f"\nCritical temperature: Tc = {Tc:.2f}°C")
    if T < Tc:
        print(f"Status: T < Tc → Coexistence is stable")
    elif T > Tc:
        print(f"Status: T > Tc → Coexistence does not exist, only prey-only is stable")
    else:
        print(f"Status: T = Tc → Bifurcation point")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    # Test equilibrium calculations at 3 temperatures
    temperatures_test = [10.0, 13.86, 20.0]
    for T in temperatures_test:
        equilibrium_summary(T)