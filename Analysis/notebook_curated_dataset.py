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
    from utils import plot_yaw_angular_velocity, boolean_array_to_event_table, bootstrap_cumulative_probability, converting_follow_velocity, heatmap, annotate_heatmap
    from reliability.Fitters import Fit_Weibull_2P,Fit_Everything,Fit_Exponential_1P,Fit_Weibull_DS,Fit_Weibull_Mixture,Fit_Exponential_2P
        ## A useful function to generate a data list for further analysis
    from matplotlib.colors import ListedColormap
    custom_5 = ListedColormap(
        ["blue","cyan","red","magenta", "purple"],
        name="custom_5")
    return (
        Fit_Everything,
        Fit_Exponential_1P,
        Fit_Exponential_2P,
        Fit_Weibull_2P,
        Fit_Weibull_DS,
        Fit_Weibull_Mixture,
        Path,
        annotate_heatmap,
        boolean_array_to_event_table,
        bootstrap_cumulative_probability,
        converting_follow_velocity,
        custom_5,
        heatmap,
        json,
        mo,
        np,
        pd,
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
    #The benefit of saving database in parquet.gzip is long-term storage but loading it takes time
    having_server_access=True
    _folder_name = 'MatrexVR'
    #_Datasets = 'Z:/DATA/experiment_trackball_Optomotor'
    _Datasets ='/Volumes/AG_Couzin-Fuchs/DATA/experiment_trackball_Optomotor/'
    if having_server_access:
        this_dataset_dir = f'{_Datasets}/{_folder_name}'
    else:
        this_dataset_dir = files_local_location
    
    _file_name = 'MatrexVR_4coherence_database_rolling_median.parquet.gzip'
    df = pd.read_parquet(Path(this_dataset_dir) / _file_name)
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 2: Visualising visually-evoked angular velocity
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Session 2.1 load some variables in the analysis methods dictionary into global variables
    """)
    return


@app.cell
def _(analysis_methods):
    _camera_fps=analysis_methods.get('camera_fps')
    analysis_window = analysis_methods.get('analysis_window')
    stim_duration = analysis_methods.get('stim_duration')
    init_frame = _camera_fps * abs(analysis_window[0])
    end_frame = _camera_fps * (abs(analysis_window[0]) + stim_duration)
    return end_frame, init_frame, stim_duration


@app.cell
def _(analysis_methods, df, end_frame, init_frame, plot_yaw_angular_velocity):
    # To save processing time, let's just include non-stationary trials (travel distance over 10 cm during 25-s stimulus presentation)
    analysis_methods.update({"active_trials_only":True})
    _colormap_name = "coolwarm"
    fig,_fig_tbt=plot_yaw_angular_velocity(df,analysis_methods,init_frame,end_frame,"all",_colormap_name)
    _fig_tbt
    return (fig,)


@app.cell
def _(fig):
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Session 3: Analysing temporal patterns of the steering event
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 3.1: Converting angular velocity into the steering event
    """)
    return


@app.cell
def _(converting_follow_velocity, df):
    df_angular_speed=df.apply(converting_follow_velocity, axis=1)
    return (df_angular_speed,)


