from pathlib import Path

import pytest
import papermill as pm

from time import time

NB_TRANSIENT_DIR = Path.cwd().parent.parent / "docs/transient"

def get_notebooks() -> list[Path]:
    skip = ["besselaesnew_timing.ipynb"]
    NB_TRANSIENT_DIRS = [
        NB_TRANSIENT_DIR / "00userguide",
        NB_TRANSIENT_DIR / "02examples",
        NB_TRANSIENT_DIR / "03xsections",
        NB_TRANSIENT_DIR / "05benchmarks",
    ]

    nblist = []
    for nbdir in NB_TRANSIENT_DIRS:
        nblist += [nb for nb in nbdir.glob("*.ipynb") if nb.name not in skip]
    return sorted(nblist)

PARAMETERS = {
    "meandering_river.ipynb": {"NGR": 2},
    "horizontal_well.ipynb": {"N": 2},
}

# @pytest.mark.notebooks
@pytest.mark.skip(reason="Use pytest --nbval on notebooks directly for coverage.")
@pytest.mark.parametrize("pth", get_notebooks())
def test_notebook(pth):
    input_path = pth
    output_path = pth.with_suffix(".out.ipynb")
    pm.execute_notebook(
        input_path,
        str(output_path),
        timeout=600,
        cwd=pth.parent,
        parameters = PARAMETERS.get(pth.name)
    )
    output_path.unlink()  # Remove the output notebook after execution

if __name__ == "__main__":
    for file in get_notebooks():
        start = time()
        test_notebook(file)
        end = time()
        print(f"Execution time for {file}: {end - start:.2f} seconds")