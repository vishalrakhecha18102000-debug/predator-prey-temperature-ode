"""
Figure generation for time-series, phase portraits, and bifurcation diagrams.
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from config import (
    temperatures_scenarios, data_dir, figures_dir,
    timeseries_figure, phase_portraits_figure, bifurcation_figure,
    stability_metrics_figure, K, Tc, scenario_filenames,
    bifurcation_filename, plot_t_end, R_max_plot, P_max_plot,
    T_plot_min, T_plot_max
)
from analysis import equilibrium_coexistence, stability_coexistence

def load_scenario_data(filename):
    """Load scenario data from CSV."""
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    t = data[:, 0]
    R = data[:, 1]
    P = data[:, 2]
    return t, R, P

def load_bifurcation_data(filename):
    """Load bifurcation data from CSV."""
    data = np.loadtxt(filename, delimiter=',', skiprows=1)
    T = data[:, 0]
    R_eq = data[:, 1]
    P_eq = data[:, 2]
    exists = data[:, 3].astype(bool)
    return T, R_eq, P_eq, exists

def plot_timeseries():
    """Create 2x2 subplot of time-series for 4 temperature scenarios."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, (T, filename) in enumerate(zip(temperatures_scenarios, scenario_filenames)):
        ax = axes[i]
        
        # Load data
        t, R, P = load_scenario_data(filename)
        
        # Plot
        ax.plot(t, R, 'b-', linewidth=2, label='Prey (R)')
        ax.plot(t, P, 'r-', linewidth=2, label='Predator (P)')
        
        # Labels and formatting
        ax.set_xlabel('Time (days)', fontsize=10)
        ax.set_ylabel('Population Density (ind/m³)', fontsize=10)
        ax.set_title(f'T = {T}°C', fontsize=11, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)
        ax.set_xlim([0, plot_t_end])
    
    plt.tight_layout()
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(timeseries_figure, dpi=300, bbox_inches='tight')
    print(f"Saved: {timeseries_figure}")
    plt.close()

def plot_phase_portraits():
    """Create 1x4 subplot of phase portraits for 4 temperature scenarios."""
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    
    for i, (T, filename) in enumerate(zip(temperatures_scenarios, scenario_filenames)):
        ax = axes[i]
        
        # Load data
        t, R, P = load_scenario_data(filename)
        
        # Plot trajectory
        ax.plot(R, P, 'b-', linewidth=1.5, alpha=0.7, label='Trajectory')
        ax.plot(R[0], P[0], 'go', markersize=8, label='Initial condition')
        ax.plot(R[-1], P[-1], 'r*', markersize=15, label='Final state')
        
        # Plot equilibrium if it exists
        eq = equilibrium_coexistence(T)
        if eq is not None:
            ax.plot(eq[0], eq[1], 'k+', markersize=12, markeredgewidth=2, label='Equilibrium')
        else:
            ax.plot(K, 0, 'kx', markersize=10, markeredgewidth=2, label='Prey-only eq.')
        
        # Labels and formatting
        ax.set_xlabel('Prey (R, ind/m³)', fontsize=10)
        ax.set_ylabel('Predator (P, ind/m³)', fontsize=10)
        ax.set_title(f'T = {T}°C', fontsize=11, fontweight='bold')
        ax.set_xlim([0, R_max_plot])
        ax.set_ylim([0, P_max_plot])
        ax.grid(True, alpha=0.3)
        if i == 0:
            ax.legend(fontsize=8, loc='upper right')
    
    plt.tight_layout()
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(phase_portraits_figure, dpi=300, bbox_inches='tight')
    print(f"Saved: {phase_portraits_figure}")
    plt.close()

