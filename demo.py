#!/usr/bin/env python3
"""
Gravity Contraction Hypothesis - Simple 1D Demonstration

This script demonstrates the core concept: gravity as local space contraction
rather than interaction between objects.

Requirements: numpy, matplotlib (install with: pip install -r requirements.txt)
"""

try:
    import numpy as np
    import matplotlib.pyplot as plt
    VISUALIZATION_AVAILABLE = True
except ImportError:
    print("Note: numpy and matplotlib not available. Install with: pip install -r requirements.txt")
    print("Continuing with text-based demonstration only.\n")
    VISUALIZATION_AVAILABLE = False
    # Create minimal numpy-like functions for demo
    class np:
        @staticmethod
        def linspace(start, stop, num):
            step = (stop - start) / (num - 1)
            return [start + i * step for i in range(num)]
        
        @staticmethod
        def zeros(num):
            return [0.0] * num
        
        @staticmethod
        def sqrt(x):
            return x ** 0.5
        
        @staticmethod
        def max(x, y):
            return x if x > y else y


class LocalContractionField:
    """
    Represents a 1D space with local contractions.
    
    Each point in space has an independent contraction value that depends
    only on the local mass-energy density. Objects move through this
    contracted space following geodesics.
    """
    
    def __init__(self, num_points=1000, length=10.0):
        """
        Initialize the contraction field.
        
        Args:
            num_points: Number of discrete points in space
            length: Total length of the 1D space
        """
        self.num_points = num_points
        self.length = length
        self.dx = length / num_points
        self.positions = np.linspace(0, length, num_points)
        
        # Local contraction at each point (initially zero)
        self.contraction = np.zeros(num_points)
        
    def add_mass(self, position, mass, G=1.0):
        """
        Add a mass, which creates LOCAL contractions at each point.
        
        Note: This is NOT the mass "pulling" on other points. Instead,
        each point independently calculates its local contraction based
        on the mass-energy distribution.
        
        Args:
            position: Location of the mass
            mass: Mass value
            G: Gravitational constant (default 1.0 for demonstration)
        """
        # Each point calculates its own local contraction
        # In Newtonian limit: Φ(x) ∝ -GM/|x - x_mass|
        for i in range(self.num_points):
            distance = abs(self.positions[i] - position)
            if distance > self.dx:  # Avoid singularity
                # Local contraction at this point due to mass
                self.contraction[i] += -G * mass / distance
                
    def get_contracted_distance(self, x1, x2):
        """
        Calculate the actual distance between two points accounting
        for local space contractions.
        
        The distance is NOT constant - it depends on the contraction
        of space between the points.
        """
        idx1 = int(x1 / self.dx)
        idx2 = int(x2 / self.dx)
        
        if idx1 > idx2:
            idx1, idx2 = idx2, idx1
            
        # Integrate through contracted space
        contracted_dist = 0.0
        for i in range(idx1, idx2):
            # Local metric factor (1 + contraction)
            # In contracted space, distances are modified
            metric_factor = 1.0 + self.contraction[i] / (3e8**2)  # c^2 normalization
            contracted_dist += self.dx * np.sqrt(max(0.01, metric_factor))
            
        return contracted_dist
    
    def get_geodesic_acceleration(self, position):
        """
        Calculate acceleration at a position by following the geodesic
        through contracted space.
        
        This is NOT a force from another object - it's the natural
        path through contracted geometry.
        """
        idx = int(position / self.dx)
        if idx <= 0 or idx >= self.num_points - 1:
            return 0.0
            
        # Gradient of contraction field gives geodesic curvature
        contraction_gradient = (self.contraction[idx + 1] - self.contraction[idx - 1]) / (2 * self.dx)
        
        # Acceleration along geodesic (in Newtonian limit)
        return contraction_gradient
        

def demonstrate_concept():
    """
    Demonstrate the gravity contraction hypothesis with a simple example.
    """
    print("=" * 70)
    print("GRAVITY CONTRACTION HYPOTHESIS - 1D DEMONSTRATION")
    print("=" * 70)
    print()
    print("Key Concept: Gravity is NOT an interaction between objects.")
    print("             Gravity is LOCAL contraction at each point in space.")
    print()
    
    # Create a 1D space
    field = LocalContractionField(num_points=1000, length=10.0)
    
    # Add two masses - each creates LOCAL contractions
    print("Adding two masses to the space...")
    print("- Mass 1: position = 3.0, mass = 5.0")
    print("- Mass 2: position = 7.0, mass = 5.0")
    print()
    
    field.add_mass(position=3.0, mass=5.0)
    field.add_mass(position=7.0, mass=5.0)
    
    print("Important: Each mass does NOT 'pull' on the other!")
    print("Instead: Each point in space calculates its own local contraction.")
    print()
    
    # Show local contractions at different points
    print("Local Space Contractions at Various Points:")
    print("-" * 70)
    test_positions = [0.0, 2.5, 3.0, 5.0, 7.0, 9.5]
    for pos in test_positions:
        idx = int(pos / field.dx)
        if 0 <= idx < field.num_points:
            contraction = field.contraction[idx]
            print(f"  Position {pos:.1f}: contraction = {contraction:.6f}")
    print()
    
    # Calculate geodesic acceleration
    print("Geodesic Accelerations (motion through contracted space):")
    print("-" * 70)
    test_positions = [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    for pos in test_positions:
        accel = field.get_geodesic_acceleration(pos)
        print(f"  Position {pos:.1f}: acceleration = {accel:.6f}")
    print()
    
    print("Notice: Objects between the masses accelerate toward each other,")
    print("        NOT because of mutual force, but because they follow")
    print("        geodesics through independently contracted space!")
    print()
    
    # Visualize
    if VISUALIZATION_AVAILABLE:
        try:
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Plot contraction field
            ax1.plot(field.positions, field.contraction, 'b-', linewidth=2)
            ax1.axvline(3.0, color='r', linestyle='--', label='Mass 1')
            ax1.axvline(7.0, color='g', linestyle='--', label='Mass 2')
            ax1.set_xlabel('Position in Space')
            ax1.set_ylabel('Local Contraction Φ(x)')
            ax1.set_title('Local Space Contraction at Each Point')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot geodesic acceleration
            accelerations = [field.get_geodesic_acceleration(pos) for pos in field.positions]
            ax2.plot(field.positions, accelerations, 'purple', linewidth=2)
            ax2.axvline(3.0, color='r', linestyle='--', label='Mass 1')
            ax2.axvline(7.0, color='g', linestyle='--', label='Mass 2')
            ax2.axhline(0, color='k', linestyle='-', linewidth=0.5)
            ax2.set_xlabel('Position in Space')
            ax2.set_ylabel('Geodesic Acceleration')
            ax2.set_title('Acceleration Following Geodesics (NOT force between masses)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('gravity_contraction_demo.png', dpi=150, bbox_inches='tight')
            print("Visualization saved to: gravity_contraction_demo.png")
            print()
        except Exception as e:
            print(f"Could not create visualization: {e}")
            print()
    else:
        print("Visualization skipped (numpy/matplotlib not installed)")
        print()
    
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print("The apparent 'attraction' between masses is actually the emergent")
    print("behavior of objects following geodesics through space that has been")
    print("locally contracted at each point. No interaction occurs between the")
    print("objects themselves - only local contractions at each point in space.")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_concept()
