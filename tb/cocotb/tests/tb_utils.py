# tb_utils.py

import cocotb

from cocotb.triggers import RisingEdge

from cocotb.triggers import ReadOnly


# -------------------------------------------------
# Reset

async def reset_dut(dut):

"""
Reset the DUT and initialize all APB interface signals.
"""

    dut.presetn.value = 0

    dut.psel.value    = 0
    dut.penable.value = 0
    dut.pwrite.value  = 0
    dut.paddr.value   = 0
    dut.pwdata.value  = 0

    for _ in range(5):
        await RisingEdge(dut.pclk)

    dut.presetn.value = 1

    await RisingEdge(dut.pclk)


# -------------------------------------------------
# APB Write

async def apb_write(dut, addr, data):

"""
Perform a single APB write transaction.
"""

    # Setup phase
    dut.psel.value    = 1
    dut.penable.value = 0
    dut.pwrite.value  = 1
    dut.paddr.value   = addr
    dut.pwdata.value  = data

    await RisingEdge(dut.pclk)

    # Access phase
    dut.penable.value = 1

    await RisingEdge(dut.pclk)

    # Return to idle
    dut.psel.value    = 0
    dut.penable.value = 0
    dut.pwrite.value  = 0
    
    await RisingEdge(dut.pclk)
    



# -------------------------------------------------
# APB Read

async def apb_read(dut, addr):

"""
Perform a single APB read transaction.

Returns:
    int: Data read from the requested address.
"""

    # Setup phase
    dut.psel.value    = 1
    dut.penable.value = 0
    dut.pwrite.value  = 0
    dut.paddr.value   = addr

    await RisingEdge(dut.pclk)

    # Access phase
    dut.penable.value = 1

    await RisingEdge(dut.pclk)
    
    await ReadOnly()

    data = int(dut.prdata.value)
    
    await RisingEdge(dut.pclk)

    # Return to idle
    dut.psel.value    = 0
    dut.penable.value = 0
    
    await RisingEdge(dut.pclk)


    cocotb.log.info(
    f"READ ADDR={addr:02d} DATA=0x{data:08X}"
    )

    return data


# -------------------------------------------------
# Initialize RAM with a known data pattern

async def initialize_memory_pattern(dut):
    """
    Initialize all RAM locations with a known pattern.

    Address 0  -> 0x00000001
    Address 1  -> 0x00000002
    ...
    Address 31 -> 0x00000020
    """

    cocotb.log.info("Initializing RAM with known data pattern...")

    for addr in range(32):

        data = addr + 1

        cocotb.log.info(
            f"WRITE ADDR={addr:02d} DATA=0x{data:08X}"
        )

        await apb_write(dut, addr, data)

    cocotb.log.info("RAM initialization complete.")

# -------------------------------------------------
# APB read and check PSLVERR
async def apb_read_expect_error(
    dut,
    addr,
):
    """
    Perform an illegal APB read.

    Expected:
        - PSLVERR asserted
        - Read transaction completes
    """

    dut.psel.value = 1
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.paddr.value = addr

    await RisingEdge(dut.pclk)

    dut.penable.value = 1

    while True:

        await RisingEdge(dut.pclk)

        if dut.pready.value:
            break

    assert dut.pslverr.value == 1, (
        f"Expected PSLVERR for illegal read "
        f"address {addr}"
    )

    dut.psel.value = 0
    dut.penable.value = 0

    await RisingEdge(dut.pclk)

# -------------------------------------------------
# APB Write and check PSLVERR

async def apb_write_expect_error(dut, addr, data):

"""
Perform an illegal APB write.

Returns:
    int: PSLVERR status from the transaction.
"""

    # Setup phase
    dut.psel.value    = 1
    dut.penable.value = 0
    dut.pwrite.value  = 1
    dut.paddr.value   = addr
    dut.pwdata.value  = data

    await RisingEdge(dut.pclk)

    # Access phase
    dut.penable.value = 1

    await RisingEdge(dut.pclk)

    # Sample DUT output after RTL updates complete
    await ReadOnly()

    err = int(dut.pslverr.value)

    # Advance to a writable phase before driving signals again
    await RisingEdge(dut.pclk)

    # Return to idle
    dut.psel.value    = 0
    dut.penable.value = 0
    dut.pwrite.value  = 0

    await RisingEdge(dut.pclk)

    return err


