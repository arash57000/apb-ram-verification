# tb_utils.py

import cocotb

from cocotb.triggers import RisingEdge

from cocotb.triggers import ReadOnly


# -------------------------------------------------
# Reset

async def reset_dut(dut):

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
    
    '''
    
   Why This Fix  adding extra await RisingEdge(dut.pclk)  at the end Works?

Each transaction becomes:

Cycle 1: SETUP
Cycle 2: ACCESS
Cycle 3: TRANSFER / cleanup

Your original helper only gave:

Cycle 1: SETUP
Cycle 2: ACCESS

So the next write started too early.

After editing tb_utils.py, run:

make stress 
    
    '''


# -------------------------------------------------
# APB Read

async def apb_read(dut, addr):

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
    f"READ ADDR={addr} DATA=0x{data:02X}"
    )

    return data

    '''
    
   Why This Fix  adding extra await RisingEdge(dut.pclk)  at the end Works?

Each transaction becomes:

Cycle 1: SETUP
Cycle 2: ACCESS
Cycle 3: TRANSFER / cleanup

Your original helper only gave:

Cycle 1: SETUP
Cycle 2: ACCESS

So the next write started too early.

After editing tb_utils.py, run:

make stress 
    
    '''

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
# APB Write and check PSLVERR

async def apb_write_expect_error(dut, addr, data):

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


# -------------------------------------------------
# APB Read and check PSLVERR

async def apb_read_expect_error(dut, addr):

    # Setup phase
    dut.psel.value    = 1
    dut.penable.value = 0
    dut.pwrite.value  = 0
    dut.paddr.value   = addr

    await RisingEdge(dut.pclk)

    # Access phase
    dut.penable.value = 1

    await RisingEdge(dut.pclk)

    # Sample outputs after RTL updates complete
    await ReadOnly()

    data = int(dut.prdata.value)
    err  = int(dut.pslverr.value)

    # Advance to a writable phase before cleanup
    await RisingEdge(dut.pclk)

    # Return to idle
    dut.psel.value    = 0
    dut.penable.value = 0

    await RisingEdge(dut.pclk)

    return data, err