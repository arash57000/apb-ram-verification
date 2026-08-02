import cocotb

from cocotb.clock import Clock

from cocotb.triggers import RisingEdge

from tests.tb_utils import (
    reset_dut,
    apb_write,
    apb_read
)


@cocotb.test()
async def test_stress_repeated_address(dut):
    """
    Stress Test

    Verify reliable operation during repeated
    writes and reads to the same RAM location.

    Test sequence:
        - Reset DUT
        - Repeatedly write to one address
        - Read back immediately after each write
        - Verify data integrity
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    await RisingEdge(dut.pclk)
    await RisingEdge(dut.pclk)

    addr = 15

    for iteration in range(500):

        data = (0x5A5A0000 | iteration) & 0xFFFFFFFF

        await apb_write(
            dut,
            addr,
            data
        )

        actual = await apb_read(
            dut,
            addr
        )

        assert actual == data, (
            f"Iteration {iteration}: "
            f"Address {addr}: "
            f"Expected 0x{data:08X}, "
            f"Got 0x{actual:08X}"
        )
        
        if (iteration + 1) % 100 == 0:
            cocotb.log.info(
            f"Completed {iteration + 1} iterations"
        )

    cocotb.log.info(
        "Stress repeated-address test PASSED."
    )