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
    Stress test:
    - No idle cycles between APB transactions
    - Write all locations
    - Read all locations
    - Verify data integrity
    
    
    
    """
    
    
    cocotb.start_soon(
        Clock(dut.pclk, 10, units="ns").start()
    )

    dut.presetn.value = 0

    await reset_dut(dut)
    
    
    await RisingEdge(dut.pclk)
    await RisingEdge(dut.pclk)

    # -----------------------------
    # Back-to-back writes
    # -----------------------------

    for addr in range(16):

        data = (addr * 3) & 0xFF

        await apb_write(
            dut,
            addr,
            data
        )
        
        cocotb.log.info(
    f"MEM0={int(dut.dut.mem[0].value)} "
    f"MEM1={int(dut.dut.mem[1].value)} "
    f"MEM2={int(dut.dut.mem[2].value)}"
)

    # -----------------------------
    # Back-to-back reads
    # -----------------------------

    for addr in range(16):

        expected = (addr * 3) & 0xFF

        actual = await apb_read(
            dut,
            addr
        )
        
        

        assert actual == expected, (
            f"Address {addr}: "
            f"Expected 0x{expected:02X}, "
            f"Got 0x{actual:02X}"
        )

    cocotb.log.info("test_stress_back2back PASSED")
