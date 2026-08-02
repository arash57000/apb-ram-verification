import random

import cocotb
from cocotb.clock import Clock

from .tb_utils import (
    reset_dut,
    apb_write,
    apb_read,
)


@cocotb.test()
async def test_random_memory_sweep(dut):
    """
    Random Test

    Run a long sequence of random legal APB reads and writes,
    then verify every RAM location against a reference model.

    Expected:
        - Random reads match the reference model
        - Random writes update the reference model
        - Final sweep of all 32 addresses matches the model
    """

    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    await reset_dut(dut)

    num_transactions = 500

    # Software reference model of the 32-word RAM.
    # RAM is expected to contain zeros after reset.
    reference_model = [0] * 32

    cocotb.log.info(
        f"\n=== Random Memory Sweep Test: "
        f"{num_transactions} Transactions ==="
    )

    # -------------------------------------------------
    # Random traffic
    # -------------------------------------------------

    for transaction in range(num_transactions):

        operation = random.choice(["READ", "WRITE"])
        addr = random.randint(0, 31)

        # -------------------------------------------------
        # Random WRITE
        # -------------------------------------------------

        if operation == "WRITE":

            data = random.getrandbits(32)

            cocotb.log.info(
                f"RANDOM WRITE "
                f"#{transaction:03d} "
                f"ADDR={addr:02d} "
                f"DATA=0x{data:08X}"
            )

            await apb_write(
                dut,
                addr,
                data,
            )

            # Update expected RAM contents
            reference_model[addr] = data

        # -------------------------------------------------
        # Random READ
        # -------------------------------------------------

        else:

            expected_data = reference_model[addr]

            read_data = await apb_read(
                dut,
                addr,
            )

            cocotb.log.info(
                f"RANDOM READ  "
                f"#{transaction:03d} "
                f"ADDR={addr:02d} "
                f"EXPECTED=0x{expected_data:08X} "
                f"GOT=0x{read_data:08X}"
            )

            assert read_data == expected_data, (
                f"Random read mismatch! "
                f"Transaction={transaction} "
                f"Address={addr} "
                f"Expected=0x{expected_data:08X} "
                f"Got=0x{read_data:08X}"
            )

    # -------------------------------------------------
    # Final full-memory verification
    # -------------------------------------------------

    cocotb.log.info(
        "\n=== Final 32-Address Memory Sweep ==="
    )

    for addr in range(32):

        expected_data = reference_model[addr]

        read_data = await apb_read(
            dut,
            addr,
        )

        cocotb.log.info(
            f"SWEEP "
            f"ADDR={addr:02d} "
            f"EXPECTED=0x{expected_data:08X} "
            f"GOT=0x{read_data:08X}"
        )

        assert read_data == expected_data, (
            f"Final memory sweep mismatch! "
            f"Address={addr} "
            f"Expected=0x{expected_data:08X} "
            f"Got=0x{read_data:08X}"
        )

    cocotb.log.info(
        f"PASS: {num_transactions} random transactions "
        f"and final 32-address memory sweep completed successfully."
    )