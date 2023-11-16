def depth(top: float, bottom: float) -> float:
    """Calculate depth."""
    return max(0, top - bottom)


def weir_flow(
    stage: float,
    weir_invert: float,
    weir_width: float,
    weir_coefficient: float,
) -> float:
    """Calculate weir flow."""
    return weir_width * weir_coefficient * depth(top=stage, bottom=weir_invert) ** 1.5


def submerged_orifice_flow(
    stage: float,
    orifice_invert: float,
    orifice_width: float,
    orifice_height: float,
    orifice_coefficient: float,
) -> float:
    """Calculate submerged orifice flow."""
    return (
        orifice_width
        * orifice_height
        * orifice_coefficient
        * (2 * 9.81 * depth(top=stage, bottom=orifice_invert)) ** 0.5
    )


def total_orifice_flow(
    stage: float,
    orifice_invert: float,
    orifice_width: float,
    orifice_height: float,
    orifice_coefficient: float,
    weir_coefficient: float,
) -> float:
    """Calculate orifice flow using either weir or submerged orifice flow function depending on whether the orifice is submerged."""
    # If orifice is entirely submerged, return submerged orifice flow
    if stage > orifice_invert + orifice_height * 1.5:
        return submerged_orifice_flow(
            stage=stage,
            orifice_invert=orifice_invert,
            orifice_width=orifice_width,
            orifice_height=orifice_height,
            orifice_coefficient=orifice_coefficient,
        )
    # If orifice is not submerged, return weir flow using orifice parameters
    return weir_flow(
        stage=stage,
        weir_invert=orifice_invert,
        weir_width=orifice_width,
        weir_coefficient=weir_coefficient,
    )


def fsa_flow(
    stage: float,
    orifice_invert: float,
    orifice_width: float,
    orifice_height: float,
    orifice_coefficient: float,
    weir_invert: float,
    weir_width: float,
    weir_coefficient: float,
) -> float:
    """
    Calculate total flow through an FSA, including through the orifice and over the weir when full.
    Returns scalar flow value.
    """
    return total_orifice_flow(
        stage=stage,
        orifice_invert=orifice_invert,
        orifice_width=orifice_width,
        orifice_height=orifice_height,
        orifice_coefficient=orifice_coefficient,
        weir_coefficient=weir_coefficient,  # Check if this is the same value as below
    ) + weir_flow(
        stage=stage,
        weir_invert=weir_invert,
        weir_width=weir_width,
        weir_coefficient=weir_coefficient,  # Check if this is the same value as above
    )