@app.cell
def _(df_angular_speed, end_frame, init_frame):
    _num_trial_info_column=16
    arr = df_angular_speed.iloc[:, init_frame+_num_trial_info_column:end_frame+_num_trial_info_column].values
    return (arr,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 3.2: A GUI to output fitting results with varying parameters
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 3.2.1 load functions in the notebook. Unlike functions in the untils.py, these functions are stored in the notebook so that users can change it easily. Just remeber to load them first.
    """)
    return


@app.cell
def _(
    Fit_Exponential_1P,
    Fit_Exponential_2P,
    Fit_Weibull_2P,
    Fit_Weibull_DS,
    Fit_Weibull_Mixture,
    censored_data,
    model_choice,
):
    def fit_model(input_data):
        output=[]
        if censored_data.value:
            _faiures=input_data[input_data['event'] == 1]['time'].values
            _right_censored=input_data[input_data['event'] == 0]['time'].values
        else:
            _faiures=input_data[input_data['event'] == 1]['time'].values
            _right_censored=None
        if model_choice.value=="All of the above":
            _1=Fit_Weibull_DS(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
            _2=Fit_Weibull_Mixture(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
            _3=Fit_Weibull_2P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
            _4=Fit_Exponential_2P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
            _5=Fit_Exponential_1P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
            output.append([_1,_2,_3,_4,_5])
        elif model_choice.value=="Weibull defective subpopulation":
            output=Fit_Weibull_DS(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
        elif model_choice.value=="Weibull mixtures":
            output=Fit_Weibull_Mixture(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
        elif model_choice.value=="Weibull":
            output=Fit_Weibull_2P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
        elif model_choice.value=="2-parameter Exponential":
            output=Fit_Exponential_2P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
        elif model_choice.value=="Exponential":
            output=Fit_Exponential_1P(failures=_faiures, right_censored=_right_censored, show_probability_plot=False)
        else:
            print("unidentified model")

    return (fit_model,)


@app.cell
def _(boolean_array_to_event_table, camera_fps, np):
    def prepare_input(
        _this_sample_size: int,_this_target_speed: float, _coherence_index: int,arr:np.ndarray, df):
        timepoints = np.arange(arr.shape[1]) / camera_fps
        coherence_levels=[0,33,66,100]
        _coherence_to_analyse=coherence_levels[_coherence_index]
        _hit_target_epochs = arr > _this_target_speed
        _trial_to_analyse = abs(df['stim_type']) == _coherence_to_analyse
        _this_data = _hit_target_epochs[df[_trial_to_analyse].index,]
        _output_table, _ = boolean_array_to_event_table(_this_data, timepoints=timepoints, stimulus_onset=0, consecutive_samples=_this_sample_size)
        return _output_table

    return (prepare_input,)


@app.cell
def _(mo):
    form = mo.ui.form(
        mo.ui.dictionary({
            "sample_size": mo.ui.slider(start=1, stop=100,value=42,step=1,show_value=True),
            "speed_thresholds": mo.ui.slider(start=0.1, stop=2, value=1,step=0.1,show_value=True),
            "coherence_levels": mo.ui.slider(start=0, stop=3, value=1, step=1, show_value=True)},label="parameters"),
        submit_button_label="Go, Hidden Scientists!",
        bordered=False
    )
    form
    return (form,)


@app.cell
def _(mo):
    censored_data = mo.ui.switch(value=True, label="include unsuccessful trials into model fitting")
    model_choice = mo.ui.dropdown(
        options=["Weibull defective subpopulation","Weibull mixtures","Weibull","2-parameter Exponential","Exponential","All of the above"],
        value="Exponential",
        label="You are using model:",
    )
    mo.hstack([censored_data, model_choice], wrap=True, justify="start")
    return censored_data, model_choice


@app.cell
def _(arr, df, fit_model, form, mo, prepare_input):
    mo.stop(form.value is None, mo.md("Click **Go, Hidden Scientists!** to fit a model to the data and adjust the parameters with sliders "))
    _v = form.value
    input_data = prepare_input(_v["sample_size"], _v["speed_thresholds"], _v["coherence_levels"],arr,df)
    fit_model(input_data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session 3.3: Visualising steering event
    """)
    return


@app.cell
def _(df, np):
    #parameter space to explore
    coherence_levels=np.sort(abs(df['stim_type']).unique())
    sample_sizes = np.arange(8, 101, 7)
    _stimulus_speed = 64 * np.pi / 180
    speed_thresholds = [round(0.5 * _stimulus_speed, 2), round(_stimulus_speed, 2), round(2 * _stimulus_speed, 2)]
    return coherence_levels, sample_sizes, speed_thresholds


@app.cell
def _(analysis_methods, arr, np):
    onset_in_sec = 0
    camera_fps = analysis_methods.get('camera_fps')
    timepoints = np.arange(arr.shape[1]) / camera_fps
    post_times = timepoints[timepoints > onset_in_sec] - onset_in_sec
    return camera_fps, onset_in_sec, post_times, timepoints


