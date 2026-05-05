import pytest
import os
import socket
from unittest.mock import patch, mock_open
from datetime import datetime
from src.model.logger import HtmlLogger, get_hostname

def test_get_hostname():
    assert get_hostname() == socket.gethostname()

@pytest.fixture
def logger(tmp_path):
    log = HtmlLogger()
    return log

orig_join = os.path.join

@pytest.fixture
def mock_logs_dir(tmp_path):
    def _join(*args):
        if len(args) == 2 and args[0] == 'logs':
            return orig_join(str(tmp_path), args[1])
        return orig_join(*args)
    
    with patch("src.model.logger.os.path.join", side_effect=_join):
        yield

def test_start_log(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test Script")
    
    assert logger.filepath is not None
    assert os.path.exists(logger.filepath)
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<html><head>" in content
        assert "LOG CREATED" in content
        assert "HOST:" in content

def test_log_comment(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    logger.log_comment("This is a test comment")
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<div class='comment'>This is a test comment</div>" in content

def test_log_wait(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    logger.log_wait(5)
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<div class='comment'>Wait 5 seconds</div>" in content

def test_log_hil_state(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    data = {
        'Temperature': 25.5,
        'Temp LED': 'OFF',
        'Switch': 'ON',
        'Switch LED': 'ON',
        'Potentiometer': 500,
        'Quadrantal LEDs': 10
    }
    logger.log_hil_state(data)
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "25.5" in content
        assert "Potentiometer" in content
        assert "500" in content

def test_log_generic(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    logger.log_generic("Test Title", "Test Message")
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<h2>Test Title</h2>" in content
        assert "<span>Test Message</span>" in content

def test_log_assert(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    item_pass = {
        'source': 'temp',
        'measured': 25.0,
        'assertType': 'eq',
        'expected': 25.0,
        'result': 'PASS'
    }
    logger.log_assert(item_pass)
    
    item_fail = {
        'source': 'temp',
        'measured': 30.0,
        'assertType': 'eq',
        'expected': 25.0,
        'result': 'FAIL'
    }
    logger.log_assert(item_fail)
    
    with open(logger.filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        assert "<div class='pass'>PASS</div>" in content
        assert "<div class='fail'>FAIL</div>" in content
        assert "30.0" in content

def test_close_log(logger, mock_logs_dir, tmp_path):
    logger.start_log("Test")
    logger.close_log()
    
    assert logger.filepath is None
        
def test_write_without_start(logger):
    logger.log_comment("Should not crash")
    logger.close_log()
    assert logger.filepath is None
