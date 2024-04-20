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
from enum import IntFlag
from pymeasure.instruments.hp.hplegacyinstrument import (
    HPLegacyInstrument,
    StatusBitsBase,
)
from pymeasure.instruments.validators import strict_discrete_set, strict_range


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class HP5384A(HPLegacyInstrument):
    """Represents the Hewlett Packard 5384A 225 MHz frequency counter
    and provides a high-level interface for interacting
    with the instrument.
    """

    def __init__(self, adapter, name="Hewlett-Packard 5384A", **kwargs):
        kwargs.setdefault("read_termination", "\r\n")
        kwargs.setdefault("send_end", True)
        super().__init__(
            adapter,
            name,
            **kwargs,
        )

    FUNCTIONS = {
        "freq_a": "FU1",
        "period_a": "FU2",
        "freq_b": "FU3",
    }

    display_text = HPLegacyInstrument.setting(
        "DR%s",
        """Display up to XX upper-case ASCII characters on the display.
        
        """,
        set_process=(lambda x: str.upper(x[0:20])),
    )

    value_ = HPLegacyInstrument.measurement(
        "",
        """Read the current frequency measurement in Hz.

        """,
    )

    function = HPLegacyInstrument.setting(
        "%s",
        """ Set the measurement function to one of the following:
        'freq_a' - Frequency of input A
        'period_a' - Period of input A
        'freq_b' - Frequency of input B
        """,
        validator=strict_discrete_set,
        values=FUNCTIONS,
        map_values=True,
    )

    # input_a_attenuation = HPLegacyInstrument.setting()

    instrument_id = HPLegacyInstrument.measurement(
        "ID",
        """ Read the instrument identification string.
        Just returns HP5384A.
        """,
    )
