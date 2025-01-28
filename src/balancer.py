# Libs >>>
from math import lcm, gcd


# Helpers >>>
def _atomic_composition(chemical_composition: list) -> dict:
    """Calculates the total number of atoms for each element in a chemical composition.

    Takes a list of chemical compounds and counts the total number of atoms for each
    unique element across all compounds in the composition.

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
            Example: {"H": 2, "O": 1, "C": 1}

    Example:
        Input: [{"decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}]}]
        Output: {"H": 2, "O": 1}
    """
    # Make a var to keep track of the number of atoms of each element
    atomic_composition = {}

    # Iterate over the chemical composition
    for chemical in chemical_composition:
        # Get the number of atoms of each element
        for element in chemical["decomposition"]:
            # If the element is already in the atomic composition, add the number of atoms
            if element["element"] in atomic_composition:
                atomic_composition[element["element"]] += element["number"]
            else:
                atomic_composition[element["element"]] = element["number"]

    # Return the atomic composition
    return atomic_composition


def _atomic_lcm(
    reactants_composition: dict, products_composition: dict, raise_error: bool = True
) -> dict:
    """Calculates the least common multiple (LCM) of atom counts between reactants and products.

    Takes dictionaries of element counts from reactants and products and calculates the LCM
    for each element to help determine balanced equation coefficients.

    Args:
        reactants_composition (dict): Dictionary of element counts in reactants
            Example: {"H": 2, "O": 1}
        products_composition (dict): Dictionary of element counts in products
            Example: {"H": 2, "O": 1}
        raise_error (bool, optional): Whether to raise error if elements don't match. Defaults to True.

    Returns:
        dict: Dictionary with elements as keys and their LCM values as values
            Example: {"H": 2, "O": 1}

    Raises:
        SystemExit: If elements in reactants and products don't match and raise_error is True

    Example:
        Input:
            reactants = {"N": 2, "O": 2}
            products = {"N": 2, "O": 1}
        Output: {"N": 2, "O": 2}
    """
    # Check if all the elements in the reactants and products are the same
    if reactants_composition.keys() != products_composition.keys():
        if raise_error:
            raise SystemExit(
                "The elements in the reactants and products are not the same"
            )
        return {}

    # Make a var to hold the least common multiple
    atomic_lcms = {}

    # Find the least common multiple of the number of atoms of each element
    for element in reactants_composition:
        atomic_lcms[element] = lcm(
            reactants_composition[element], products_composition[element]
        )

    # Return the least common multiple
    return atomic_lcms


