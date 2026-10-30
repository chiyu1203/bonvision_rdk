# General information about this folder.
While the stimulus code was made in Bonsai, the analysis codes were written in Python.
They were tested under both Window 11 and MacOS, so as long as the coding environment is ready, the computer's operating system is not an issue.<br />

Here we will go through how to set up the coding environment in python
I have tested the following two package managers to manage virtual environments of python and install python packages.<br />

## How to set up an virtual environment in python with package manager tool conda

This part is the same as any general guidance about conda and anaconda online.
Since it is a popular package managers, I will skip the explanation.<br />
Install the latest anaconda version for your operating system (https://www.anaconda.com/products/individual) and open the anaconda prompt

If you prefer to to use environment.yml or requirements.txt files to install the packages on the list:
```
#choose one of the commends to create the virutla environment
conda env create -f environment.yml
conda create --name analysis --file requirements.txt
```
Then activate your virtual environment with 
```
conda activate analysis
```
Based on my experience, the requirements.txt file works better. Not sure if this is because I have installed packages via pip so some configuration in the environment.yml might be missing <br />
Alternatively, you can use the following commands to create a virtual environment and intall python packages inside the environment.
```
conda create --name analysis --channel conda-forge python=3.14
conda activate analysis
conda update -n base -c defaults conda
conda config --add channels conda-forge
conda install --yes -c conda-forge -v matplotlib seaborn pytables marimo fastparquet pyarrow numpy scipy pandas
```
Two packages are not stored in conda so we need to install them via pip
```
pip install reliability zenodo-get
```

Then you are ready to go.<br />

To run the marimo notebook, first ensure you have activate the virtual environment.
Then type the following
```
#to enter editor mode
marimo edit notebook.py
#to enter web app view-only mode
marimo run notebook.p
```

## How to set up an virtual environment in python with package manager tool uv
Installing uv in your local devices
```
## on Windows, open powershell, then type
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
## on Mac/Linux, open terminal, then type
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### For Windows users, if you receive this error, "running scripts is disabled on this system”,
then run in the powershell
```
Set-ExecutionPolicy -Scope CurrentUser 
Unrestricted
Y
```

This repository have stored the configuration to set up the virtual environment. Once the uv is installed in your computer, you can just type the following. It will create a virtual environment using python 3.14 and installed packages listed up in pyproject.<br />
```
uv run --locked --python 3.14 marimo edit .\notebook_curated_dataset.py
```

### Adding new packages in the uv project
It seems that there is no need to create a virtual environment inside the project to isolate its python environment from outside, since uv project manages which python to use already. However, I wanted to follow my old practice and having a virtual environment inside a uv project does not harm anything. Therefore, the following command can be used.<br />


[Optional]To initiate a python project with uv inside an existing folder, in this case, "Analysis"<br />
go to that folder and then type. This commend turns the folder into a uv folder by adding *uv.lock*, *pyproject.toml*, and *.python-version* files and a *src* folder
```
uv init
```
Once the project is created, type the following to create a virtual environment named "venv" wit python 3.14 version
```
uv venv --python 3.14  
```
To activate the virtual environment:
```
## on Windows
.\.venv\Scripts\activate 
## on Mac/Linux
source ./.venv/bin/activate
```
To add python dependencies inside the project
```
uv add scipy pandas matplotlib pyarrow fastparquet deepdiff tables ipyparallel seaborn h5py reliability marimo numpy zenodo-get

[Optional] To remove a python package from the project
```
uv remove h5py
```

[Optional] To synchronise you uv projeccts with added dependencies
```
uv sync
```

```
To run marimo notebook
```
uv run marimo edit .\notebook_curated_dataset.py
```
(useCtrl + C, to terminate an operating notebook)