@app.cell
def _(
    arr,
    boolean_array_to_event_table,
    bootstrap_cumulative_probability,
    coherence_levels,
    df,
    onset_in_sec,
    plt,
    post_times,
    sample_sizes,
    speed_thresholds,
    stim_duration,
    timepoints,
):
    colours = ['y', 'c', 'm', 'k']
    _use_single_threshold = True
    if _use_single_threshold:
        _stimulus_speed = speed_thresholds[1]
        _hit_target_epochs = arr > _stimulus_speed
    else:
        _stimulus_speed = [speed_thresholds[0], speed_thresholds[2]]
        _hit_target_lower = arr > _stimulus_speed[0]
        _hit_target_higher = arr < _stimulus_speed[1]
        _hit_target_epochs = _hit_target_higher & _hit_target_lower
    _fig, _axes = plt.subplots(nrows=1, ncols=sample_sizes.shape[0], figsize=(24, 5), tight_layout=True, sharex=True, sharey=True)
    for _j, _this_sample_size in enumerate(sample_sizes):
        for _i, _this_coherence in enumerate(coherence_levels):
            _trial_to_analyse = abs(df['stim_type']) == _this_coherence
            _this_data = _hit_target_epochs[df[_trial_to_analyse].index,]
            _, _qualifying = boolean_array_to_event_table(_this_data, timepoints=timepoints, stimulus_onset=onset_in_sec, consecutive_samples=_this_sample_size)
            probability, lower, upper = bootstrap_cumulative_probability(_qualifying, n_resamples=99, confidence_level=0.95, seed=42, subject_ids=None)
            event_times = post_times[:_qualifying.shape[1]]
            # _axes[_j].step(event_times, probability, where='post', color=colours[_i], label='Cumulative probability')
            #_axes[_j].fill_between(event_times, lower, upper, step='post', color=colours[_i], alpha=0.25, label='95% pointwise bootstrap CI')
            _axes[_j].plot(event_times, probability, color=colours[_i], label=f"{_this_coherence}%")
            _axes[_j].fill_between(event_times, lower, upper,color=colours[_i], alpha=0.25)
            if _j==0:
                _axes[_j].set(xlabel='Time since stimulus onset (s)', ylabel='Probability of Hit (%)', xticks=[onset_in_sec, stim_duration], ylim=(0, 1), yticks=[0, 0.5, 1], yticklabels=['0', '50', '100'])
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##Session 4: Applying survival analysis/reliability engineering to steering events
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Session4.1: Using Fit_everything function to compare the performance of each model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### The Fit_everything function can output parameter values, log-likelihood, AIC and BIC.
    """)
    return


@app.cell
def _(
    Fit_Everything,
    arr,
    boolean_array_to_event_table,
    coherence_levels,
    df,
    np,
    onset_in_sec,
    sample_sizes,
    speed_thresholds,
    timepoints,
):
    _number_of_models=5
    _coherence_to_analyse=coherence_levels[3]
    ready_to_plot_AIC = np.ones((len(speed_thresholds), sample_sizes.shape[0], _number_of_models))
    ready_to_plot_BIC = np.ones((len(speed_thresholds), sample_sizes.shape[0], _number_of_models))
    for _i, _this_target_speed in enumerate(speed_thresholds):
        _hit_target_epochs = arr > _this_target_speed
        for _j, _this_sample_size in enumerate(sample_sizes):
            _trial_to_analyse = abs(df['stim_type']) == _coherence_to_analyse
            _this_data = _hit_target_epochs[df[_trial_to_analyse].index,]
            _time_to_success_pd, _ = boolean_array_to_event_table(_this_data, timepoints=timepoints, stimulus_onset=onset_in_sec, consecutive_samples=_this_sample_size)
            every = Fit_Everything(failures=_time_to_success_pd[_time_to_success_pd['event'] == 1]['time'].values, right_censored=_time_to_success_pd[_time_to_success_pd['event'] == 0]['time'].values, exclude=['Normal_2P', 'Gumbel_2P', 'Lognormal_2P', 'Lognormal_3P', 'Loglogistic_2P', 'Loglogistic_3P', 'Gamma_2P', 'Gamma_3P', 'Weibull_CR', 'Weibull_3P'], show_probability_plot=False, print_results=False, show_best_distribution_probability_plot=False, show_histogram_plot=False, show_PP_plot=False)
            sorted_pd = every.results.sort_values('Distribution')
            ready_to_plot_AIC[_i, _j, :] = sorted_pd['AICc'].values
            ready_to_plot_BIC[_i, _j, :] = sorted_pd['BIC'].values
    return (ready_to_plot_AIC,)


@app.cell
def _(custom_5, np, plt, ready_to_plot_AIC, sample_sizes):
    _xlims = [(13000, 17500), (9500, 17000), (3000, 13500)]
    _yticks = [8, 50, 99]
    ix, iy, iz = np.indices(ready_to_plot_AIC.shape)
    _fig, _axes = plt.subplots(nrows=3, ncols=1, figsize=(30, 20), tight_layout=True, sharey=False)  #sharey='row'
    for _i in range(ready_to_plot_AIC.shape[0]):
        _axes[_i].scatter(ready_to_plot_AIC[_i, :, :], np.transpose(np.tile(sample_sizes, (ready_to_plot_AIC.shape[2], 1))), s=40, c=iz[_i, :, :], cmap=custom_5, marker='^', alpha=1)
        _axes[_i].set_xlim(_xlims[_i])
        _axes[_i].set_xticks(_xlims[_i])
        _axes[_i].set_yticks(_yticks)
        for _label in _axes[_i].get_xticklabels():
            _label.set_fontsize(20)  #axes[i].set_xscale('log')
        for _label in _axes[_i].get_yticklabels():
            _label.set_fontsize(20)
    _fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### To output the confidence interval of each parameter, it is required to apply speicific fitting functions, for example: Fit_Weibull_2P, these functions accept the same input arguement.
    """)
    return


