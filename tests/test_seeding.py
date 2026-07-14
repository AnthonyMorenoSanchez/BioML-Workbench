import random

from bioml_workbench.utils.seeding import SeedManager


def test_seed_manager_reproducibility() -> None:
    manager = SeedManager(seed=12345)
    manager.apply()
    first = random.randint(0, 1000000)

    manager.apply()
    second = random.randint(0, 1000000)

    assert first == second
