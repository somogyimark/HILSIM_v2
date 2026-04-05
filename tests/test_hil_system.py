import pytest
import asyncio
import time
from model.dut import DUT
from model.hil_system import HILSystem
from unittest.mock import MagicMock

pytestmark = pytest.mark.asyncio

async def test_hil_system_initialization():
    dut = DUT()
    hil = HILSystem(dut)
    assert hil.dut == dut

@pytest.mark.parametrize("cmd_type, args, hw_input, swfi_input", [
    ('-hwfi', ['pot', 11], 11, None),
    ('-hwfi', ['pot', 111], 111, None),
    ('-hwfi', ['pot', 21], 21, None),
    ('-swfi', ['pot', 21], 0, 21),
    ('-swfi', ['pot', 198], 0, 198),
    ('-hwfi', ['temp', 45.5], 45.5, None),
    ('-swfi', ['temp', 45.5], 25, 45.5),
    ('-hwfi', ['switch', 1], 1, None),
    ('-swfi', ['switch', 1], 0, 1),
])
@pytest.mark.asyncio

async def test_fault_injection(cmd_type, args, hw_input, swfi_input):
    dut = DUT()
    hil = HILSystem(dut)

    await hil.process_command(cmd_type, args)

    assert dut.hw_inputs[args[0]] == hw_input
    assert dut.swfi_inputs[args[0]] == swfi_input


async def test_wait():
    dut = DUT()
    hil = HILSystem(dut)

    start = time.time()

    await hil.process_command('-wait', [2])

    end = time.time()
    assert end - start > 2


@pytest.mark.parametrize("source, expected_arg, actual_dut_val, is_output, expected_result, expected_str_val", [
    ('temp', '25.0', 25.0, False, 'PASS', '25.00'),

    ('temp', '30.0', 25.0, False, 'FAIL', '30.00'),

    ('pot_led', '1100', 1100, True, 'PASS', '1100'),

    ('pot_led', '1111', 1000, True, 'FAIL', '1111'),
])
@pytest.mark.asyncio
async def test_assert_command(source, expected_arg, actual_dut_val, is_output, expected_result, expected_str_val):
    dut = DUT()
    hil = HILSystem(dut)

    hil.logger = MagicMock()

    if is_output:
        dut.outputs[source] = actual_dut_val
    else:
        dut.set_hw_input(source, actual_dut_val)

    result = await hil.process_command('-assert', [source, expected_arg])

    assert result == {'status': 'ok'}

    hil.logger.log_assert.assert_called_once()

    logged_data = hil.logger.log_assert.call_args[0][0]

    assert logged_data['type'] == 'assert'
    assert logged_data['source'] == source
    assert logged_data['assertType'] == '='
    assert logged_data['result'] == expected_result
    assert logged_data['expected'] == expected_str_val

async def test_bugon():
    dut = DUT()
    hil = HILSystem(dut)

    await hil.process_command('-bug_on')

    assert dut.bug != None




