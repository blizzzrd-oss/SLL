"""
Comparison between multiplicative and additive multiplier systems.
This demonstrates why additive bonuses prevent exponential scaling.
"""

def multiplicative_system():
    """The old system where all multipliers are multiplied together."""
    print("=== MULTIPLICATIVE SYSTEM (Old) ===")
    print("Wave 1: Normal Mode (1.0) × Wave 1 (1.0) = 1.0x total")
    print("Wave 2: Normal Mode (1.0) × Wave 2 (1.2) = 1.2x total")
    print("Wave 3: Normal Mode (1.0) × Wave 3 (1.4) = 1.4x total")
    print("Wave 4: Normal Mode (1.0) × Wave 4 (1.7) = 1.7x total")
    print("Wave 5: Normal Mode (1.0) × Wave 5 (2.0) = 2.0x total")
    print()
    
    # With Hard mode and events
    print("Hard Mode Examples:")
    print("Wave 1: Hard Mode (1.2) × Wave 1 (1.0) = 1.2x total")
    print("Wave 2: Hard Mode (1.2) × Wave 2 (1.2) = 1.44x total")
    print("Wave 3: Hard Mode (1.2) × Wave 3 (1.4) = 1.68x total")
    print("Wave 4: Hard Mode (1.2) × Wave 4 (1.7) = 2.04x total")
    print("Wave 5: Hard Mode (1.2) × Wave 5 (2.0) = 2.4x total")
    print()
    
    # With events
    print("With Boss Wave + Event:")
    print("Hard Mode (1.2) × Wave 5 (2.0) × Boss (2.0) × Event (1.5) = 7.2x total!")
    print("This gets CRAZY fast!")
    print()

def additive_system():
    """The new system where bonuses are added together before applying."""
    print("=== ADDITIVE SYSTEM (New) ===")
    print("Wave 1: Normal Mode (+0%) + Wave 1 (+0%) = +0% = 1.0x total")
    print("Wave 2: Normal Mode (+0%) + Wave 2 (+20%) = +20% = 1.2x total")
    print("Wave 3: Normal Mode (+0%) + Wave 3 (+40%) = +40% = 1.4x total")
    print("Wave 4: Normal Mode (+0%) + Wave 4 (+70%) = +70% = 1.7x total")
    print("Wave 5: Normal Mode (+0%) + Wave 5 (+100%) = +100% = 2.0x total")
    print()
    
    # With Hard mode
    print("Hard Mode Examples:")
    print("Wave 1: Hard Mode (+20%) + Wave 1 (+0%) = +20% = 1.2x total")
    print("Wave 2: Hard Mode (+20%) + Wave 2 (+20%) = +40% = 1.4x total")
    print("Wave 3: Hard Mode (+20%) + Wave 3 (+40%) = +60% = 1.6x total")
    print("Wave 4: Hard Mode (+20%) + Wave 4 (+70%) = +90% = 1.9x total")
    print("Wave 5: Hard Mode (+20%) + Wave 5 (+100%) = +120% = 2.2x total")
    print()
    
    # With events
    print("With Boss Wave + Event:")
    print("Hard Mode (+20%) + Wave 5 (+100%) + Boss (+100%) + Event (+50%) = +270% = 3.7x total")
    print("Much more balanced progression!")
    print()

def damage_scaling_comparison():
    """Compare how damage scales over time with both systems."""
    print("=== DAMAGE SCALING COMPARISON ===")
    base_damage = 10
    
    print("Wave | Multiplicative | Additive | Difference")
    print("-" * 45)
    
    # Simulate some complex scenarios
    scenarios = [
        ("Wave 1 Normal", 1.0, 1.0),
        ("Wave 2 Normal", 1.2, 1.2),
        ("Wave 3 Normal", 1.4, 1.4),
        ("Wave 4 Normal", 1.7, 1.7),
        ("Wave 5 Normal", 2.0, 2.0),
        ("Wave 5 Hard", 1.2 * 2.0, 1.0 + 0.2 + 1.0),  # Hard mode + Wave 5
        ("Wave 5 Hard + Boss", 1.2 * 2.0 * 2.0, 1.0 + 0.2 + 1.0 + 1.0),  # + Boss bonus
        ("Wave 5 Hard + Boss + Event", 1.2 * 2.0 * 2.0 * 1.5, 1.0 + 0.2 + 1.0 + 1.0 + 0.5),  # + Event
    ]
    
    for name, mult_factor, add_factor in scenarios:
        mult_damage = base_damage * mult_factor
        add_damage = base_damage * add_factor
        difference = mult_damage - add_damage
        print(f"{name:<15} | {mult_damage:>10.1f} | {add_damage:>8.1f} | {difference:>+9.1f}")

if __name__ == "__main__":
    multiplicative_system()
    additive_system()
    damage_scaling_comparison()
