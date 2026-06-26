from qiskit import QuantumCircuit
from qiskit import QuantumRegister
from qiskit import ClassicalRegister


class Circuit:

    def __init__(self, code):

        self.code = code

        self.data = QuantumRegister(code.n_data, "data")
        self.anc = QuantumRegister(code.n_ancilla, "anc")
        # self.creg = ClassicalRegister(code.n_data + code.n_ancilla, "c") 
        # self.creg = ClassicalRegister(code.n_ancilla, "c")

        self.x_syn = ClassicalRegister(3, "X_syn")
        self.z_syn = ClassicalRegister(3, "Z_syn")
        self.data_out = ClassicalRegister(9, "Data")

        self.x_check = ClassicalRegister(3, "X_chk")
        self.z_check = ClassicalRegister(3, "Z_chk")

        self.qc = QuantumCircuit(
            self.data,
            self.anc,
            self.x_syn,
            self.z_syn,
            self.data_out,
            self.x_check,
            self.z_check,
        )

        # self.qc = QuantumCircuit(
        #     self.data,
        #     self.anc,
        #     self.creg,
        # )


    def prepare(self, state="+"):

        # Setting up at Logical |+> = (GHZ+)^3
        if state == "+" or state == "-":
            for r in [0, 3, 6]:
                self.qc.h(self.data[r])
                self.qc.cx(self.data[r], self.data[r + 1])
                self.qc.cx(self.data[r], self.data[r + 2])

            if state=="-":
                # print("Apply Logical Z")
                for r in [2,5,8]:
                    self.qc.z(self.data[r])

        elif state=="0" or state == "1":
            # Prepare (|000>+|011>+|101>+|110>)/2
            # on qubits 0,3,6
            self.qc.h(0)
            self.qc.h(3)
            self.qc.cx(0, 6)
            self.qc.cx(3, 6)

            # Expand each control into a GHZ row
            # Row 1
            self.qc.cx(0,1)
            self.qc.cx(0,2)
            # Row 2
            self.qc.cx(3,4)
            self.qc.cx(3,5)
            # Row 3
            self.qc.cx(6,7)
            self.qc.cx(6,8)

            if state == "1":
                for r in [0,1,2]:
                    self.qc.x(self.data[r])
            
        for anc in self.anc:
            self.qc.reset(anc)
            self.qc.h(anc)

    # Error on Data Qubits
    def inject_error(self, error_type, qubit):

        if error_type == "X":
            self.qc.x(self.data[qubit])

        elif error_type == "Y":
            self.qc.y(self.data[qubit])

        elif error_type == "Z":
            self.qc.z(self.data[qubit])

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

        self.qc.measure(self.anc, self.x_syn) # Inputting into first 3 classical regs

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

        self.qc.measure(self.anc, self.z_syn)
        # for anc in self.anc:
        #     self.qc.reset(anc)

    def final_measurement(self):

        # # Shift back from GHZ state to normal 000,000,000
        # # Not required in final circuit, good for debug
        # for r in [0, 3, 6]:
        #     self.qc.cx(self.data[r], self.data[r + 1])
        #     self.qc.cx(self.data[r], self.data[r + 2])
        #     self.qc.h(self.data[r])

        # Checking outputs stabilizers
        for anc in self.anc:
            self.qc.reset(anc)
            self.qc.h(anc)
        self.x_syndrome_extraction()
        self.qc.measure(self.anc, self.x_check)

        for anc in self.anc:
            self.qc.reset(anc)
        self.z_syndrome_extraction()
        self.qc.measure(self.anc, self.z_check)
        

        self.qc.measure(
            self.data,
            self.data_out,
        )

    def build(self, state, error, err_reg):

        self.prepare(state)
        self.inject_error(error, err_reg)
        self.x_syndrome_extraction()
        self.x_feedback()

        # Debug for Syndrome check after coherent feedback
        # for anc in self.anc:
        #     self.qc.reset(anc)
        #     self.qc.h(anc)
        # self.x_syndrome_extraction()

        self.z_prepare()
        self.z_syndrome_extraction()
        self.z_feedback()

        self.final_measurement()

        return self.qc
