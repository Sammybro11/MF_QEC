from dataclasses import dataclass


@dataclass
class BaconShorCode:

    distance: int = 3

    def __post_init__(self):

        self.n_data = 9
        self.n_ancilla = 3

        # X stabilizers
        self.x_stabilizers = [
            [0, 1, 2, 3, 4, 5],
            [3, 4, 5, 6, 7, 8],
            [0, 1, 2, 6, 7, 8],
        ]

        # Z stabilizers
        self.z_stabilizers = [
            [0, 1, 3, 4, 6, 7],
            [1, 2, 4, 5, 7, 8],
            [0, 2, 3, 5, 6, 8],
        ]

        self.logical_x = [
            [0,1,2]
        ]

        self.logical_z = [
            [2,5,8]
        ]

    def syndrome_table(self):
        """
        Optional lookup table.

        syndrome -> correction
        """
        return {}
