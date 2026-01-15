"""
Main orchestrator for temperature-dependent predator-prey model analysis.
Runs all phases: simulations, bifurcation analysis, and figure generation.
"""

import sys
import time
from config import print_parameters
from simulations import main as run_simulations
from plotting import main as run_plotting

def main():
    """Execute complete analysis pipeline."""
    
    print("\n" + "="*70)
    print("TEMPERATURE-DEPENDENT PREDATOR-PREY SYSTEM")
    print("Complete Analysis Pipeline")
    print("="*70)
    
    # Print parameter summary
    print_parameters()
    
    # Measure total execution time
    start_time = time.time()
    
    try:
        # Numerical simulations
        run_simulations()
        
        # Visualization
        run_plotting()
        
        # Completion message
        elapsed_time = time.time() - start_time
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nTotal execution time: {elapsed_time:.2f} seconds")
        print("\nOutput files:")
        print("  Data: data/scenario_T*.csv, data/bifurcation.csv")
        print("  Figures: figures/*.png")
        print("\n" + "="*70 + "\n")
        
        return 0
    
    except Exception as e:
        print("\n" + "="*70)
        print("ERROR OCCURRED")
        print("="*70)
        print(f"\nError message: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)