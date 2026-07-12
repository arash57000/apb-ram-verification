"""
===============================================================================
Test Name : test_addr0.py

Description:
    Directed test that verifies write and read functionality at the
    lowest valid APB RAM address (address 0).

Verification Objective:
    - Reset the DUT
    - Write known data to address 0
    - Read back from address 0
    - Verify the read data matches the written data

Expected Result:
    Test passes if the read data equals the written data.
===============================================================================
"""

import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_addr0(dut):

    # Start APB clock
    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== DIRECTED TEST: ADDRESS 0 ==========")

    # Reset DUT
    await reset_dut(dut)

    # Test data
    addr = 0
    data = 0xA5

    cocotb.log.info(
        f"WRITE ADDR={addr} DATA=0x{data:02X}"
    )

    # Write
    await apb_write(dut, addr, data)

    # Read
    rdata = await apb_read(dut, addr)

    # Verify
    assert rdata == data, (
        f"Expected 0x{data:02X}, "
        f"Got 0x{rdata:02X}"
    )

    cocotb.log.info("Address 0 test PASSED.")