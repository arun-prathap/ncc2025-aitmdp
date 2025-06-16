# ncc2025-aitmdp
Simulation Code for National Conference on Communications (NCC) 2025 paper ["On Resource Allocation for Remote Control of MDPs Over Queues Using Age-of-Loop"](https://doi.org/10.1109/NCC63735.2025.10982939)

### Code for Analytical and Simulation Results
The components of the code made publicly available for reproducing results from the paper are explained below.

#### System Model and associated components
The basic building blocks used in simulation are available in blocks/.

```bash
├── blocks/
│   ├── queue.py (models a data structure configurable as FIFO/LIFO)
│   ├── linkwithqueue.py (Models a link with queue having probabilistic admission and service)
│   ├── mdplantmodel.py (MDP Plant Model)
│   ├── mdpcontroller.py (AIT-MDP RemoteML controller as described in the paper)
│   ├── mdpsystem_mod.py (Implementation of Constrained system as described in the paper)
│   ├── mdpsystem.py (Implementation of Relaxed system as described in the paper)
```

#### Running the Code for Simulations/Analytical Results

In generate_data.py file, uncomment the line corresponding to the data you want to generate  (import gen_data.fig_\* corresponding to your requirement). This tweak is done since the execution times may vary depending on the chosen episode lengths and number of steps in simulations and hence it is recommended to execute the simulations independently. (The parameter that can be adjusted to reduce/increase number of simulation steps/runs and the values used for results in the paper corresponding to files in gen_data/ is included in brackets in list below, if applicable)

Execute the python file generate_data.py from the root directory of the repository. 

The output is dumped as json files in sim/sim\*.json which can be used to generate the plots or compared with the author's results available in jsons/sim\*.json.

```bash
├── generate_data.py
├── utils/util.py
├── gen_data/
│   ├── fig_3_6.py (max_steps=100000 in generate_data())
│   ├── fig_4_sim_constrained.py (NO_OF_SIMULATIONS=1000 and NO_OF_STEPS=10000)
│   ├── fig_4_analytical.py
│   ├── fig_5a_5b_analytical.py (the code is more or less same as fig_4_analytical.py--can be clubbed)
│   ├── fig_7a_analytical.py
│   ├── fig_7a_sim_constrained.py (NO_OF_SIMULATIONS=1000 and NO_OF_STEPS=10000)
│   ├── fig_7a_sim_relaxed.py (NO_OF_SIMULATIONS=1000 and NO_OF_STEPS=10000)
│   ├── fig_7b.py
│   ├── fig_8a.py
│   ├── fig_8b.py
├── sim/
│   ├── sim*.json (data corresponding to plots in the paper, after executing generate_data.py)
```

The generation of random TPMs uses [Markov Decision Process (MDP) Toolbox for Python](https://pymdptoolbox.readthedocs.io/en/latest/). Other package requirements like os, json, numpy, pandas, random, etc. are commonly available in any conda-like distribution. 

### Generating plots in the publication

Execute the python file generate_figures.py from the root directory of the repository. (The figures are not included as such in repo since the copyright has been transferred to IEEE for publication) 

The generated plots can be found in img/. 

The code for fetching data from jsons/\*.json and converting to dictionary for plotting is available in gen_figures/\*.py from which plots are generated with plotfigure function in utils/plot_from_dicts.py. 

```bash
├── generate_figures.py
├── utils/plot_from_dicts.py
├── jsons/
│   ├── sim*.json (data used for plots in the paper)
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
