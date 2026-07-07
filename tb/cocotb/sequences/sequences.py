import random
from tb.cocotb.env.log import dv_log


# ============================================================
# Base Sequence
# ============================================================
class BaseSequence:
    """
    UVM-like base sequence
    """

    def __init__(self, env, name="BASE_SEQ"):
        self.env = env
        self.drv = env.driver
        self.log = dv_log(env.dut, name)

    async def run(self):
        raise NotImplementedError("Sequence must implement run()")


# ============================================================
# Directed Sequence
# ============================================================
class DirectedSequence(BaseSequence):
    """
    Deterministic functional checks
    """

    def __init__(self, env):
        super().__init__(env, name="DIR_SEQ")

    async def run(self):
        self.log.info("Starting DirectedSequence")

        await self.drv.reset()

        # basic
        await self.drv.write(12, 0x23)
        await self.drv.read(12)

        # boundaries
        await self.drv.write(0, 0x1111)
        await self.drv.read(0)

        await self.drv.write(31, 0x2222)
        await self.drv.read(31)

        # illegal
        await self.drv.write(45, 0x3333)
        await self.drv.read(45)

        self.log.info("DirectedSequence complete")


# ============================================================
# Random Sequence
# ============================================================
class RandomSequence(BaseSequence):
    """
    Constrained-random traffic
    """

    def __init__(self, env, iterations=200):
        super().__init__(env, name="RAND_SEQ")
        self.iterations = iterations

    async def run(self):
        self.log.info(f"Starting RandomSequence ({self.iterations} iters)")

        for _ in range(self.iterations):

            # reset injection
            if random.random() < 0.05:
                await self.drv.reset()
                continue

            # address space
            if random.random() < 0.8:
                addr = random.randint(0, 31)
            else:
                addr = random.randint(32, 63)

            # operation
            if random.random() < 0.6:
                data = random.getrandbits(32)
                await self.drv.write(addr, data)
            else:
                await self.drv.read(addr)

        self.log.info("RandomSequence complete")


# ============================================================
# Reset Stress Sequence
# ============================================================
class ResetStressSequence(BaseSequence):
    """
    Reset robustness testing
    """

    def __init__(self, env, iterations=20):
        super().__init__(env, name="RST_SEQ")
        self.iterations = iterations

    async def run(self):
        self.log.info(f"Starting ResetStressSequence ({self.iterations} iters)")

        for _ in range(self.iterations):
            await self.drv.reset()
            await self.drv.write(random.randint(0, 31), random.getrandbits(32))
            await self.drv.reset()
            await self.drv.read(random.randint(0, 31))

        self.log.info("ResetStressSequence complete")

