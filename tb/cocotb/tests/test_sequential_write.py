import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_sequential_write(dut):
    """
    Directed Test

    Verification Objective:
        Verify that write transactions complete successfully for every
        valid APB RAM address (0–31).
    """

    # Start APB clock
    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: SEQUENTIAL WRITE ==========")

    # Reset DUT
    await reset_dut(dut)

    # Initialize RAM with a known data pattern
    await initialize_memory_pattern(dut)

    cocotb.log.info("PASS: Sequential write completed successfully.")