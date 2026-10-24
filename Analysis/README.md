# General information about coding environment.

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
```
uv init
```

It seems that there is no need to create a virtual environment inside the project to isolate its python environment from outside, since uv project manages which python to use already. However, it also seems that using a python virtual environment inside a uv project does not harm anything. Therefore, the following command can be used.
```
uv venv --python 3.14  
```
To activate the virtual environment:
```
## on Windows
.\.venv\Scripts\activate 

## on Mac/Linux
source .\.venv\bin\activate
```
To add python dependencies inside the project
```
uv add scipy pandas matplotlib pyarrow fastparquet deepdiff tables ipyparallel seaborn h5py reliability marimo numpy zenodo-get
```
To run marimo notebook within the project
```
uv run marimo edit .\notebook.py
```