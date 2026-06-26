from code import BaconShorCode
from circuit import Circuit
from simulation import Simulation


def syndrome_table(error_type, initial_state="0"):

    code = BaconShorCode()

    print(f"\n=== {error_type} errors ===\n")

    for qubit in range(code.n_data):

        builder = Circuit(code)

        qc = builder.build(
            state=initial_state,
            error=error_type,
            err_reg=qubit,
        )

        result = Simulation(qc).run()

        print(f"{error_type}{qubit} ",result)
