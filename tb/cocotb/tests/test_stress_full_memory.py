import cocotb

from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_stress_full_memory(dut):
    """
    Stress Test

    Continuously write and verify all RAM locations
    over multiple full-memory cycles.

    Expected:
        - Every write succeeds
        - Every read returns the expected value
        - No corruption occurs during repeated operation
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    for iteration in range(100):

        #
        # Write entire memory
        #
        for addr in range(32):

            data = ((iteration << 8) | addr) & 0xFFFFFFFF

            await apb_write(
                dut,
                addr,
                data
            )

        #
        # Read back and verify
        #
        for addr in range(32):

            data = ((iteration << 8) | addr) & 0xFFFFFFFF

            actual = await apb_read(
                dut,
                addr
            )

            assert actual == data, (
                f"Iteration {iteration}, "
                f"Address {addr}: "
                f"Expected 0x{data:08X}, "
                f"Got 0x{actual:08X}"
            )

        if (iteration + 1) % 20 == 0:

            cocotb.log.info(
                f"Completed {iteration + 1} full-memory cycles"
            )

    cocotb.log.info(
        "Stress full-memory test PASSED."
    )