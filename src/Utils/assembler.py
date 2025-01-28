# Main >>>
def assemble_formula(chemical_composition: dict) -> str:
    # Make a var to hold the formula
    formula = ""

    # Iterate over the formula scopes
    for chemical_scope, scope_chemicals in chemical_composition.items():
        # Iterate over the chemicals in the scope
        for chemical in scope_chemicals:
            # Add the chemical to the formula
            if chemical["multiplier"] > 1:
                formula += f"({chemical['chemical']}){chemical['multiplier']}"
            else:
                formula += chemical["chemical"]
            # Add the + sign if it's not the last chemical
            if chemical != scope_chemicals[-1]:
                formula += "+"
        # Add the => sign for the next scope (products)
        if chemical_scope == "reactants":
            formula += "=>"

    # Return the formula
    return formula
