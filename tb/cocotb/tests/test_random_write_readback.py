import random

import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_random_write_readback(dut):
    """
    Random Test

    Perform random legal APB writes followed immediately
    by reads from the same address.

    Expected:
        - Read data matches the data that was written
        - All transactions use legal addresses
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    num_transactions = 100

    for transaction in range(num_transactions):

        addr = random.randint(0, 31)
        data = random.getrandbits(32)

        cocotb.log.info(
            f"RANDOM WRITE/READ "
            f"#{transaction:03d} "
            f"ADDR={addr:02d} "
            f"DATA=0x{data:08X}"
        )

        await apb_write(
            dut,
            addr,
            data,
        )

        read_data = await apb_read(
            dut,
            addr,
        )

        assert read_data == data, (
            f"Random write/read mismatch! "
            f"Transaction={transaction} "
            f"Address={addr} "
            f"Expected=0x{data:08X} "
            f"Got=0x{read_data:08X}"
        )

    cocotb.log.info(
        f"PASS: {num_transactions} random write/read "
        f"transactions completed successfully."
    )