from __future__ import annotations

import os
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class SeedManager:
    """Manage reproducible random seeds."""

    seed: int = 42

    def apply(self) -> None:
        """Apply the configured seed to supported Python randomness sources."""

        os.environ["PYTHONHASHSEED"] = str(self.seed)
        random.seed(self.seed)

        try:
            import numpy as np  # type: ignore[import]

            np.random.seed(self.seed)
        except ImportError:
            pass

    def with_seed(self, seed: int) -> "SeedManager":
        """Return a new manager configured with a different seed."""

        return SeedManager(seed=seed)