def plot_bifurcation():
    """Create 1x2 subplot of bifurcation diagram (R* and P* vs T)."""
    # Load bifurcation data
    T_bifurc, R_eq, P_eq, exists = load_bifurcation_data(bifurcation_filename)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot R* vs T
    ax = axes[0]
    mask_exist = exists
    mask_no_exist = ~exists
    ax.plot(T_bifurc[mask_exist], R_eq[mask_exist], 'b-', linewidth=2.5, label='Coexistence exists')
    ax.axvline(Tc, color='red', linestyle='--', linewidth=2, label=f'Critical T = {Tc:.2f}°C')
    ax.set_xlabel('Temperature (°C)', fontsize=11)
    ax.set_ylabel('Prey Equilibrium R* (ind/m³)', fontsize=11)
    ax.set_title('Bifurcation Diagram: Prey Population', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_xlim([T_plot_min, T_plot_max])
    
    # Plot P* vs T
    ax = axes[1]
    ax.plot(T_bifurc[mask_exist], P_eq[mask_exist], 'r-', linewidth=2.5, label='Coexistence exists')
    ax.axvline(Tc, color='red', linestyle='--', linewidth=2, label=f'Critical T = {Tc:.2f}°C')
    ax.set_xlabel('Temperature (°C)', fontsize=11)
    ax.set_ylabel('Predator Equilibrium P* (ind/m³)', fontsize=11)
    ax.set_title('Bifurcation Diagram: Predator Population', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_xlim([T_plot_min, T_plot_max])
    
    plt.tight_layout()
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(bifurcation_figure, dpi=300, bbox_inches='tight')
    print(f"Saved: {bifurcation_figure}")
    plt.close()

def plot_stability_metrics():
    """Create 1x2 subplot of stability metrics (eigenvalues and trace-determinant)."""
    # Compute stability metrics over temperature range
    T_range = np.linspace(10, 25, 50)
    tau_array = []
    delta_array = []
    lambda1_array = []
    lambda2_array = []
    
    for T in T_range:
        result = stability_coexistence(T)
        if result is not None:
            tau, delta, lambda1, lambda2, _ = result
            tau_array.append(tau)
            delta_array.append(delta)
            lambda1_array.append(lambda1.real)
            lambda2_array.append(lambda2.real)
        else:
            tau_array.append(np.nan)
            delta_array.append(np.nan)
            lambda1_array.append(np.nan)
            lambda2_array.append(np.nan)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot eigenvalues vs T
    ax = axes[0]
    ax.plot(T_range, lambda1_array, 'b-', linewidth=2, label='λ₁ (real part)')
    ax.plot(T_range, lambda2_array, 'r-', linewidth=2, label='λ₂ (real part)')
    ax.axhline(0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(Tc, color='green', linestyle='--', linewidth=2, label=f'Tc = {Tc:.2f}°C')
    ax.set_xlabel('Temperature (°C)', fontsize=11)
    ax.set_ylabel('Eigenvalue', fontsize=11)
    ax.set_title('Stability: Eigenvalues vs Temperature', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    
    # Plot trace-determinant plane
    ax = axes[1]
    ax.plot(tau_array, delta_array, 'b-', linewidth=2.5, label='Coexistence equilibrium')
    ax.axhline(0, color='k', linestyle='-', linewidth=0.5)
    ax.axvline(0, color='k', linestyle='-', linewidth=0.5)
    
    # Shade stability region (τ < 0, Δ > 0)
    tau_fill = np.linspace(-15, 0, 100)
    delta_fill = np.linspace(0, 40, 100)
    ax.fill_between(tau_fill, 0, 40, alpha=0.2, color='green', label='Stable region')
    
    ax.set_xlabel('Trace(J) = τ', fontsize=11)
    ax.set_ylabel('Det(J) = Δ', fontsize=11)
    ax.set_title('Trace-Determinant Plane', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
    ax.set_xlim([-15, 1])
    ax.set_ylim([-5, 40])
    
    plt.tight_layout()
    os.makedirs(figures_dir, exist_ok=True)
    plt.savefig(stability_metrics_figure, dpi=300, bbox_inches='tight')
    print(f"Saved: {stability_metrics_figure}")
    plt.close()

def main():
    """Generate all figures."""
    print("\n" + "="*70)
    print("VISUALIZATION")
    print("="*70 + "\n")
    
    plot_timeseries()
    plot_phase_portraits()
    plot_bifurcation()
    plot_stability_metrics()
    
    print("\n" + "="*70)
    print("FIGURES COMPLETE")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()