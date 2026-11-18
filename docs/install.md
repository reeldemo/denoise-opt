# Install

## Statistics scripts and tests

Python 3 with the standard library is enough. No packages need installing.

<!-- ci:run -->
```bash
python3 -m venv .venv
. .venv/bin/activate
python --version
```

## Experiment and plotting scripts

The scripts under `scripts/` that load models or draw figures import `numpy`, `scipy`, `matplotlib` and `torch`. They also need the ReelSynth repository on the Python path, see [reproduce](reproduce.md).

```bash
pip install -r requirements.txt
```

## PDF build

A TeX Live installation with `latexmk` and these packages: the ones named in `main.tex` (`algorithm`, `algpseudocode`, `tikz`, `orcidlink`, `hyperref`, `cite`, `xurl` and others). The class file `arxiv-twocolumn.sty` is in the repository.

## Build these docs

<!-- ci:run -->
```bash
pip install -r requirements-docs.txt
mkdocs build --strict
```

The site is not deployed. CI checks that it builds.
