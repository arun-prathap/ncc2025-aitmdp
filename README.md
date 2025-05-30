# ncc2025-aitmdp
Simulation Code for National Conference on Communications (NCC) 2025 paper ["On Resource Allocation for Remote Control of MDPs Over Queues Using Age-of-Loop"](https://doi.org/10.1109/NCC63735.2025.10982939)

Update as on 30 May 2025 : Made repo public, code for generating plots in publication are uploaded, simulation code will be available here by Jun 10, 2025.

### Code for Analytical and Simulation Results

The output is dumped in json files which are used to generate the plots.

### Generating plots in the publication

Run generate_figures.py from the root directory of the repository. (The figures are not included as such in repo since the copyright has been transferred to IEEE for publication) 

The generated plots can be found in img/. 

The code for fetching data from jsons/\*.json and converting to dictionary for plotting is available in gen_figures/\*.py from which plots are generated with plotfigure function in utils/plot_from_dicts.py. 

```bash
├── generate_figures.py
├── utils/plot_from_dicts.py
├── jsons/
│   ├── sim*.json
├── gen_figures/
│   ├── fig*.py
├── img/
│   ├── fig*.pdf (after executing generate_figures.py)
```

The generation of plots uses [SciencePlots](https://github.com/garrettj403/SciencePlots) and requires a working Latex installation.

## Publication
If you find the repository useful, please cite the [paper](https://doi.org/10.1109/NCC63735.2025.10982939):
```
Arun P. R., Minha Mubarak and Vineeth B. S.,
"On Resource Allocation for Remote Control of MDPs Over Queues using Age-of-Loop,"
2025 National Conference on Communications (NCC), New Delhi, India, 2025, pp. 1-6,
doi: 10.1109/NCC63735.2025.10982939.
