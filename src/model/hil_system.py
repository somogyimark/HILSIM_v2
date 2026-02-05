from src.model.dut import DUT
from src.model.logger import HtmlLogger
from datetime import datetime


class HILSystem:
    def __init__(self, dut: DUT):
        self.dut = dut
        self.logger = HtmlLogger()

    def process_command(self, cmd_type: str, args: list) -> dict:


        if cmd_type in ['-hwfi', '-swfi']:
            source = args[0]
            value = int(args[1])

            if cmd_type == '-hwfi':
                self.dut.set_hw_input(source, value)
                self.logger.log_generic(f"HWFI {source} {value}", datetime.now().strftime("%H:%M:%S"))
            else:
                self.dut.set_swfi_input(source, value)
                self.logger.log_generic(f"SWFI {source} {value}", datetime.now().strftime("%H:%M:%S"))

            self.dut.update_firmware()
            return {'status': 'ok'}

        elif cmd_type == '-assert':

            source = args[0]
            expected = int(args[1])

            if '_led' in source:
                measured = self.dut.get_output(source)
            else:
                measured = self.dut.get_input(source)

            result = "PASS" if (measured == expected) else "FAIL"
            data= {
                'type': 'assert',
                'source': source,
                'measured': measured,
                'assertType': '=',
                'expected': expected,
                'result': result
            }
            self.logger.log_assert(data)
            return {'status': 'ok'}


        elif cmd_type == '-bug_on':
            self.dut.is_bug_active = True
            self.dut.update_firmware()
            self.logger.log_generic("BUG_ON", datetime.now().strftime("%H:%M:%S"))
            return {'status': 'ok'}

        elif cmd_type == '-init':
            self.dut.__init__()
            self.logger.log_generic("Initialize", datetime.now().strftime("%H:%M:%S"))
            return {'status': 'ok'}

        elif cmd_type == '-start':
            return {'status': 'ok'}

        elif cmd_type == '-comment':
            text = " ".join(args)
            self.logger.log_comment(text)
            return {'status': 'ok'}

        return {'status': 'unknown'}