@app.cell
def _(
    Fit_Weibull_2P,
    Fit_Weibull_DS,
    arr,
    boolean_array_to_event_table,
    coherence_levels,
    df,
    np,
    onset_in_sec,
    sample_sizes,
    speed_thresholds,
    timepoints,
):
    _coherence_to_analyse=coherence_levels[3]
    _consider_censored_data=True
    ready_to_plot_kappa = np.zeros((len(speed_thresholds), sample_sizes.shape[0]))
    ready_to_plot_kappa_lower = np.zeros((len(speed_thresholds), sample_sizes.shape[0]))
    ready_to_plot_kappa_upper = np.zeros((len(speed_thresholds), sample_sizes.shape[0]))
    for _i, _this_target_speed in enumerate(speed_thresholds):
        _hit_target_epochs = arr > _this_target_speed
        for _j, _this_sample_size in enumerate(sample_sizes):
            _trial_to_analyse = abs(df['stim_type']) == _coherence_to_analyse
            _this_data = _hit_target_epochs[df[_trial_to_analyse].index,]
            output_table, _qualifying = boolean_array_to_event_table(_this_data, timepoints=timepoints, stimulus_onset=onset_in_sec, consecutive_samples=_this_sample_size)
            if _consider_censored_data:
                _wbf = Fit_Weibull_DS(failures=output_table[output_table['event'] == 1]['time'].values, right_censored=output_table[output_table['event'] == 0]['time'].values, show_probability_plot=False, print_results=True)
            else:
                _wbf = Fit_Weibull_2P(failures=output_table[output_table['event'] == 1]['time'].values, show_probability_plot=False, print_results=True)
            ready_to_plot_kappa[_i, _j] = _wbf.beta
            ready_to_plot_kappa_lower[_i, _j] = _wbf.beta_lower
            ready_to_plot_kappa_upper[_i, _j] = _wbf.beta_upper
    return (ready_to_plot_kappa,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###Session 4.1: Using heatmap to visualise shape parameter
    """)
    return


@app.cell
def _(
    annotate_heatmap,
    heatmap,
    ready_to_plot_kappa,
    sample_sizes,
    speed_thresholds,
):
    #these two functions were adapted from https://matplotlib.org/3.1.0/gallery/images_contours_and_fields/image_annotated_heatmap.html
    im, cbar = heatmap(ready_to_plot_kappa, list(map(str, speed_thresholds)), sample_sizes.astype(str).tolist())
    texts = annotate_heatmap(im, valfmt='{x:.2f}', fontsize=8)
    im
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
