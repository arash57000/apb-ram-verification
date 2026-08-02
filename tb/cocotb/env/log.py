import cocotb
import logging


def dv_log(dut, name="DV"):
    """
    Unified logging interface for DV components.
    Mimics UVM report server behavior.

    Usage:
        log = dv_log(dut, "SEQ")
        log.info("message")
        log.warning("message")
        log.error("message")
    """

    logger = dut._log.getChild(name)

    # Attach Python logging style formatting
    py_logger = logging.getLogger(name)
    py_logger.setLevel(logging.INFO)

    return logger

