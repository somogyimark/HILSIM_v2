import traceback
from src.model.dut import DUT

class ScriptExecutor:
    def __init__(self, dut: DUT):
        self.dut = dut

    def execute(self, script_code: str, log_callback):

        def custom_print(*args):
            msg = " ".join(map(str, args))
            log_callback(msg)


        execution_context = {
            'dut': self.dut,
            'print': custom_print,
        }

        try:
            log_callback(">>> Running script...")

            exec(script_code, execution_context)
            log_callback(">>> Execution finished successfully.")
        except Exception as e:
            error_msg = traceback.format_exc()
            log_callback(f"ERROR:\n{error_msg}")