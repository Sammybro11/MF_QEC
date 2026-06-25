from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit import ClassicalRegister


class Circuit:

    def __init__(self, code):

        self.code = code

        self.data = QuantumRegister(code.n_data, "data")
        self.anc = QuantumRegister(code.n_ancilla, "anc")
        self.creg = ClassicalRegister(code.n_data + code.n_ancilla, "c")
        # self.creg = ClassicalRegister(code.n_ancilla, "c")

        self.qc = QuantumCircuit(
            self.data,
            self.anc,
            self.creg,
        )


    def prepare(self):

        # Setting up at Logical 0 = (GHZ+)^3
        for r in [0, 3, 6]:
            self.qc.h(self.data[r])
            self.qc.cx(self.data[r], self.data[r + 1])
            self.qc.cx(self.data[r], self.data[r + 2])

        for anc in self.anc:
            self.qc.reset(anc)
            self.qc.h(anc)


    def x_syndrome_extraction(self):

        for anc, stabilizer in enumerate(self.code.x_stabilizers):

            for q in stabilizer:
                self.qc.cx( self.anc[anc],self.data[q])

        for anc in self.anc:
            self.qc.h(anc)

    def x_feedback(self):


        self.qc.ccz(self.data[2], self.anc[0], self.anc[2])
        self.qc.ccz(self.data[5], self.anc[0], self.anc[1])
        self.qc.ccz(self.data[8], self.anc[1], self.anc[2])

        # for anc in self.anc:
        #     self.qc.reset(anc)

    def z_prepare(self):

        for anc in self.anc:
            self.qc.reset(anc)

    def z_syndrome_extraction(self):

        for anc, stabilizer in enumerate(self.code.z_stabilizers):

            for q in stabilizer:
                self.qc.cx(self.data[q], self.anc[anc])

    def z_feedback(self):

        self.qc.ccx(self.anc[0], self.anc[2], self.data[0])
        self.qc.ccx(self.anc[0], self.anc[1], self.data[1])
        self.qc.ccx(self.anc[1], self.anc[2], self.data[2])

        # for anc in self.anc:
        #     self.qc.reset(anc)

    def final_measurement(self):

        # Shift back from GHZ state to normal 000,000,000
        for r in [0, 3, 6]:
            self.qc.cx(self.data[r], self.data[r + 1])
            self.qc.cx(self.data[r], self.data[r + 2])
            self.qc.h(self.data[r])
        

        self.qc.measure(
            list(self.data) + list(self.anc),
            self.creg,
        )

    def build(self):

        self.prepare()
        self.qc.x(self.data[1])
        self.x_syndrome_extraction()
        self.x_feedback()

        # for anc in self.anc:
        #     self.qc.reset(anc)
        #     self.qc.h(anc)
        # self.x_syndrome_extraction()

        self.z_prepare()
        self.z_syndrome_extraction()
        self.z_feedback()

        self.final_measurement()

        return self.qc
