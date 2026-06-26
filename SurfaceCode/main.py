from code import BaconShorCode
from circuit import Circuit
from simulation import Simulation
from experiments import syndrome_table

def main():
    print("Initial State 0")
    syndrome_table("X")
    syndrome_table("Z")
    syndrome_table("Y")
    # print("Initial State Logical 1")
    # syndrome_table("X", "1")
    # syndrome_table("Z", "1")
    # syndrome_table("Y", "1")
    # print("Initial State Logical +")
    # syndrome_table("X", "+")
    # syndrome_table("Z", "+")
    # syndrome_table("Y", "+")


if __name__ == "__main__":
    main()
