import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_read,
    initialize_memory_pattern,
)


@cocotb.test()
async def test_sequential_read(dut):
    """
    Directed Test

    Verification Objective:
        Verify that every valid APB RAM address (0–31)
        returns the expected data after memory
        initialization.
    """

    # Start APB clock
    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: SEQUENTIAL READ ==========")

    # Reset DUT
    await reset_dut(dut)

    # Initialize RAM with a known pattern
    await initialize_memory_pattern(dut)

    # Read and verify every address
    for addr in range(32):

        expected_data = addr + 1

        read_data = await apb_read(dut, addr)

        assert read_data == expected_data, (
            f"Read mismatch at address {addr}. "
            f"Expected 0x{expected_data:08X}, "
            f"Got 0x{read_data:08X}"
        )

    cocotb.log.info(
        "PASS: Sequential read verification completed successfully."
    )