# Libs >>>
from math import lcm, gcd


# Helpers >>>
def _atomic_composition(chemical_composition: list) -> dict:
    """Calculates the total number of atoms for each element in a chemical composition.

    Takes a list of chemical compounds and counts the total number of atoms for each
    unique element across all compounds in the composition, considering multipliers.

    Args:
        chemical_composition (list): List of dictionaries containing chemical compounds with structure:
            [
                {
                    "decomposition": [{"element": str, "number": int}],
                    "chemical": str,
                    "multiplier": int
                }
            ]

    Returns:
        dict: Dictionary with element symbols as keys and their total atom count as values.
            Example: {"H": 4, "O": 2, "C": 2} for 2(CH2O)

    Example:
        Input: [{"decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}], "multiplier": 2}]
        Output: {"H": 4, "O": 2}
    """
    # Make a var to keep track of the number of atoms of each element
    atomic_composition = {}

    # Iterate over the chemical composition
    for chemical in chemical_composition:
        # Get the multiplier for this chemical compound
        multiplier = chemical.get("multiplier", 1)
        
        # Get the number of atoms of each element
        for element in chemical["decomposition"]:
            # Calculate total atoms considering the multiplier
            total_atoms = element["number"] * multiplier
            
            # If the element is already in the atomic composition, add the number of atoms
            if element["element"] in atomic_composition:
                atomic_composition[element["element"]] += total_atoms
            else:
                atomic_composition[element["element"]] = total_atoms

    # Return the atomic composition
    return atomic_composition


def _calculate_max_attempts(reactants: list, products: list) -> int:
    """
    Dynamically calculates the maximum number of balancing attempts based on the complexity of the equation.

    Args:
        reactants (list): List of reactant compounds.
        products (list): List of product compounds.

    Returns:
        int: The maximum number of balancing attempts, calculated as:
             - Base value of 10
             - Plus 2 for each unique element
             - Plus 1 for each compound
    """
    # Count unique elements
    all_elements = set()
    for chem in reactants + products:
        for elem in chem["decomposition"]:
            all_elements.add(elem["element"])
    
    # Count total compounds
    total_compounds = len(reactants) + len(products)
    
    # Calculate max attempts
    return 10 + (2 * len(all_elements)) + total_compounds


def _balance_elements(reactants: list, products: list) -> dict:
    """
    Balances a chemical equation by adjusting the coefficients of reactants and products.

    The function uses an iterative approach to balance the equation:
    1. Calculates the total number of atoms for each element on both sides.
    2. Determines the least common multiple (LCM) of atom counts for each element.
    3. Adjusts coefficients to balance the equation.
    4. Repeats until the equation is balanced or the maximum number of attempts is reached.

    Args:
        reactants (list): List of reactant compounds, where each compound is a dictionary with:
            - "decomposition": List of dictionaries with "element" and "number" keys.
            - "chemical": The chemical formula as a string.
            - "multiplier": The current coefficient for the compound.
        products (list): List of product compounds, with the same structure as reactants.

    Returns:
        dict: A dictionary with balanced coefficients for reactants and products:
            - "reactants": Updated list of reactants with balanced coefficients.
            - "products": Updated list of products with balanced coefficients.

    Raises:
        ValueError: If an element is missing from one side of the equation or if balancing fails.

    """
    # Dynamically calculate max attempts based on equation complexity
    MAX_ATTEMPTS = _calculate_max_attempts(reactants, products)

    for attempt in range(MAX_ATTEMPTS):
        # Get current atom counts for reactants and products
        reactants_comp = _atomic_composition(reactants)
        products_comp = _atomic_composition(products)
        
        # Check if the equation is already balanced
        if reactants_comp == products_comp:
            break
        
        # Create a processing order for elements, starting with those in the fewest compounds
        all_elements = set(reactants_comp.keys()).union(products_comp.keys())
        element_order = sorted(
            all_elements,
            key=lambda e: sum(1 for chem in reactants + products 
                            if any(el["element"] == e for el in chem["decomposition"]))
        )

        # Balance each element in the determined order
        for element in element_order:
            # Get current atom counts for this element
            r_count = reactants_comp.get(element, 0)
            p_count = products_comp.get(element, 0)
            
            # Skip if the element is already balanced
            if r_count == p_count:
                continue
                
            # Raise an error if an element is missing from one side
            if r_count == 0 or p_count == 0:
                raise ValueError(f"Element {element} is missing from one side of the equation.")

            # Calculate the least common multiple (LCM) of the atom counts
            balance_factor = lcm(r_count, p_count)
            
            # Determine the required multipliers for reactants and products
            r_mult = balance_factor // r_count
            p_mult = balance_factor // p_count

            # Apply multipliers to all compounds containing this element
            for chem in reactants:
                if any(e["element"] == element for e in chem["decomposition"]):
                    chem["multiplier"] *= r_mult
                    
            for chem in products:
                if any(e["element"] == element for e in chem["decomposition"]):
                    chem["multiplier"] *= p_mult

            # Recalculate atom counts after adjustments
            reactants_comp = _atomic_composition(reactants)
            products_comp = _atomic_composition(products)

    # Simplify coefficients by dividing by their greatest common divisor (GCD)
    all_coeffs = [chem["multiplier"] for chem in reactants + products]
    common_gcd = gcd(*all_coeffs)
    if common_gcd > 1:
        for chem in reactants + products:
            chem["multiplier"] //= common_gcd

    # Return the balanced equation
    return {"reactants": reactants, "products": products}

# Main >>>
def balance_formula(chemical_composition: dict) -> dict:
    """
    Balances a chemical equation by finding the appropriate coefficients for all reactants and products.

    This function serves as the main entry point for chemical equation balancing. It extracts the reactants 
    and products from the input dictionary and delegates the actual balancing to the _balance_elements helper function.

    Args:
        chemical_composition (dict): A dictionary containing the chemical equation components with structure:
            {
                "reactants": [
                    {
                        "decomposition": [{"element": str, "number": int}],
                        "chemical": str,
                        "multiplier": int
                    }
                ],
                "products": [
                    {
                        "decomposition": [{"element": str, "number": int}],
                        "chemical": str,
                        "multiplier": int
                    }
                ]
            }

    Returns:
        dict: A dictionary containing the balanced chemical equation with updated multipliers:
            {
                "reactants": [list of balanced reactants],
                "products": [list of balanced products]
            }

    Raises:
        ValueError: If an element is missing from one side of the equation or if balancing fails.
    """
    # Balance the elements + return the balanced elements
    return _balance_elements(chemical_composition["reactants"], chemical_composition["products"])
