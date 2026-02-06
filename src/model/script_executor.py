import asyncio
from src.model.hil_system import HILSystem


class ScriptExecutor:
    def __init__(self, hil_system: HILSystem):
        self.hil = hil_system
        self.is_running = False
        self.step_delay = 0.0

    async def run_script(self, script_text: str, log_callback):
        self.is_running = True
        self.hil.init_dut()
        lines = [line.strip() for line in script_text.split('\n') if line.strip()]

        if not self._validate_structure(lines, log_callback):
            self.is_running = False
            return

        self.hil.logger.start_log("Batch Execution")


        try:
            for i, line in enumerate(lines):
                if not self.is_running: break

                if self.step_delay > 0:
                    await asyncio.sleep(self.step_delay)

                log_callback(f"Line {i + 1}: {line}")

                parts = line.split()
                if not parts: continue

                if line.lower() == 'pause':
                    log_callback(">>> Script execution finished (PAUSE reached).")
                    break

                if parts[0] == 'batchControl':
                    cmd_type = parts[1]
                    args = parts[2:]

                    if cmd_type == '-wait':
                        seconds = float(args[0])
                        log_callback(f"... Waiting {seconds}s ...")
                        await asyncio.sleep(seconds)

                    else:
                        self.hil.process_command(cmd_type, args)

        except Exception as e:
            log_callback(f"CRITICAL ERROR: {str(e)}")
        finally:
            log_callback("... Resetting DUT to initial state ...")
            try:
                self.hil.init_dut()
            except Exception as reset_err:
                log_callback(f"Error during reset: {reset_err}")

            self.hil.logger.close_log()
            self.is_running = False

    def _validate_structure(self, lines, log_cb):
        # 1. -init
        has_init = any('batchControl -init' in line for line in lines)
        if not has_init:
            log_cb("ERROR: Script must contain 'batchControl -init'")
            return False

        # 2. -start
        has_start = any('batchControl -start' in line for line in lines)
        if not has_start:
            log_cb("ERROR: Script must contain 'batchControl -start'")
            return False

        # 3. pause
        has_pause = any(line.lower() == 'pause' for line in lines)
        if not has_pause:
            log_cb("ERROR: Script must contain 'pause'")
            return False

        return True