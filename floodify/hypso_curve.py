import numpy as np
from numpy.typing import ArrayLike


class HypsoCurve:
    def __init__(self, area: ArrayLike, elevation: ArrayLike) -> None:
        """Initialises the HypsoCurve with area and elevation data."""
        self.area = area
        self.elevation = elevation
        try:
            self.volume = np.insert(
                np.cumsum(((area[:-1] + area[1:]) / 2) * np.diff(elevation)), 0, 0
            )
        except ValueError:
            # If area and elevation are pandas.Series objects, then ValueError may be thrown
            # Convert pandas.Series objects to numpy.Array
            area = area.values
            elevation = elevation.values
            self.volume = np.insert(
                np.cumsum(((area[:-1] + area[1:]) / 2) * np.diff(elevation)), 0, 0
            )

    def get_stage(self, volume: float) -> float:
        """
        Returns the stage (elevation) corresponding to a given volume using linear interpolation.
        """
        return np.interp(volume, self.volume, self.elevation)

    def get_volume(self, stage: float) -> float:
        """
        Returns the volume corresponding to a given stage (elevation) using linear interpolation.
        """
        return np.interp(stage, self.elevation, self.volume)