def _balance_elements(reactants: list, products: list, atomic_lcms: dict) -> dict:
    """
    Balances the chemical equation by adjusting the multipliers of reactants and products
    to ensure the number of atoms for each element is equal on both sides of the equation.

    The function works in two main steps:
    1. **Balancing Single Elements**: For elements that appear in exactly one reactant and one product,
       it calculates the necessary multipliers to balance the atom counts using the greatest common divisor (GCD).
       This ensures that elements present in single chemicals are balanced first, simplifying the overall process.

    2. **Fallback Balancing**: If elements are still unbalanced after the first step, the function uses a fallback method
       to adjust multipliers based on the remaining unbalanced elements. This ensures that all elements are balanced,
       even if they appear in multiple chemicals.

    Args:
        reactants (list): A list of dictionaries representing the reactants, where each dictionary contains:
            - "decomposition": A list of dictionaries with "element" and "number" keys representing the atoms.
            - "chemical": The chemical formula as a string.
            - "multiplier": An integer representing the current multiplier for the chemical.

        products (list): A list of dictionaries representing the products, with the same structure as reactants.

        atomic_lcms (dict): A dictionary containing the least common multiple (LCM) of atom counts for each element
            in the reactants and products. Keys are element symbols, and values are the LCMs.

    Returns:
        dict: A dictionary with two keys:
            - "reactants": The updated list of reactants with adjusted multipliers.
            - "products": The updated list of products with adjusted multipliers.

    Example:
        Input:
            reactants = [
                {
                    "decomposition": [{"element": "N", "number": 2}, {"element": "H", "number": 8}],
                    "chemical": "(NH4)2Cr2O7",
                    "multiplier": 1,
                }
            ],
            products = [
                {
                    "decomposition": [{"element": "N", "number": 2}],
                    "chemical": "N2",
                    "multiplier": 1,
                },
                {
                    "decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}],
                    "chemical": "H2O",
                    "multiplier": 1,
                },
            ],
            atomic_lcms = {"N": 2, "H": 8, "O": 1}

        Output:
            {
                "reactants": [
                    {
                        "decomposition": [{"element": "N", "number": 2}, {"element": "H", "number": 8}],
                        "chemical": "(NH4)2Cr2O7",
                        "multiplier": 1,
                    }
                ],
                "products": [
                    {
                        "decomposition": [{"element": "N", "number": 2}],
                        "chemical": "N2",
                        "multiplier": 1,
                    },
                    {
                        "decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}],
                        "chemical": "H2O",
                        "multiplier": 4,
                    },
                ],
            }
    """

    # Function to handle elements present in exactly one reactant and one product
    def balance_single_elements():
        """
        Balances elements that appear in exactly one reactant and one product.
        For each such element, it calculates the necessary multipliers to balance the atom counts
        using the greatest common divisor (GCD) to find the minimal multipliers.
        """
        for element in atomic_lcms:
            # Find all reactants and products that contain the current element
            reactant_chems = [
                chem
                for chem in reactants
                if any(e["element"] == element for e in chem["decomposition"])
            ]
            product_chems = [
                chem
                for chem in products
                if any(e["element"] == element for e in chem["decomposition"])
            ]

            # If the element appears in exactly one reactant and one product, balance it
            if len(reactant_chems) == 1 and len(product_chems) == 1:
                reactant_chem = reactant_chems[0]
                product_chem = product_chems[0]

                # Get the specific element counts in the reactant and product
                reactant_elem = next(
                    e for e in reactant_chem["decomposition"] if e["element"] == element
                )
                product_elem = next(
                    e for e in product_chem["decomposition"] if e["element"] == element
                )

                # Calculate the total number of atoms for the element in the reactant and product
                a = reactant_elem["number"] * reactant_chem["multiplier"]
                b = product_elem["number"] * product_chem["multiplier"]

                # Skip if either count is zero or if they are already balanced
                if a == 0 or b == 0:
                    continue
                if a == b:
                    continue

                # Calculate the greatest common divisor (GCD) to find the minimal multipliers
                gcd_val = gcd(a, b)
                k_r = b // gcd_val  # Multiplier for the reactant
                k_p = a // gcd_val  # Multiplier for the product

                # Adjust the multipliers for the reactant and product
                reactant_chem["multiplier"] *= k_r
                product_chem["multiplier"] *= k_p

    # First pass to balance elements in single chemicals
    balance_single_elements()

    # Recalculate atomic compositions after adjustments
    reactants_composition = _atomic_composition(reactants)
    products_composition = _atomic_composition(products)

    # Check if all elements are balanced
    is_balanced = True
    for element in reactants_composition:
        if reactants_composition[element] != products_composition.get(element, 0):
            is_balanced = False
            break

    if not is_balanced:
        # Fallback method to adjust based on remaining unbalanced elements
        # This part is a simplified approach and may not handle all cases
        total_atoms = {}
        # Calculate the total number of atoms required in the products
        for chem in products:
            for elem in chem["decomposition"]:
                elem_name = elem["element"]
                total_atoms[elem_name] = (
                    total_atoms.get(elem_name, 0) + elem["number"] * chem["multiplier"]
                )

        # Adjust reactant multipliers to meet the required atom counts
        for chem in reactants:
            for elem in chem["decomposition"]:
                elem_name = elem["element"]
                needed = total_atoms.get(
                    elem_name, 0
                )  # Number of atoms needed for this element
                current = (
                    elem["number"] * chem["multiplier"]
                )  # Current number of atoms provided by the reactant

                # Skip if no atoms are needed or if the current contribution is zero
                if current == 0:
                    continue

                # If the current contribution is insufficient, adjust the multiplier
                if needed % current != 0:
                    multiplier = needed // current
                    if multiplier <= 0:
                        multiplier = 1
                    chem["multiplier"] *= multiplier

                    # Update the total_atoms as the reactant multiplier changed
                    for e in chem["decomposition"]:
                        en = e["element"]
                        total_atoms[en] = (
                            total_atoms.get(en, 0)
                            + e["number"] * (multiplier - 1) * chem["multiplier"]
                        )

    return {"reactants": reactants, "products": products}


# Main >>>
def balance_formula(chemical_composition: dict) -> dict:
    """Balances a chemical equation by adjusting coefficients of reactants and products.

    Takes a chemical composition dictionary containing reactants and products, and returns
    a balanced chemical equation where the number of atoms of each element is equal on 
    both sides.

    Args:
        chemical_composition (dict): Dictionary containing:
            - "reactants": List of dictionaries for each reactant compound
            - "products": List of dictionaries for each product compound
            Each compound dictionary contains:
                - "decomposition": List of {"element": str, "number": int}
                - "chemical": str (chemical formula)
                - "multiplier": int (coefficient)

    Returns:
        dict: Dictionary with balanced equation containing:
            - "reactants": Updated reactants list with balanced multipliers
            - "products": Updated products list with balanced multipliers

    Example:
        Input:
            {
                "reactants": [{
                    "decomposition": [{"element": "H", "number": 2}, {"element": "O", "number": 1}],
                    "chemical": "H2O",
                    "multiplier": 1
                }],
                "products": [...]
            }
        Output:
            {
                "reactants": [...],  # With updated multipliers
                "products": [...]    # With updated multipliers
            }
    """
    # Get the reactants and products
    reactants = chemical_composition["reactants"]
    products = chemical_composition["products"]

    # Calculate the number of atoms of each element in the reactants and products
    reactants_composition = _atomic_composition(reactants)
    products_composition = _atomic_composition(products)

    # Find the least common multiple of the number of atoms of each element in the reactants and products
    atomic_lcms = _atomic_lcm(reactants_composition, products_composition)

    # Balance the elements + return the balanced elements
    return _balance_elements(reactants, products, atomic_lcms)
