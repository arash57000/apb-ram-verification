import cocotb
import random
import os


def init_seed(dut, seed=None):
    """
    Initialize deterministic random seed.
    Priority:
        1) Explicit argument
        2) ENV: DV_SEED
        3) cocotb RANDOM_SEED
        4) system random
    """

    if seed is None:
        # ENV override
        if "DV_SEED" in os.environ:
            seed = int(os.environ["DV_SEED"])
        # cocotb seed
        elif "RANDOM_SEED" in os.environ:
            seed = int(os.environ["RANDOM_SEED"])
        else:
            seed = random.randint(1, 2**31 - 1)

    random.seed(seed)

    dut._log.info(f"[SEED] Regression seed = {seed}")
    return seed

