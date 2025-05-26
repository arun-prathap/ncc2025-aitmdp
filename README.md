# ncc2025-aitmdp
Simulation Code for NCC 2025 paper "On Resource Allocation for Remote Control of MDPs Over Queues Using Age-of-Loop"

Update as on 26 May 2025 : Made repo public, code for generating plots in publication are uploaded, simulation code will be available here by May 31, 2025.

### Generating plots in the publication

Run generate_figures.py from the home directory. The generated plots can be found in img directory. The code for fetching data from data in jsons folder is in gen_figures directory and figures are generated using plotfigure function in utils/plot_from_dicts.py. The generation of plots uses [SciencePlots](https://github.com/garrettj403/SciencePlots) and requires a working Latex installation.

## Publication
If you find the repository useful, please cite the [paper](https://doi.org/10.1109/NCC63735.2025.10982939):
```
Arun P. R., Minha Mubarak and Vineeth B. S.,
"On Resource Allocation for Remote Control of MDPs Over Queues using Age-of-Loop,"
2025 National Conference on Communications (NCC), New Delhi, India, 2025, pp. 1-6,
doi: 10.1109/NCC63735.2025.10982939.
