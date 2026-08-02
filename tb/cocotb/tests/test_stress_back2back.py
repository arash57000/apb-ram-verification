import cocotb

from cocotb.clock import Clock

from cocotb.triggers import RisingEdge

from tests.tb_utils import (
    reset_dut,
    apb_write,
    apb_read
)




@cocotb.test()
async def test_stress_back2back(dut):
    """
    Stress Test

    Verify reliable APB operation during sustained
    back-to-back transactions.

    Test sequence:
        - Reset DUT
        - Write all 32 RAM locations
        - Read back all 32 RAM locations
        - Verify data integrity
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    await RisingEdge(dut.pclk)
    await RisingEdge(dut.pclk)

    expected_memory = {}

    # -------------------------------------------------
    # Back-to-back writes
    # -------------------------------------------------

    for addr in range(32):

        data = (0xA5A50000 | (addr * 3)) & 0xFFFFFFFF

        expected_memory[addr] = data


        await apb_write(
            dut,
            addr,
            data
        )

    # -------------------------------------------------
    # Back-to-back reads
    # -------------------------------------------------

    for addr in range(32):

        expected = expected_memory[addr]

        actual = await apb_read(
            dut,
            addr
        )

        assert actual == expected, (
            f"Address {addr}: "
            f"Expected 0x{expected:08X}, "
            f"Got 0x{actual:08X}"
        )

    cocotb.log.info(
        "Stress back-to-back test PASSED."
    )