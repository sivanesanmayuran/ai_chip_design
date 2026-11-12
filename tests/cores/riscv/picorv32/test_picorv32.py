"""cocotb testbench for PicoRV32 (native memory interface).

A Python memory model serves instruction fetches and data accesses. A small
RV32I program is assembled with the helper encoders below, run on the core,
and results are checked in the memory model.
"""
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge

# ---------------- minimal RV32I encoders ----------------


def i_type(op, f3, rd, rs1, imm):
    return ((imm & 0xFFF) << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | op


def r_type(f7, f3, rd, rs1, rs2):
    return (f7 << 25) | (rs2 << 20) | (rs1 << 15) | (f3 << 12) | (rd << 7) | 0x33


def s_type(f3, rs1, rs2, imm):
    return (((imm >> 5) & 0x7F) << 25) | (rs2 << 20) | (rs1 << 15) | \
        (f3 << 12) | ((imm & 0x1F) << 7) | 0x23


def addi(rd, rs1, imm): return i_type(0x13, 0, rd, rs1, imm)
def add(rd, rs1, rs2): return r_type(0x00, 0, rd, rs1, rs2)
def sub(rd, rs1, rs2): return r_type(0x20, 0, rd, rs1, rs2)
def lw(rd, rs1, imm): return i_type(0x03, 2, rd, rs1, imm)
def sw(rs2, rs1, imm): return s_type(2, rs1, rs2, imm)
def sb(rs2, rs1, imm): return s_type(0, rs1, rs2, imm)


def jal_self(): return 0x0000006F  # jal x0, 0 (infinite loop)


# ---------------- memory model ----------------

class Memory:
    def __init__(self, program):
        self.words = {4 * i: w for i, w in enumerate(program)}
        self.writes = []

    def read(self, addr):
        return self.words.get(addr & ~3, 0)

    def write(self, addr, data, strb):
        a = addr & ~3
        old = self.words.get(a, 0)
        for b in range(4):
            if strb & (1 << b):
                old = (old & ~(0xFF << 8 * b)) | (data & (0xFF << 8 * b))
        self.words[a] = old
        self.writes.append((a, old))


def sig(handle, default=0):
    """Read a signal as int; return default while it is X/Z (e.g. before reset)."""
    v = handle.value
    return int(v) if v.is_resolvable else default


async def mem_model(dut, mem):
    """One-cycle-latency memory: respond the cycle after mem_valid is seen."""
    ready = 0
    while True:
        await RisingEdge(dut.clk)
        if sig(dut.mem_valid) and not ready:
            addr = int(dut.mem_addr.value)
            strb = int(dut.mem_wstrb.value)
            if strb:
                mem.write(addr, int(dut.mem_wdata.value), strb)
            dut.mem_rdata.value = mem.read(addr)
            dut.mem_ready.value = 1
            ready = 1
        else:
            dut.mem_ready.value = 0
            ready = 0


async def start(dut, program):
    mem = Memory(program)
    dut.resetn.value = 0
    dut.mem_ready.value = 0
    dut.mem_rdata.value = 0
    dut.irq.value = 0
    dut.pcpi_wr.value = 0
    dut.pcpi_rd.value = 0
    dut.pcpi_wait.value = 0
    dut.pcpi_ready.value = 0
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    cocotb.start_soon(mem_model(dut, mem))
    for _ in range(5):
        await RisingEdge(dut.clk)
    dut.resetn.value = 1
    return mem


async def run_until(dut, cond, max_cycles=2000):
    for _ in range(max_cycles):
        await RisingEdge(dut.clk)
        assert sig(dut.trap) == 0, "core trapped"
        if cond():
            return
    raise AssertionError("timeout waiting for condition")


# ---------------- tests ----------------

@cocotb.test()
async def test_alu_and_store(dut):
    """5 + 7 = 12, 12 - 5 = 7, both stored to memory."""
    prog = [
        addi(1, 0, 5),
        addi(2, 0, 7),
        add(3, 1, 2),
        sub(4, 3, 1),
        sw(3, 0, 0x100),
        sw(4, 0, 0x104),
        jal_self(),
    ]
    mem = await start(dut, prog)
    await run_until(dut, lambda: 0x104 in mem.words)
    assert mem.words[0x100] == 12
    assert mem.words[0x104] == 7


@cocotb.test()
async def test_load_store_roundtrip(dut):
    """Preload data, load it, add 1, store back; also check byte strobe."""
    prog = [
        lw(1, 0, 0x200),
        addi(1, 1, 1),
        sw(1, 0, 0x204),
        addi(2, 0, 0xAB),
        sb(2, 0, 0x209),     # byte lane 1 of word 0x208
        jal_self(),
    ]
    mem = await start(dut, prog)
    mem.words[0x200] = 0x1234
    mem.words[0x208] = 0
    await run_until(dut, lambda: any(a == 0x208 for a, _ in mem.writes))
    assert mem.words[0x204] == 0x1235
    assert mem.words[0x208] == 0xAB00
