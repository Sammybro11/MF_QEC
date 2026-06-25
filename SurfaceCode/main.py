from code import BaconShorCode
from circuit import Circuit
from simulation import Simulation


def main():

    code = BaconShorCode()

    builder = Circuit(code)

    qc = builder.build()

    print(qc.draw())

    sim = Simulation(qc)

    counts = sim.run()

    print(counts)


if __name__ == "__main__":
    main()
