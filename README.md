# Simple Chemistry Balancer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

This project is a **simple example** of a chemical equation balancer implemented in Python. It is designed to demonstrate the basic concepts of balancing chemical equations programmatically. While it works for many common cases, it is **not the fastest or most efficient solution** available.

## 🚀 Installation

To use this example project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AidinHamedi/Simple-Chemistry-Balencer.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd Simple-Chemistry-Balencer
   ```

3. **Run the Script**:
   Ensure you have Python 3.9 or higher installed, then run:
   ```bash
   python run.py
   ```


## 🛠️ Usage

When you run the script, you will be prompted to enter a chemical equation. The equation should be in the following format:

```
Reactants=>Products
```

For example:
```
Formula: H2+O2=>H2O
```

The program will output the balanced equation:
```
H2+O2=>(H2O)2
```

## 🪜 How It Works (Simplified)

1. **Input Validation**: The input formula is checked to ensure it follows the correct format.
2. **Decomposition**: The formula is split into reactants and products, and each chemical compound is broken down into its constituent elements.
3. **Balancing**: The balancer calculates the least common multiple (LCM) of atom counts for each element and adjusts the coefficients to balance the equation.
4. **Assembly**: The balanced equation is reconstructed into a readable string.

## 🚶‍➡️ Example Code Walkthrough

### Decomposition (`decomposer.py`)
The `decompose_formula` function splits the input formula into reactants and products, then further decomposes each compound into its elements and their counts.

### Balancing (`balancer.py`)
The `balance_formula` function calculates the necessary coefficients to balance the equation by comparing the number of atoms on both sides of the equation.

### Assembly (`assembler.py`)
The `assemble_formula` function reconstructs the balanced equation into a readable string.

## 📝 License
This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/licenses/MIT) file for details.
