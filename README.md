# Predator-Prey Temperature Dynamics

A mathematical and numerical study of how ocean temperature affects predator-prey population stability.

## Overview

This project models a marine predator-prey system with explicit temperature dependence. We analyze how rising temperature affects equilibrium populations, system stability, and long-term dynamics.

### Key Questions Addressed

- How does temperature affect predator-prey coexistence?
- At what critical temperature do predators go extinct?
- How does the system transition from stable coexistence to predator extinction?

## Model

### System Equations

The predator-prey system is governed by:

$$\frac{dR}{dt} = r(T) R \left(1 - \frac{R}{K}\right) - a_0 R P$$

$$\frac{dP}{dt} = b a_0 R P - d(T) P$$

where:
- **R(t)** = prey density (ind/m³)
- **P(t)** = predator density (ind/m³)
- **T** = temperature (°C) — bifurcation parameter
- **r(T)** = r₀ exp(α_r T) — temperature-dependent prey growth rate
- **d(T)** = d₀ exp(α_d T) — temperature-dependent predator mortality
- **K** = prey carrying capacity
- **a₀** = predator attack rate
- **b** = conversion efficiency

### Parameters

| Parameter | Value | Unit | Description |
|---|---|---|---|
| r₀ | 0.5 | day⁻¹ | Baseline prey growth rate |
| K | 100 | ind/m³ | Prey carrying capacity |
| α_r | 0.02 | °C⁻¹ | Prey growth temperature sensitivity |
| a₀ | 0.01 | day⁻¹ | Predator attack rate |
| b | 0.2 | — | Conversion efficiency |
| d₀ | 0.1 | day⁻¹ | Baseline predator mortality |
| α_d | 0.05 | °C⁻¹ | Predator mortality temperature sensitivity |

## Repository Structure