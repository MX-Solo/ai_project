# Advanced Map Coloring with Neighbourhood Awareness
This file contains a template for solving the Skyscraper problem. You have to complete the code to implement the solution.  
The goal of the Skyscraper Puzzle is to fill a grid with numbers, representing building heights, so that each row and column contains unique values from 1 up to the grid size. Clues around the grid indicate the number of visible buildings from that vantage point, with taller buildings blocking the view of shorter ones behind them. The solution must satisfy both the uniqueness and visibility constraints for all rows and columns.


## Installation

```python
pip install -r requirements.txt
```
## Contents
Below is a brief overview of the contents: 

- CSP.py: Contains the CSP class representing a Constraint Satisfaction Problem and provides functions to define CSP problems.

- graphics.py: Functions for visualizing the table based on the solution found.

- test_case_generator.py: Generates grids with arbitrary size.

- Solver.py: Contains a class with functions to implement algorithms for finding the CSP solution.

- main.py: Main file to execute the code with specified parameters.

## Parameters
* -m, --map: Specifies the table to solve. 

* -lcv, --lcv: Enables the Least Constraint Value (LCV) heuristic as an order-type optimizer.

* -mrv, --mrv: Enables the Minimum Remaining Values (MRV) heuristic as an order-type optimizer.

* -MAC, --maintaining_arc_consistency: Processes constraints to remove values from variable domains that violate constraint consistency.


## Running the Code
To run the code, you have to execute main.py with the following command format: 

* If you want to solve map 3 with lcv and mrv heuristics: 

python3 main.py -m3 -lcv -mrv 
(If python 3 is the default version on your system, you can simply use python instead of python3: 
python main.py -m3 -lcv -mrv)
 
* If you want to also enable arc consistency: 

python3 main.py -m2 -lcv -mrv -MAC

you can observe the number of assignments for each run, which is displayed above the table, enabling you to compare algorithms.

