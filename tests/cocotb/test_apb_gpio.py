import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


async def apb_write(dut, addr, data):
    dut.psel.value = 1
    dut.pwrite.value = 1
    dut.paddr.value = addr
    dut.pwdata.value = data
    dut.penable.value = 0
    await RisingEdge(dut.pclk)
    dut.penable.value = 1
    await RisingEdge(dut.pclk)
    dut.psel.value = 0
    dut.penable.value = 0


async def apb_read(dut, addr):
    dut.psel.value = 1
    dut.pwrite.value = 0
    dut.paddr.value = addr
    dut.penable.value = 0
    await RisingEdge(dut.pclk)
    dut.penable.value = 1
    await RisingEdge(dut.pclk)
    val = int(dut.prdata.value)
    dut.psel.value = 0
    dut.penable.value = 0
    return val


@cocotb.test()
async def test_rw(dut):
    cocotb.start_soon(Clock(dut.pclk, 10, unit="ns").start())
    dut.presetn.value = 0
    dut.psel.value = 0
    dut.penable.value = 0
    dut.pwrite.value = 0
    dut.gpio_in.value = 0xA5
    for _ in range(3):
        await RisingEdge(dut.pclk)
    dut.presetn.value = 1
    await RisingEdge(dut.pclk)

    await apb_write(dut, 0x0, 0x3C)
    assert int(dut.gpio_out.value) == 0x3C
    assert await apb_read(dut, 0x0) == 0x3C
    await apb_write(dut, 0x4, 0xFF)
    assert int(dut.gpio_dir.value) == 0xFF
    assert await apb_read(dut, 0x8) == 0xA5
