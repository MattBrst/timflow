from pathlib import Path

import pytest
import papermill as pm

nbdirs = [
    Path("docs/steady/00userguide/tutorials"),
    Path("docs/steady/00userguide/howtos"),
    Path("docs/steady/02examples"),
    Path("docs/steady/03xsections"),
    Path("docs/steady/04benchmarks"),
]


def get_notebooks() -> list[Path]:
    skip = ["benchmarking_besselaes.ipynb", "vertical_anisotropy.ipynb"]
    nblist = []
    for nbdir in nbdirs:
        nblist += [nb for nb in nbdir.glob("*.ipynb") if nb.name not in skip]
    return nblist


# @pytest.mark.notebooks
@pytest.mark.skip(reason="Use pytest --nbval on notebooks directly for coverage.")
@pytest.mark.parametrize("pth", get_notebooks())
def test_notebook(pth) -> None:
    pth = Path(pth)
    pm.execute_notebook(
        pth,
        str(pth.with_suffix(".out.ipynb")),
        timeout=600,
    )

if __name__ == "__main__":
    for file in get_notebooks():
        test_notebook(file)
