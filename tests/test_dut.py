import pytest
from model.dut import DUT



def test_dut_initialization():
    dut = DUT()
    assert dut.hw_inputs['temp'] == 25.00
    assert dut.hw_inputs['pot'] == 0
    assert dut.outputs['pot_led'] == 1000
    assert dut.bug is None


def test_input_precedence():
    dut = DUT()

    dut.set_hw_input('pot', 50)
    assert dut.get_input('pot') == 50

    dut.set_swfi_input('pot', 200)
    assert dut.get_input('pot') == 200


def test_clear_inputs():
    dut = DUT()
    dut.set_hw_input('pot', 50)
    dut.set_swfi_input('temp', 100)

    dut.clear_hw_input('pot')
    assert 'pot' not in dut.hw_inputs

    dut.clear_swfi_input('temp')
    assert 'temp' not in dut.swfi_inputs


def test_bug_activation():
    dut = DUT()
    dut.set_bug_active(True)
    assert dut.bug in [1, 2, 3, 4]

    dut.set_bug_active(False)
    assert dut.bug is None


def test_get_output():
    dut = DUT()
    dut.outputs['switch_led'] = 1
    assert dut.get_output('switch_led') == 1



@pytest.mark.parametrize("pot_val, expected_led", [
    (50, 1000),
    (100, 1100),
    (150, 1110),
    (200, 1111)
])
def test_update_pot_normal(pot_val, expected_led):
    dut = DUT()
    dut.set_hw_input('pot', pot_val)
    dut.update_firmware()
    assert dut.outputs['pot_led'] == expected_led


@pytest.mark.parametrize("temp_val, expected_led", [
    (25, 0),
    (35, 1)
])
def test_update_temp_normal(temp_val, expected_led):
    dut = DUT()
    dut.set_hw_input('temp', temp_val)
    dut.update_firmware()
    assert dut.outputs['temp_led'] == expected_led


def test_update_switch_normal():
    dut = DUT()
    dut.set_hw_input('switch', 1)
    dut.update_firmware()
    assert dut.outputs['switch_led'] == 1


def test_bug_case_1():
    dut = DUT()
    dut.bug = 1
    dut.set_hw_input('switch', 1)
    dut.update_firmware()
    assert dut.outputs['switch_led'] == 0


@pytest.mark.parametrize("pot_val, expected_led", [
    (70, 1000),
    (100, 1100),
    (150, 1110),
    (200, 1111)
])
def test_bug_case_2(pot_val, expected_led):
    dut = DUT()
    dut.bug = 2
    dut.set_hw_input('pot', pot_val)
    dut.update_firmware()
    assert dut.outputs['pot_led'] == expected_led

@pytest.mark.parametrize("pot_val, expected_led", [
    (50, 1000),
    (100, 1100),
    (150, 1110),
    (200, 1110)
])
def test_bug_case_3(pot_val, expected_led):
    dut = DUT()
    dut.bug = 3
    dut.set_hw_input('pot', pot_val)
    dut.update_firmware()
    assert dut.outputs['pot_led'] == expected_led


def test_bug_case_4():
    dut = DUT()
    dut.bug = 4
    dut.set_hw_input('temp', 33)
    dut.update_firmware()
    assert dut.outputs['temp_led'] == 0