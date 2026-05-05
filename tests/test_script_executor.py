import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.model.script_executor import ScriptExecutor

@pytest.fixture
def mock_hil():
    hil = MagicMock()
    hil.logger = MagicMock()
    hil.process_command = AsyncMock()
    return hil

@pytest.fixture
def executor(mock_hil):
    return ScriptExecutor(mock_hil)

@pytest.mark.asyncio
async def test_run_script_valid_structure(executor, mock_hil):
    script_text = """
    batchControl -init
    batchControl -start
    batchControl -hwfi temp 50
    pause
    """
    log_callback = MagicMock()
    update_callback = MagicMock()

    await executor.run_script(script_text, log_callback, update_callback)

    assert update_callback.call_count >= 2
    
    assert mock_hil.init_dut.call_count == 2
    mock_hil.logger.start_log.assert_called_once_with("Batch Execution")
    mock_hil.logger.close_log.assert_called_once()

    mock_hil.process_command.assert_any_call("-init", [])
    mock_hil.process_command.assert_any_call("-start", [])
    mock_hil.process_command.assert_any_call("-hwfi", ["temp", "50"])

    log_callback.assert_any_call(">>> Script execution finished (PAUSE reached).")

@pytest.mark.asyncio
async def test_run_script_invalid_structure_no_init(executor, mock_hil):
    script_text = """
    batchControl -start
    pause
    """
    log_callback = MagicMock()
    await executor.run_script(script_text, log_callback, MagicMock())
    
    log_callback.assert_any_call("ERROR: Script must contain 'batchControl -init'")
    assert not executor.is_running

@pytest.mark.asyncio
async def test_run_script_invalid_structure_no_start(executor, mock_hil):
    script_text = """
    batchControl -init
    pause
    """
    log_callback = MagicMock()
    await executor.run_script(script_text, log_callback, MagicMock())
    
    log_callback.assert_any_call("ERROR: Script must contain 'batchControl -start'")
    assert not executor.is_running

@pytest.mark.asyncio
async def test_run_script_invalid_structure_no_pause(executor, mock_hil):
    script_text = """
    batchControl -init
    batchControl -start
    """
    log_callback = MagicMock()
    await executor.run_script(script_text, log_callback, MagicMock())
    
    log_callback.assert_any_call("ERROR: Script must contain 'pause'")
    assert not executor.is_running

@pytest.mark.asyncio
async def test_run_script_exception_handling(executor, mock_hil):
    script_text = """
    batchControl -init
    batchControl -start
    batchControl -hwfi temp 50
    pause
    """
    log_callback = MagicMock()
    mock_hil.process_command.side_effect = Exception("Test Error")
    
    await executor.run_script(script_text, log_callback, MagicMock())
    
    log_callback.assert_any_call("CRITICAL ERROR: Test Error")
    mock_hil.logger.close_log.assert_called_once()
    assert executor.is_running is False

@pytest.mark.asyncio
async def test_run_script_step_delay(executor, mock_hil):
    script_text = """
    batchControl -init
    batchControl -start
    pause
    """
    executor.step_delay = 0.1
    log_callback = MagicMock()
    
    start_time = asyncio.get_event_loop().time()
    await executor.run_script(script_text, log_callback, MagicMock())
    end_time = asyncio.get_event_loop().time()
    
    assert (end_time - start_time) >= 0.25

def test_validate_structure_valid(executor):
    lines = ["batchControl -init", "batchControl -start", "pause"]
    log_cb = MagicMock()
    assert executor._validate_structure(lines, log_cb) is True

def test_validate_structure_missing_init(executor):
    lines = ["batchControl -start", "pause"]
    log_cb = MagicMock()
    assert executor._validate_structure(lines, log_cb) is False
    log_cb.assert_called_with("ERROR: Script must contain 'batchControl -init'")
