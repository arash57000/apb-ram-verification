import random

import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
    apb_write_expect_error,
    apb_read_expect_error,
)


@cocotb.test()
async def test_random_illegal_access(dut):
    """
    Random Test

    Generate random illegal APB read and write accesses.

    Expected:
        - Every illegal access produces PSLVERR
        - DUT remains operational after repeated errors
        - Periodic legal accesses still succeed
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    num_transactions = 100

    cocotb.log.info(
        f"\n=== Random Illegal Access Test: "
        f"{num_transactions} Transactions ==="
    )

    # -------------------------------------------------
    # Random illegal traffic
    # -------------------------------------------------

    for transaction in range(num_transactions):

        operation = random.choice(["READ", "WRITE"])
        addr = random.randint(32, 255)

        # -------------------------------------------------
        # Random illegal WRITE
        # -------------------------------------------------

        if operation == "WRITE":

            data = random.getrandbits(32)

            cocotb.log.info(
                f"RANDOM ILLEGAL WRITE "
                f"#{transaction:03d} "
                f"ADDR={addr:03d} "
                f"DATA=0x{data:08X}"
            )

            await apb_write_expect_error(
                dut,
                addr,
                data,
            )

        # -------------------------------------------------
        # Random illegal READ
        # -------------------------------------------------

        else:

            cocotb.log.info(
                f"RANDOM ILLEGAL READ  "
                f"#{transaction:03d} "
                f"ADDR={addr:03d}"
            )

            await apb_read_expect_error(
                dut,
                addr,
            )

        # -------------------------------------------------
        # Periodic legal recovery check
        # -------------------------------------------------

        if (transaction + 1) % 10 == 0:

            legal_addr = random.randint(0, 31)
            legal_data = random.getrandbits(32)

            cocotb.log.info(
                f"RECOVERY CHECK "
                f"ADDR={legal_addr:02d} "
                f"DATA=0x{legal_data:08X}"
            )

            await apb_write(
                dut,
                legal_addr,
                legal_data,
            )

            read_data = await apb_read(
                dut,
                legal_addr,
            )

            assert read_data == legal_data, (
                f"Recovery check failed! "
                f"After illegal transaction #{transaction} "
                f"Address={legal_addr} "
                f"Expected=0x{legal_data:08X} "
                f"Got=0x{read_data:08X}"
            )

    cocotb.log.info(
        f"PASS: {num_transactions} random illegal accesses "
        f"completed with successful periodic recovery checks."
    )