# SPDX-License-Identifier: Apache-2.0
"""Locate the pipeline's data files in a checkout or an installed package.

In a checkout, prompts/, frameworks/, schemas/ and config/ sit next to lsb/.
An installed wheel carries copies under lsb/data/ (see pyproject.toml).
"""

from __future__ import annotations

from pathlib import Path


def is_checkout() -> bool:
    """True when lsb/ is running from a repository checkout."""
    return (Path(__file__).resolve().parents[1] / "prompts").is_dir()


def resource_root() -> Path:
    """The directory holding prompts/, frameworks/, schemas/ and config/."""
    checkout = Path(__file__).resolve().parents[1]
    if (checkout / "prompts").is_dir():
        return checkout
    import importlib.resources as res

    data = res.files("lsb") / "data"
    if isinstance(data, Path) and (data / "prompts").is_dir():
        return data
    raise SystemExit("pipeline data files not found; reinstall lesson-scaffold-builder")
