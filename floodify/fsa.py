import numpy as np
from numpy.typing import ArrayLike
from .hypso_curve import HypsoCurve
from .funcs import fsa_flow


class FSA:
    def __init__(
        self,
        orifice_invert: float,
        orifice_height: float,
        orifice_width: float,
        orifice_coefficient: float,
        weir_invert: float,
        weir_width: float,
        weir_coefficient: float,
        hypso_curve: HypsoCurve,
        initial_stage: float = None,
    ) -> None:
        """Initialises the FSA with the given parameters."""
        self.orifice_invert = orifice_invert
        self.orifice_height = orifice_height
        self.orifice_width = orifice_width
        self.orifice_coefficient = orifice_coefficient
        self.weir_invert = weir_invert
        self.weir_width = weir_width
        self.weir_coefficient = weir_coefficient
        self.hypso_curve = hypso_curve
        self.initial_stage = orifice_invert if initial_stage is None else initial_stage

    def run(
        self, inflow: ArrayLike, dt: float
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Calculate the FSA stage, volume and flow using for a given inflow timeseries and timestep.
        Returns the timeseries array of stage, volume, and outflow.
        """
        # Get length of timeseries
        timesteps = len(inflow)
        # Initialise timeseries of stage, volume and outflow
        stage = np.empty(timesteps)
        volume = np.empty(timesteps)
        outflow = np.empty(timesteps)

        # Set the initial condition of stage, volume and outflow
        stage[0] = self.initial_stage
        volume[0] = self.hypso_curve.get_volume(stage[0])
        outflow[0] = fsa_flow(
            stage=stage[0],
            orifice_invert=self.orifice_invert,
            orifice_width=self.orifice_width,
            orifice_height=self.orifice_height,
            orifice_coefficient=self.orifice_coefficient,
            weir_invert=self.weir_invert,
            weir_width=self.weir_width,
            weir_coefficient=self.weir_coefficient,
        )

        # Calculate remaining timesteps
        for i in range(1, timesteps):
            # Calculate change in storage from t-1 to t using inflow rate
            volume_change = (inflow[i - 1] - outflow[i - 1]) * dt
            # Get storage volume at t
            volume[i] = max(0, volume[i - 1] + volume_change)
            # Get stage at t using updated volume and hypsometric curve
            stage[i] = self.hypso_curve.get_stage(volume[i])
            # Caculate outflow using updated stage
            outflow[i] = fsa_flow(
                stage[i],
                orifice_invert=self.orifice_invert,
                orifice_width=self.orifice_width,
                orifice_height=self.orifice_height,
                orifice_coefficient=self.orifice_coefficient,
                weir_invert=self.weir_invert,
                weir_width=self.weir_width,
                weir_coefficient=self.weir_coefficient,
            )

        return stage, volume, outflow
