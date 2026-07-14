import random

import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_random_basic(dut):
    """
    Random Basic Test

    Verification Objective:
        Perform randomized legal APB writes and reads and verify
        that every read returns the expected value.
    """

    cocotb.start_soon(Clock(dut.pclk, 10, units="ns").start())

    cocotb.log.info("========== RANDOM BASIC TEST ==========")

    await reset_dut(dut)

    # Fixed seed makes failures reproducible.
    seed = 12345
    random.seed(seed)

    cocotb.log.info(f"Random seed = {seed}")

    # Python reference model:
    # address -> expected stored data
    expected_memory = {
        addr: 0x00000000 for addr in range(32)
    }

    number_of_transactions = 100

    for transaction in range(number_of_transactions):

        addr = random.randint(0, 31)
        operation = random.choice(["WRITE", "READ"])

        if operation == "WRITE":

            data = random.randint(0, 0xFFFFFFFF)

            cocotb.log.info(
                f"TXN={transaction:03d} "
                f"WRITE ADDR={addr:02d} "
                f"DATA=0x{data:08X}"
            )

            await apb_write(dut, addr, data)

            # Update expected value after the DUT write.
            expected_memory[addr] = data

        else:

            expected_data = expected_memory[addr]

            read_data = await apb_read(dut, addr)

            cocotb.log.info(
                f"TXN={transaction:03d} "
                f"READ ADDR={addr:02d} "
                f"EXPECTED=0x{expected_data:08X} "
                f"ACTUAL=0x{read_data:08X}"
            )

            assert read_data == expected_data, (
                f"Random read mismatch during transaction {transaction}. "
                f"Address={addr}, "
                f"Expected=0x{expected_data:08X}, "
                f"Received=0x{read_data:08X}, "
                f"Seed={seed}"
            )

    cocotb.log.info(
        f"PASS: Completed {number_of_transactions} randomized transactions."
    )