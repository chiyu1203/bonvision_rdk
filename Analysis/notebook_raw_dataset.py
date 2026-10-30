import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Accessing dataset Random Dot Kinematograms in Desert Locusts on Marimo notebook
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Marimo notebook is similar to jupyter notebook, where you can interact with codes cell by cell (or block by block). Nevertheless, the biggest difference between the two is that Marimo notebook can automatically synchronise the value of global variables to all of the activated cells. This helps demonstrate a database like this, because you do not need to remember which cell to activate and which one to skip, but it is tricky to prototype a script on Marimo.

    #### A useful tip for new Marimo notebook users: get used to local variables and global variables
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### What is a local variable on Marimo notebook?
    #### A variable whose name starts from an _, for example _file_name
    #### When a local variable gets updated, it will only affect code within the same cell. By contrast, a global variable will affect the entire notebook. Therefore, it is impossible to define two global variables with the same name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Anyway, let us give it a try.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 0: loading package depandancies and environmental variables
    """)
    return


@app.cell
def _():
    import os,json
    from pathlib import Path
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from utils import boolean_array_to_event_table, bootstrap_cumulative_probability, converting_follow_velocity,bfill
    from plotting_utils import plot_example_trajectory, plot_yaw_angular_velocity, heatmap, annotate_heatmap

    from matplotlib.colors import ListedColormap
    ## a useful function to generate a customised colourmap to repordocue the colour schemes in the Extended Figure 2B (the manuscript in the Zenodo dataset)
    custom_5 = ListedColormap(
        ["blue","cyan","red","magenta", "purple"],
        name="custom_5")
    return (
        Path,
        bfill,
        json,
        mo,
        np,
        pd,
        plot_example_trajectory,
        plot_yaw_angular_velocity,
        plt,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 0.1: Loading analysis methods into a dictionary variable
    """)
    return


@app.cell
def _(json):
    # I used python dict to manage how to analyse data. The dictionary is stored in .json file. These commands load json file as a python dictionary
    _file_name = './analysis_methods_dictionary.json'
    with open(_file_name, 'r') as _f:
        analysis_methods = json.loads(_f.read())
    return (analysis_methods,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 0.2: Gaining access to the dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Session 0.2.1 we used a 3-party package zenodo_get to download data from Zenodo (skip this session if you have access to the server of AG Couzin-Fuchs)
    """)
    return


@app.cell
def _():
    from zenodo_get import download
    # the raw dataset is huge so I would recommend you to prepar a 10GB space to your local hard drive. 

    #"10.5281/zenodo.23565813" is the dataset ID on Zenodo

    # specify either the full file name or some pattern of the file name to download the data you want in file_glob. For example:
    ## to download the curated database, type "*.gzip"
    ## to download the raw database, type "*.zip"
    ## to download the metadata, type "*.xlsx"
    ## typing "*.pdf", will download both the protocol and manuscript, so I would recommend using the full name in this scenario

    files_local_location="/Users/chiyu_lee/Downloads"# change here to where you want to download the dataset
    #download("10.5281/zenodo.23565813",output_dir=files_local_location,file_glob="*.zip")
    return (files_local_location,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 1: Loading dataset as pandas dataframe
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Session 1.1 if you have access to the server of AG Couzin-Fuchs, specify the path to where the database is stored. If you download the data from Zenodo, having_server_access to False and then specify where you store the data in this_dataste_dir
    """)
    return


