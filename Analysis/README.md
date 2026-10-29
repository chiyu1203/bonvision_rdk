# General information about coding environment.
While the stimulus code was made in Bonsai, the analysis code was written in Python.
I have used the following two package managers to install python packages.

## How to set up an virtual environment in python with package manager tool conda

This part is the same as any general guidance about conda and anaconda online.
Since it is a popular package managers, I will skip the explanation.
Install the latest anaconda version for your operating system (https://www.anaconda.com/products/individual) and open the anaconda prompt

If you prefer to to use environment.yml or requirements.txt files to install the packages on the list:
```
conda env create -f environment.yml
conda create --name analysis --file requirements.txt
```
Then activate your virtual environment.

```
Otherwise, use the following commands to create a virtual environment and intall python packages inside the environment.
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

Then you are ready to go.

To run the marimo notebook, first ensure you are in the virtual environment.
Then type the following
```
#to enter editor-only mode
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

To initiate a python project with uv inside an existing folder. In this case, "Analysis"

use 
```
uv init
```
but since this repository have stored the configuration, you can just type the following. It will create a virtual environment using python 3.14 and installed packages listed up in pyproject.
```
uv run --locked --python 3.14 marimo edit notebook.py
```

It seems that there is no need to create a virtual environment inside the project to isolate its python environment from outside, since uv project manages which python to use already. However, I wanted to follow my old practice and having a virtual environment inside a uv project does not harm anything. Therefore, the following command can be used.
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
```
To run marimo notebook within the project
```
uv run marimo edit .\notebook.py
```