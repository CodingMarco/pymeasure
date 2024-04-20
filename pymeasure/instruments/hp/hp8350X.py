#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2024 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import ctypes
import logging
import math
from enum import IntFlag, IntEnum
from pymeasure.instruments.hp.hplegacyinstrument import (
    HPLegacyInstrument,
    StatusBitsBase,
)
from pymeasure.instruments.validators import strict_discrete_set, strict_range


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class HP8350X(HPLegacyInstrument):
    """Represents the Hewlett Packard 8350A/B sweep oscillator
    and provides a high-level interface for interacting
    with the instrument.
    """

    def __init__(self, adapter, name="Hewlett-Packard 8350X", **kwargs):
        kwargs.setdefault("read_termination", "\r\n")
        kwargs.setdefault("send_end", True)
        super().__init__(
            adapter,
            name,
            **kwargs,
        )

    BOOL_MAPPINGS = {True: 1, False: 0}

    class LevelingMode(IntEnum):
        Internal = 1
        ExternalCrystal = 2
        ExternalPowerMeter = 3

    class FMSensitivity(IntEnum):
        Neg20 = -20
        Neg6 = -6

    def reset(self):
        """Reset the instrument."""
        self.write("IP")

    def decrement(self):
        """Decrements the parameter that was set last by one step."""
        self.write("DN")

    def increment(self):
        """Increments the parameter that was set last by one step."""
        self.write("UP")

    def set_marker_to_center_frequency(self):
        """Sets the marker to the center frequency."""
        self.write("MC")

    amplitude_marker_enabled = HPLegacyInstrument.control(
        "OPAK",
        "AK%d",
        """ Enable/disable the amplitude marker.
        
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    leveling_mode = HPLegacyInstrument.control(
        "OPA",
        "A%d",
        """ Select the leveling mode.
        
        """,
        validator=strict_discrete_set,
        values=[x.value for x in LevelingMode],
        get_process=lambda x: HP8350X.LevelingMode(x),
    )

    amplitude_crystal_marker_enabled = HPLegacyInstrument.control(
        "OPCA",
        "CA%d",
        """ Enable/disable the amplitude crystal marker. 
        (works with 83522/83525 plug-ins only)

        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    intensity_crystal_marker_enabled = HPLegacyInstrument.control(
        "OPCI",
        "CI%d",
        """ Enable/disable the intensity crystal marker. 
        (works with 83522/83525 plug-ins only)

        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    # TODO: X MHz Crystal Marker Frequency

    center_frequency = HPLegacyInstrument.control(
        "OPCF",
        "CF %d",
        """ Select the center frequency in Hz.
        The valid range is constrained by the installed plug-in.
        
        """,
        set_process=lambda x: f"{int(x)}HZ",
    )

    delta_frequency = HPLegacyInstrument.control(
        "OPDF",
        "DF %d",
        """ Delta frequency in Hz.

        """,
        set_process=lambda x: f"{int(x)}HZ",
    )

    display_blanking_enabled = HPLegacyInstrument.control(
        "OPDP",
        "DP%d",
        """ Enable/disable the display blanking.
        
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    display_update_enabled = HPLegacyInstrument.control(
        "OPDU",
        "DU%d",
        """ Enable/disable the display update.
        
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    start_frequency = HPLegacyInstrument.control(
        "OPFA",
        "FA %d",
        """ Select the start frequency in Hz.
        The valid range is constrained by the installed plug-in.
        
        """,
        set_process=lambda x: f"{int(x)}HZ",
    )

    stop_frequency = HPLegacyInstrument.control(
        "OPFB",
        "FB %d",
        """ Select the stop frequency in Hz.
        The valid range is constrained by the installed plug-in.
        
        """,
        set_process=lambda x: f"{int(x)}HZ",
    )

    cw_filter_enabled = HPLegacyInstrument.control(
        "OPFI",
        "FI%d",
        """ Enable/disable the CW filter.
        The CW Filter, when enabled, reduces the oscillator tuning voltage noise and hence Residual FM.
        The CW Filter is inactive in sweep modes.
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    fm_sensitivity = HPLegacyInstrument.control(
        "OPF",
        "F%d",
        """ Select the FM sensitivity.
        Can be eigher -20 for -20 MHz/V or -6 for -6 MHz/V.
        
        """,
        validator=strict_discrete_set,
        values=[x.value for x in FMSensitivity],
        get_process=lambda x: HP8350X.FMSensitivity(x),
    )

    am_enabled = HPLegacyInstrument.control(
        "OPMD",
        "MD%d",
        """ Enable/disable the amplitude modulation.
        
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )

    marker_1_2_sweep_enabled = HPLegacyInstrument.control(
        "OPMP",
        "MP%d",
        """ Enable/disable sweep between the frequencies of marker 1 and 2.
        After exit, sweep returns to original sweep limits.
        
        """,
        validator=strict_discrete_set,
        values=BOOL_MAPPINGS,
        map_values=True,
    )