@app.cell
def _(Path, files_local_location, pd):
    #The raw data following a hierarchical structure where each animal's data is stored in its own folder so here is an example to work on one of the folder.
    having_server_access=True
    _folder_name = 'MatrexVR'
    #_Datasets = 'Z:/DATA/experiment_trackball_Optomotor'
    _Datasets ='/Volumes/AG_Couzin-Fuchs/DATA/experiment_trackball_Optomotor/'
    _animal_ID='GN24098'
    _experiment_date='240810'
    _file_name = 'database_camera2_2024-08-10T17_38_24-20240810_231205.parquet.gzip'
    if having_server_access:
        this_dataset_dir = f'{_Datasets}/{_folder_name}'
    else:
        this_dataset_dir = files_local_location
    df = pd.read_parquet(Path(this_dataset_dir) / _animal_ID / _experiment_date / 'coherence'/ 'session1'/_file_name)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 2: Visualising trajectory of interest
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Session 2.1 load some variables in the analysis methods dictionary into global variables
    """)
    return


@app.cell
def _(analysis_methods, np):
    camera_fps=analysis_methods.get('camera_fps')
    filtering_method=analysis_methods.get("filtering_method")
    if np.mod(camera_fps*0.5, 2) == 1:
        smooth_window_length=round(camera_fps*0.5)
    else: 
        smooth_window_length=round(camera_fps*0.5)+1 
    yaw_axis=analysis_methods.get("yaw_axis","z").lower()
    return filtering_method, smooth_window_length, yaw_axis


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Session 2.2 apply smoothing tools to the raw data
    """)
    return


@app.cell
def _(
    bfill,
    df,
    filtering_method,
    savgol_filter,
    smooth_window_length,
    yaw_axis,
):
    if filtering_method == "sg_filter":
        x_all = savgol_filter(df.loc[:, ["intergrated x position"]].values[:,0], smooth_window_length, 3, axis=0)
        y_all = savgol_filter(df.loc[:, ["intergrated y position"]].values[:,0], smooth_window_length, 3, axis=0)
        yaw_angular_velocity =df.loc[:, [f"delta rotation vector lab {yaw_axis}"]].values[:,0]
    elif filtering_method == "rolling_median":
        x_all =df.loc[:, ["intergrated x position"]].rolling(smooth_window_length).median().values
        y_all = df.loc[:, ["intergrated y position"]].rolling(smooth_window_length).median().values
        yaw_angular_velocity =df.loc[:, [f"delta rotation vector lab {yaw_axis}"]].rolling(smooth_window_length).median().values
        x_all=bfill(x_all[:,0])
        y_all=bfill(y_all[:,0])
        yaw_angular_velocity=bfill(yaw_angular_velocity[:,0])
    else:
        x_all = df.loc[:, ["intergrated x position"]].values[:,0]
        y_all = df.loc[:, ["intergrated y position"]].values[:,0]
        yaw_angular_velocity = df.loc[:, [f"delta rotation vector lab {yaw_axis}"]].values[:,0] 
    return x_all, y_all, yaw_angular_velocity


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ####Session 2.3 write in from which frames to which frames you want to visualise the trajectory.
    """)
    return


@app.cell
def _(
    analysis_methods,
    plot_example_trajectory,
    x_all,
    y_all,
    yaw_angular_velocity,
):
    plot_example_trajectory(x_all,y_all,yaw_angular_velocity=yaw_angular_velocity,start_frame=411341,end_frame=420430,start_marker=[412857,416894],end_marker=[415381,419418],analysis_methods=analysis_methods)
    return


@app.cell
def _(analysis_methods, df, end_frame, init_frame, plot_yaw_angular_velocity):
    fig,_fig_tbt=plot_yaw_angular_velocity(df,analysis_methods,init_frame,end_frame)
    _fig_tbt
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Session 5: Others in the dataset
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 5.1: visualising travel distance in the dataset
    """)
    return


@app.cell
def _(df, plt):
    _fig, (_ax1,_ax2) = plt.subplots(nrows=1, ncols=2,figsize=(10, 5))
    #use pandas's groupby to get a summarised dataframe for every animal.
    df_aba = df.groupby('ID').agg(travel_distance=('travel_distance', 'mean'), travel_distance_isi=('travel_distance_isi', 'mean'), ID=('ID', 'first'))
    #ax1 is on the left, which plots the distribution of every animal's travel distance
    #ax2 is on the right, which plots the distribution of the travel distance in every trial
    _ax1.hist(df_aba['travel_distance'])
    _ax2.hist(df['travel_distance'], bins=100)
    _ax2.axvline(x=10, ymin=0, ymax=1, color='red', ls='--')
    #_fig.savefig("histogram_4coherence.svg")
    _fig
    return


if __name__ == "__main__":
    app.run()
