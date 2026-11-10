# Fe-Ni MACE-sqs: model, DFT training data and analysis files

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23484911.svg)](https://doi.org/10.5281/zenodo.23484911)
[![arXiv](https://img.shields.io/badge/arXiv-2605.28395-b31b1b.svg)](https://arxiv.org/abs/2605.28395)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

Companion repository for the paper

> **Capabilities and Limitations of MACE Interatomic Potentials for Fe–Ni Alloys: A Systematic Benchmark**
> Kushal Ramakrishna, Mani Lokamani, Attila Cangi
> Helmholtz-Zentrum Dresden-Rossendorf (HZDR)
> *Modelling and Simulation in Materials Science and Engineering* (in press)
> Preprint: [arXiv:2605.28395](https://arxiv.org/abs/2605.28395)

The archived data and model live on Zenodo at
[doi.org/10.5281/zenodo.23484911](https://doi.org/10.5281/zenodo.23484911).
This repository mirrors the record metadata and provides a script to fetch and verify the files.
The trained model (1.5 GB) exceeds GitHub's file size limits, so Zenodo remains the canonical archive.

## Overview

We benchmark MACE machine-learned interatomic potentials for iron-nickel alloys across structural, elastic, magnetic and finite-temperature properties relevant to phase stability.
A system-specific **MACE-sqs** model is trained on spin-polarized PBE DFT data for chemically disordered special quasirandom structures (SQS) spanning composition, bcc and fcc lattices, and volumetric and shear deformations.
It reaches validation errors of 2.0 meV/atom (energies) and 24.3 meV/Å (forces) and is compared against several MACE foundation models, including Hubbard-U trained variants.

Key findings:

- MACE-sqs gives the most consistent agreement with DFT and experiment for equations of state, equilibrium volumes, elastic constants and thermal expansion trends in bcc and fcc Fe-Ni.
- For the bcc to hcp transition, MACE-sqs predicts a pure-Fe transition pressure closer to experiment than the foundation models.
- All tested models predict an incorrect increase of the transition pressure with Ni content, pointing to high-pressure magnetic collapse as an open challenge for MLIPs.

## Contents of the Zenodo record

| File | Size | Description |
|---|---|---|
| `MACE-sqs.model` | 1.5 GB | Trained MACE-sqs interatomic potential for Fe-Ni |
| `FeNi_train.xyz` | 61.4 MB | DFT-PBE training set, 5115 configurations (extended XYZ) |
| `FeNi_val.xyz` | 15.1 MB | DFT-PBE validation set, 1274 configurations (extended XYZ) |
| `sro_data.zip` | 379 kB | SQS structures and Warren-Cowley short-range-order analysis |
| `magnetic_moment.zip` | 3.6 kB | DFT-PBE and experimental magnetic moments vs. composition |
| `vasp_example_FeNi_fcc_n108.zip` | 26.8 kB | Complete VASP input example (fcc, 108 atoms) |
| `scripts.zip` | 66.2 kB | Analysis scripts |
| `notebooks.zip` | 166.5 kB | Jupyter notebooks for the analyses and figures |
| `README.md` | 10.9 kB | Detailed file layout, data formats and DFT settings |

Training cells contain 54, 108, 128 and 250 atoms.
MD5 checksums are listed in [`checksums.md5`](checksums.md5).

## Getting the data

```bash
git clone https://github.com/gyro555in/fe-ni-mace-sqs.git
cd fe-ni-mace-sqs

# everything (about 1.6 GB)
python download_data.py

# skip the 1.5 GB model, fetch only data, scripts and notebooks
python download_data.py --skip-model
```

Files are saved to `data/`, verified against the published MD5 checksums, and the zip archives are extracted.
The script only needs the Python standard library.

## Using the model

```python
from ase.build import bulk
from mace.calculators import MACECalculator

calc = MACECalculator(model_paths="data/MACE-sqs.model", device="cuda", default_dtype="float64")

atoms = bulk("Fe", "bcc", a=2.83, cubic=True).repeat((3, 3, 3))
atoms.calc = calc
print(atoms.get_potential_energy() / len(atoms), "eV/atom")
```

## Software

| Package | Version |
|---|---|
| VASP (DFT reference) | 6.5.1 |
| ASE | 3.25.0 |
| mace-torch | 0.3.13 |
| torch-sim-atomistic | 0.2.1 |

## Citation

If you use the model or data, please cite both the paper and the dataset.
GitHub's "Cite this repository" button uses [`CITATION.cff`](CITATION.cff).

```bibtex
@misc{ramakrishna2026fenimace_data,
  author    = {Ramakrishna, Kushal and Lokamani, Mani and Cangi, Attila},
  title     = {Fe--Ni MACE-sqs: model, DFT training data and analysis files},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23484911},
  url       = {https://doi.org/10.5281/zenodo.23484911}
}

@article{ramakrishna2026fenimace,
  author  = {Ramakrishna, Kushal and Lokamani, Mani and Cangi, Attila},
  title   = {Capabilities and Limitations of {MACE} Interatomic Potentials for {Fe--Ni} Alloys: A Systematic Benchmark},
  journal = {Modelling and Simulation in Materials Science and Engineering},
  year    = {2026},
  note    = {in press, arXiv:2605.28395}
}
```

## License

Data, model and documentation are released under [CC BY 4.0](LICENSE), matching the Zenodo record.

## Contact

Kushal Ramakrishna, HZDR ([ORCID 0000-0003-4211-2484](https://orcid.org/0000-0003-4211-2484))
