# General information about this folder.
While the stimulus code was made in Bonsai, the analysis codes were written in Python.
They were tested under both Window 11 and MacOS, so as long as the coding environment is ready, the computer's operating system is not an issue.<br />

Here we will go through how to set up the coding environment in python, and then open [marimo](https://docs.marimo.io/) notebook to access the data.<br />
Marimo notebook is similar to jupyter notebook, where you can interact with codes cell by cell (or block by block). Nevertheless, the biggest difference between the two is that Marimo notebook can automatically synchronise the value of global variables to all of the activated cells. This helps demonstrate a database like this, because you do not need to remember which cells to activate and which ones to skip. User feedback is updated automatically. However, jupyter notebook still has better support in other asepects but I found it trickier to prototype a script on Marimo (The promising thing is that Marimo has built up their APIs for users to convert notebooks from juypter notebook to Marimo notebook vice versa).

#### A useful tip for new Marimo notebook users: get used to local variables and global variables



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
marimo edit notebook_raw_dataset.py
#to enter web app view-only mode
marimo run notebook_raw_dataset.py
```
Note: I would recommend to start from notebook_download_dataset.py, followed by notebook_raw_dataset.py and finally notebook_curated_dataset.py. But you can skip the notebook_download_dataset.py if you already have access to the dataset.

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
To run marimo notebook (Similar to the note for conda users, I would recommend to start from notebook_download_dataset.py, followed by notebook_raw_dataset.py and finally notebook_curated_dataset.py, but you can skip the notebook_download_dataset.py if you already have access to the dataset). 
```
#similarly, there are two modes to choose from, so just run one of the commands
#to enter editor mode
uv run marimo edit .\notebook_download_dataset.py
#to enter web app view-only mode
uv run marimo run notebook_raw_dataset.py
```
Here is how a marimo notebook look like
<img width="828" height="673" alt="Screenshot 2026-10-30 at 14 46 05" src="https://github.com/user-attachments/assets/20fa3af8-4e0d-4dfb-9124-dea037457d87" />

(use Ctrl + C, to terminate an operating notebook)

## How to use the notebook

Usually, in a notebook like this, as long as you go through commmands cell by cell, you will more or less understand the analysis. However, in this repository, there is also a notebook to create curated data based on raw data. Therefore, it should be better if some flexibility is left in the notebook and users can decide how to analyse the data themselves.<br />
When I manage different ways of analysis, I loaded those variables (or input arguments for a function) into a dictionary form, so that I can change and monitor those variables.<br />

Below is the dictionary used in the analysis


```
    "exp_place": "MatrexVR",# where the experiment takes place? No need to change anything here
    "temperature_data_options": "el_usb", # which temperature logger was used in this dataset? No need to change anything here
    "active_trials_only": true, # whether to only include trials where animals walk longer than 10 cm (an arbitrary threshold set in the function "plot_yaw_angular_velocity") when plotting median angular velocity?
    "filtering_method": "rolling_median", # methods to smooth the raw data. You can choose between rolling_median or sg_filter (savgol_filter). The method is applied in "notebook_raw_dataset.py" for the position (x,y) and angular velocity. Note: in the curated database, animals' walking distance was estimated based on their location being smoothed by savgol_filter, but the angular velocity was not smoothed. 
    "yaw_axis": "z", # which axis represents the yaw axis in this dataset? No need to change anything here 
    "camera_fps": 100, # How many frames were acquired by the camera in a second? No need to change anything here 
    "stim_duration": 25, # How long was the stimulus presentation? No need to change anything here
    "interval_duration": [
        10,
        15
    ], # How long was the inter-stimulus intervals? No need to change anything here 
    "analysis_window": [
    -10,
    35
    ], # From when to when would you like to extract and align the angular velocity for further analysis. 0 marks the onset of the stimulus. These default values means extract angular velocities between 10 second prior to the stimulus presentation and 35 second after the stimulus presentation in every trial
    "prestim_duration": 300 # How long was the grey screen prior to any stimulus and inter-stimulus interval? No need to change anything here 
```
This python dictionary is stored as .json file.<br />
You can load this dictionary with the following command.
```
_file_name = './analysis_methods_dictionary.json'
with open(_file_name, 'r') as _f:
    analysis_methods = json.loads(_f.read())
```

You can change any variables in this dictionary with the following command.
```
analysis_methods.update({"active_trials_only":True})
```