from src.model.dut import DUT
from src.model.logger import HtmlLogger


class HILSystem:
    def __init__(self, dut: DUT):
        self.dut = dut
        self.logger = HtmlLogger()

    def process_command(self, cmd_type: str, args: list) -> dict:


        if cmd_type in ['-hwfi', '-swfi']:
            target = args[0]  # pl. 'temp'
            value = int(args[1])  # pl. 70

            if cmd_type == '-hwfi':
                self.dut.set_hw_input(target, value)
                self.logger.log_generic("HWFI Action", f"Set HW input '{target}' to {value}")
            else:
                self.dut.set_swfi_input(target, value)
                self.logger.log_generic("SWFI Action", f"Set SW injection '{target}' to {value}")

            self.dut.update_firmware()
            return {'status': 'ok'}

        elif cmd_type == '-assert':

            target = args[0]
            expected = int(args[1])

            if '_led' in target:
                actual = 1 if self.dut.outputs.get(target) else 0
            else:
                actual = self.dut.get_input(target)

            passed = (actual == expected)
            return {
                'type': 'assert',
                'param': target,
                'expected': expected,
                'actual': actual,
                'passed': passed
            }

        elif cmd_type == '-bug_on':
            self.dut.is_bug_active = True
            self.dut.update_firmware()
            self.logger.log_generic("BUG SIMULATION", "Bug Mode Enabled")
            return {'status': 'ok'}

        elif cmd_type == '-init':
            self.dut.__init__()
            self.logger.log_generic("System Init", "HIL System Initialized to default state.")
            return {'status': 'ok'}

        elif cmd_type == '-start':
            self.logger.log_generic("System Start", "Simulation sequence started.")
            return {'status': 'ok'}

        elif cmd_type == '-comment':
            text = " ".join(args)
            self.logger.log_comment(text)
            return {'status': 'ok'}

        return {'status': 'unknown'}