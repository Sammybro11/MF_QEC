from qiskit_aer import AerSimulator
from qiskit import transpile


class Simulation:

    def __init__(self, circuit):

        self.backend = AerSimulator()
        self.circuit = circuit

    def run(self, shots=1024):

            compiled = transpile(
                self.circuit,
                self.backend,
            )

            job = self.backend.run(
                compiled,
                shots=shots,
            )

            counts = job.result().get_counts()

            return counts

