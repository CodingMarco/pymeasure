import datetime
import time

import pytest

from pymeasure.generator import Generator
from pymeasure.instruments.redpitaya import RedPitayaScpi

ip_address = '169.254.134.87'
port = 5000

generator = Generator()
inst: RedPitayaScpi = generator.instantiate(RedPitayaScpi, f"TCPIP::{ip_address}::{port}::SOCKET", 'redpitaya',
                             adapter_kwargs=dict(read_termination='\r\n',
                                                 write_termination='\r\n',
                                                 ))


inst.time = datetime.time(13, 7, 20)
assert inst.time.hour == 13
assert inst.time.minute == 7

inst.date = datetime.date(2023, 12, 22)
assert inst.date == datetime.date(2023, 12, 22)

inst.board_name

inst.digital_reset()

for ind in range(8):
    inst.led[ind].enabled = True
    assert inst.led[ind].enabled

    inst.led[ind].enabled = False
    assert not inst.led[ind].enabled

for ind in range(7):
    inst.dioN[ind].direction_in = True
    assert inst.dioN[ind].direction_in
    inst.dioN[ind].direction_in = False
    assert not inst.dioN[ind].direction_in

    inst.dioN[ind].enabled = True
    assert inst.dioN[ind].enabled

    inst.dioN[ind].enabled = False
    assert not inst.dioN[ind].enabled

for ind in range(7):
    inst.dioP[ind].direction_in = True
    assert inst.dioP[ind].direction_in
    inst.dioP[ind].direction_in = False
    assert not inst.dioP[ind].direction_in

    inst.dioP[ind].enabled = True
    assert inst.dioP[ind].enabled

    inst.dioP[ind].enabled = False
    assert not inst.dioP[ind].enabled

inst.analog_reset()

for ind in range(4):
    inst.analog_in_slow[ind].voltage
    inst.analog_out_slow[ind].voltage = 0.5

for ind in range(17):
    inst.decimation = 2**ind
    assert inst.decimation == 2**ind

inst.average_skipped_samples = False
assert inst.average_skipped_samples is False
inst.average_skipped_samples = True
assert inst.average_skipped_samples

assert inst.acq_units == 'VOLTS'
inst.acq_units = 'RAW'
assert inst.acq_units == 'RAW'

assert inst.acq_size == 16384

inst.acq_format = 'ASCII'
inst.acq_format = 'BIN'

for trigger_source in inst.TRIGGER_SOURCES:
    inst.acq_trigger_source = trigger_source
    if trigger_source == "DISABLED":
        assert inst.acq_trigger_status

assert inst.acq_buffer_filled is False

inst.acq_trigger_delay_samples = 0
assert inst.acq_trigger_delay_samples == 0
assert inst.acq_trigger_delay_ns == 0

inst.acq_trigger_delay_samples = 500
assert inst.acq_trigger_delay_samples == 500
assert inst.acq_trigger_delay_ns == int(500 / inst.CLOCK * 1e9)

inst.acq_trigger_delay_ns = RedPitayaScpi.DELAY_NS[10]
assert inst.acq_trigger_delay_ns == RedPitayaScpi.DELAY_NS[10]
assert inst.acq_trigger_delay_samples == -8192 + 10

inst.acq_trigger_level = 0.5
assert inst.acq_trigger_level == pytest.approx(0.5)

inst.ain1.gain = 'LV'
assert inst.ain1.gain == 'LV'

inst.acq_format = 'BIN'
inst.ain1.get_data_from_binary()

inst.acq_format = 'ASCII'
inst.ain1.get_data_from_ascii()

generator.write_file('test_redpitaya.py')