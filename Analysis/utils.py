import warnings
from typing import Optional, Sequence
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import pandas as pd
import scipy.stats as st
from scipy.stats import bootstrap

class MplColorHelper:
    def __init__(self, cmap_name, start_val, stop_val):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)
    
def plot_yaw_angular_velocity(df,analysis_methods,init_frame=1000,end_frame=3500,vr_no="all",colormap_name="coolwarm"):
    camera_fps=analysis_methods.get("camera_fps")
    active_trials_only=analysis_methods.get("active_trials_only")
    COL = MplColorHelper(colormap_name, 0, len(df["stim_type"].unique())-1)
    sm = cm.ScalarMappable(cmap=colormap_name)
    analysis_window=analysis_methods.get("analysis_window")
    stim_duration=analysis_methods.get("stim_duration")
    if vr_no=='single':
        ylim_w=(-3,3)
        
    else:
        ylim_w=(-1.2,1.2)
    ylim_heading=(-150,150)
    using_bs_ci=False
    use_mean=False
    stimulus_velocity=64 #unit degree/s
    walk_threshold_tbt=10
    premature_turn=0.25#set this criteria to remove animals starting to make turn turing ISI
    fig, axes = plt.subplots(
        nrows=1, ncols=2, figsize=(12, 8))
    ax1, ax2 = axes.flatten()

    fig_tbt, subplots = plt.subplots(
        nrows=1, ncols=len(df["stim_type"].unique())+1, figsize=(15, 3), tight_layout=True,sharey=False
    )
    if active_trials_only==True:
        #df_selected=df[(df['travel_distance_isi']>walk_threshold_tbt) & (abs(df["opto_index_isi"])<premature_turn)]
        df_selected=df[(df['travel_distance']>walk_threshold_tbt)]
    else:
        df_selected=df
    i=0
    for this_stim, entries in df_selected.groupby('stim_type'):
        these_angular_velocity=entries.loc[:,'angular_velocity_f0':].values
        these_angular_acceleration=np.gradient(these_angular_velocity,1/camera_fps,axis=1)
        these_headings=np.cumsum(these_angular_velocity,axis=1)/camera_fps
        heading_at_stim=these_headings[:,init_frame]
        these_headings=these_headings-np.reshape(np.repeat(heading_at_stim,these_headings.shape[1]), these_headings.shape)# rezero the orientation at the start of stimuli
        #heading_prev_stim=these_headings[:,:init_frame]-np.reshape(np.repeat(heading_at_stim,init_frame), these_headings[:,:init_frame].shape)
        #heading_post_stim=these_headings[:,init_frame:]-np.reshape(np.repeat(heading_at_stim,end_frame), (these_headings.shape[0], end_frame))
        time_points = np.arange(these_headings.shape[1])
        time_points_2D = np.tile(time_points, (these_headings.shape[0], 1))
        #define the stimulus speed in the first iteration
        if i ==0:
            xticks = [0, init_frame, end_frame]
            xticklabels = [str(analysis_window[0]), "0", str(stim_duration)]
            y_range=150
            tmp = np.full(these_headings.shape[1],np.nan)
            dif_tmp= np.full(these_angular_velocity.shape[1],np.nan)
            stim_w_array=np.ones(end_frame-init_frame)*stimulus_velocity*np.pi/180
            tmp[init_frame:end_frame]=np.cumsum(stim_w_array)/camera_fps
            dif_tmp[init_frame:end_frame]=stim_w_array


        #plot trial-by-trial response
        #ax.scatter(time_points_2D, these_headings, s=0.01,alpha=0.1,color=COL.get_rgb(i))
        #plot the whole area (not recommended for tbt)
        #ax.plot(time_points_2D, these_headings, linestyle='-',linewidth=0.1,color=COL.get_rgb(i)))
        subplots[i].scatter(time_points_2D, these_headings, s=0.01,alpha=0.1,color=COL.get_rgb(i))
        subplots[i].plot(time_points,tmp,color='k',linewidth=1)
        subplots[i].plot(time_points,tmp*-1,color='k',linewidth=1)
        subplots[i].axvline(
        x=init_frame,
        color="black",
        linestyle="--",
        label="Stimulus Starts",
        )
        subplots[i].axvline(
            x=end_frame,
            color="black",
            linestyle="--",
            label="Stimulus Ends",
        )
        subplots[i].set(
        #ylabel="Orientation (rad)",
        xticks=[init_frame, end_frame],
        xticklabels=["0", str(stim_duration)],
        #xlabel="Time (s)",
        yticks=[-100,0,100],
        ylim=ylim_heading,
    )
        for label in subplots[i].get_xticklabels():
            label.set_fontsize(16)
        for label in subplots[i].get_yticklabels():
            label.set_fontsize(16)
            label.set_rotation(90)
        if i==0:
            subplots[i].set_ylabel(r'sum of turn (rad)', fontsize=20)
        if i==3:
            subplots[i].set_xlabel("Time (s)", fontsize=20)
        #plot average response
        if use_mean==True:
            headings_to_plot = np.mean(these_headings, axis=0)
            velocity_to_plot = np.mean(these_angular_velocity, axis=0)
            acceleration_to_plot=np.mean(these_angular_acceleration, axis=0)
        else:
            headings_to_plot=np.median(these_headings, axis=0)
            velocity_to_plot=np.median(these_angular_velocity, axis=0)
            acceleration_to_plot=np.median(these_angular_acceleration, axis=0)
        #ax.plot(time_points,headings_to_plot,color=COL.get_rgb(i))
        ax1.plot(time_points,velocity_to_plot,color=COL.get_rgb(i))
        ax2.plot(time_points,acceleration_to_plot,color=COL.get_rgb(i))
        subplots[len(df["stim_type"].unique())].plot(time_points,headings_to_plot,color=COL.get_rgb(i))

        ##to plot distribution with bootstrap 95% confidence interval
        if using_bs_ci:
            # data=(these_headings,)
            # res=st.bootstrap(data,np.std,n_resamples=99,vectorized=True,random_state=1)
            # y1=res.confidence_interval[0]
            # y2=res.confidence_interval[1]
            # del data
            confidence_level = 0.95
            #data=(these_angular_velocity,)
            
            res=st.bootstrap(data=(these_angular_velocity,),statistic=np.median,n_resamples=999,vectorized=True,batch=100,random_state=1)
            w_y1=res.confidence_interval[0]
            w_y2=res.confidence_interval[1]
            ##to plot distribution with 95% confidence interval with normal distribution because it is faster not because it is correct
            res=st.bootstrap(data=(these_headings,),statistic=np.median,n_resamples=999,vectorized=True,batch=100,random_state=1)
            #cl95=st.norm.interval(confidence_level,loc=headings_to_plot,scale=st.sem(these_headings))
            # y1=cl95[0][:]
            # y2=cl95[1][:]
            y1=res.confidence_interval[0]
            y2=res.confidence_interval[1]
            #cl95=st.norm.interval(confidence_level,loc=velocity_to_plot,scale=st.sem(these_angular_velocity))
            # w_y1=cl95[0][:]
            # w_y2=cl95[1][:]
            cl95=st.norm.interval(confidence_level,loc=acceleration_to_plot,scale=st.sem(these_angular_acceleration))
            acc_y1=cl95[0][:]
            acc_y2=cl95[1][:]
        else:
            ##to plot distribution with sem
            sem_response = np.std(these_headings, axis=0, ddof=1) / np.sqrt(these_headings.shape[0])
            y1 = headings_to_plot + sem_response
            y2 = headings_to_plot - sem_response
            sem_response = np.std(these_angular_velocity, axis=0, ddof=1) / np.sqrt(these_angular_velocity.shape[0])
            w_y1=velocity_to_plot + sem_response
            w_y2=velocity_to_plot - sem_response
            sem_response = np.std(these_angular_acceleration, axis=0, ddof=1) / np.sqrt(these_angular_acceleration.shape[0])
            acc_y1=acceleration_to_plot + sem_response
            acc_y2=acceleration_to_plot - sem_response
        #ax.fill_between(time_points,y1,y2, alpha=0.5,color=COL.get_rgb(i))
        ax1.fill_between(time_points,w_y1,w_y2, alpha=0.5,color=COL.get_rgb(i))
        ax2.fill_between(time_points,acc_y1,acc_y2, alpha=0.5,color=COL.get_rgb(i))
        subplots[len(df["stim_type"].unique())].fill_between(time_points,y1,y2, alpha=0.5,color=COL.get_rgb(i))

        i=i+1
    # ax.plot(time_points,tmp,color='k',linewidth=0.8)
    # ax.plot(time_points,tmp*-1,color='k',linewidth=0.8)
    ax1.plot(time_points,dif_tmp,color='k',linewidth=1)
    ax1.plot(time_points,dif_tmp*-1,color='k',linewidth=1)
    subplots[len(df["stim_type"].unique())].plot(time_points,tmp,color='k',linewidth=1)
    subplots[len(df["stim_type"].unique())].plot(time_points,tmp*-1,color='k',linewidth=1)
    # ax.axvline(
    #     x=init_frame,
    #     color="black",
    #     linestyle="--",
    #     label="Stimulus Starts",
    # )
    # ax.axvline(
    #     x=end_frame,
    #     color="black",
    #     linestyle="--",
    #     label="Stimulus Ends",
    # )
    ax1.axvline(
        x=init_frame,
        color="black",
        linestyle="--",
        label="Stimulus Starts",
    )
    ax1.axvline(
        x=end_frame,
        color="black",
        linestyle="--",
        label="Stimulus Ends",
    )
    ax2.axvline(
        x=init_frame,
        color="black",
        linestyle="--",
        label="Stimulus Starts",
    )
    ax2.axvline(
        x=end_frame,
        color="black",
        linestyle="--",
        label="Stimulus Ends",
    )
    subplots[len(df["stim_type"].unique())].axvline(
        x=init_frame,
        color="black",
        linestyle="--",
        label="Stimulus Starts",
    )
    subplots[len(df["stim_type"].unique())].axvline(
        x=end_frame,
        color="black",
        linestyle="--",
        label="Stimulus Ends",
    )
    subplots[len(df["stim_type"].unique())].set(
        xticks=[init_frame, end_frame],
        xticklabels=["0", str(stim_duration)],
        yticks=[-50,0,50],
        ylim=[-50,50],
    )
    for label in subplots[len(df["stim_type"].unique())].get_xticklabels():
        label.set_fontsize(16)
    for label in subplots[len(df["stim_type"].unique())].get_yticklabels():
        label.set_fontsize(16)
        label.set_rotation(90)

    ax1.set(
        #ylabel=r'angular velocity (rad s$^{-1}$)',
        xticks=xticks,
        yticks=[-1,0,1],
        #ylim=[-0.005,0.02],
        ylim=ylim_w,
        xticklabels=xticklabels,
        #xlabel="Time (s)",
    )
    ax1.set_ylabel(r'angular velocity (rad s$^{-1}$)', fontsize=22)
    ax2.set_xlabel(r'angular velocity (rad s$^{-1}$)', fontsize=22)
  


    for label in ax1.get_xticklabels():
        label.set_fontsize(16)

    for label in ax1.get_yticklabels():
        label.set_fontsize(16)
    ax2.set(
        ylabel=r'angular acceleration (rad s$^{-2}$)',
        xlabel="Time (s)",
        xticks=xticks,
        xticklabels=xticklabels,
    )  
    tick_positions = np.linspace(0, 1, len(df["stim_type"].unique()))
    these_coherence=df["stim_type"].unique()
    these_coherence.sort()
    tick_labels = [str(value) for value in these_coherence]
    cbar = plt.colorbar(sm, ax=[ax1], orientation="horizontal", location='top',ticks=tick_positions,aspect=80)
    #cbar = plt.colorbar(sm, ax=[ax2], orientation="horizontal", location='top',ticks=tick_positions,aspect=60)
    cbar.set_ticklabels(tick_labels)
    return fig, fig_tbt

def boolean_array_to_event_table(
    reached_target: np.ndarray,
    *,
    timepoints: Optional[Sequence[float]] = None,
    sampling_interval: Optional[float] = None,
    stimulus_onset: float = 0.0,
    stimulus_onset_index: int = -1,
    consecutive_samples: int = 1,
    trial_ids: Optional[Sequence] = None,
    subject_ids: Optional[Sequence] = None,
    trial_col: str = "trial",
    subject_col: str = "animal_id",
) -> pd.DataFrame:
    """Convert a trial-by-time Boolean array to first-passage event data.

    Parameters
    ----------
    reached_target
        Two-dimensional array with shape (n_trials, n_timepoints). True means
        that the target-speed criterion was met at that sampled timepoint.
        Numeric arrays are accepted only when every value is 0 or 1.
    timepoints
        Optional length-n_timepoints vector containing the recorded times in
        seconds. Values may include baseline times. ``stimulus_onset`` is
        subtracted from this vector, and only strictly post-onset samples are
        used. Supply either ``timepoints`` or ``sampling_interval``.
    sampling_interval
        Seconds between columns when an explicit time vector is unavailable.
        Relative time is calculated as
        ``(column_index - stimulus_onset_index) * sampling_interval``.
    stimulus_onset
        Stimulus-onset time in the coordinate system of ``timepoints``. This
        argument is used only when ``timepoints`` is supplied.
    stimulus_onset_index
        Column representing t=0 when ``sampling_interval`` is used. The default
        -1 means that column 0 is the first post-onset sample, occurring one
        sampling interval after onset. If column 0 is sampled exactly at t=0,
        pass 0. If column 100 is t=0, pass 100.
    consecutive_samples
        Number of consecutive True samples required to define a hit. The event
        time is the beginning of the first qualifying run. Default is 1.
    trial_ids, subject_ids
        Optional identifiers with one value per row. Supplying ``subject_ids``
        adds a column suitable for ``subject_col`` in the fitting function.

    Returns
    -------
    pandas.DataFrame
        One row per trial. ``time`` is the first-hit latency for event=1, or
        the last observed post-onset time for event=0 (right-censored).

    Notes
    -----
    A sample exactly at t=0 is excluded because the continuous Weibull model
    requires positive event times. A True value at t=0 that persists into the
    next sample is therefore recorded at the first strictly positive time.
    """
    values = np.asarray(reached_target)
    if values.ndim != 2:
        raise ValueError(
            "reached_target must be a 2D array with shape "
            "(n_trials, n_timepoints)"
        )
    n_trials, n_timepoints = values.shape
    if n_trials == 0 or n_timepoints == 0:
        raise ValueError("reached_target cannot have an empty dimension")

    if values.dtype != np.bool_:
        if not np.issubdtype(values.dtype, np.number):
            raise TypeError("reached_target must contain Boolean or 0/1 values")
        if np.any(~np.isfinite(values)) or not np.all(np.isin(values, [0, 1])):
            raise ValueError("Numeric reached_target arrays may contain only 0 and 1")
    hits = values.astype(bool, copy=False)

    if timepoints is not None and sampling_interval is not None:
        raise ValueError("Supply timepoints or sampling_interval, not both")
    if timepoints is None and sampling_interval is None:
        raise ValueError("Supply either timepoints or sampling_interval")

    if timepoints is not None:
        sample_times = np.asarray(timepoints, dtype=float)
        if sample_times.ndim != 1 or len(sample_times) != n_timepoints:
            raise ValueError(
                "timepoints must be one-dimensional with one value per column"
            )
        if np.any(~np.isfinite(sample_times)):
            raise ValueError("timepoints contains missing or non-finite values")
        if np.any(np.diff(sample_times) <= 0):
            raise ValueError("timepoints must be strictly increasing")
        relative_times = sample_times - float(stimulus_onset)
    else:
        sampling_interval = float(sampling_interval)
        if not np.isfinite(sampling_interval) or sampling_interval <= 0:
            raise ValueError("sampling_interval must be a positive number")
        if not isinstance(stimulus_onset_index, (int, np.integer)):
            raise TypeError("stimulus_onset_index must be an integer")
        if stimulus_onset_index >= n_timepoints:
            raise ValueError("stimulus_onset_index lies beyond the final column")
        relative_times = (
            np.arange(n_timepoints, dtype=float) - stimulus_onset_index
        ) * sampling_interval

    post_mask = relative_times > 0
    if not np.any(post_mask):
        raise ValueError("There must be at least one timepoint after stimulus onset")
    if np.any(hits[:, relative_times < 0]):
        warnings.warn(
            "At least one pre-stimulus True value was found. These samples are "
            "excluded, but they conflict with a zero pre-stimulus failure rate.",
            stacklevel=2,
        )

    if not isinstance(consecutive_samples, (int, np.integer)):
        raise TypeError("consecutive_samples must be an integer")
    if consecutive_samples < 1:
        raise ValueError("consecutive_samples must be at least 1")

    post_hits = hits[:, post_mask]
    post_times = relative_times[post_mask]
    if consecutive_samples > post_hits.shape[1]:
        raise ValueError(
            "consecutive_samples exceeds the number of post-stimulus samples"
        )
    if consecutive_samples == 1:
        qualifying = post_hits
    else:
        windows = np.lib.stride_tricks.sliding_window_view(
            post_hits, window_shape=consecutive_samples, axis=1
        )
        qualifying = windows.all(axis=-1)

    event = qualifying.any(axis=1)
    first_index = np.argmax(qualifying, axis=1)
    observed_time = np.full(n_trials, post_times[-1], dtype=float)
    observed_time[event] = post_times[first_index[event]]

    if trial_ids is None:
        trial_ids_array = np.arange(n_trials)
    else:
        trial_ids_array = np.asarray(trial_ids)
        if trial_ids_array.ndim != 1 or len(trial_ids_array) != n_trials:
            raise ValueError("trial_ids must contain one value per array row")

    output = pd.DataFrame(
        {
            trial_col: trial_ids_array,
            "time": observed_time,
            "event": event.astype(int),
        }
    )
    if subject_ids is not None:
        subject_ids_array = np.asarray(subject_ids)
        if subject_ids_array.ndim != 1 or len(subject_ids_array) != n_trials:
            raise ValueError("subject_ids must contain one value per array row")
        output[subject_col] = subject_ids_array
    return output,qualifying

def bootstrap_cumulative_probability(
    qualifying,
    *,
    subject_ids=None,
    n_resamples=10_000,
    confidence_level=0.95,
    batch=100,
    seed=42,
):
    """Return (probability, lower, upper), each shaped (n_window_starts,).

    Parameters
    ----------
    qualifying : 2D Boolean or 0/1 array
        Output from boolean_array_to_event_table. Rows are trials and columns
        are candidate start times for qualifying windows.
    subject_ids : 1D sequence or None
        One animal ID per trial. If supplied, resample animals with replacement
        and keep all trials belonging to each sampled animal. Otherwise,
        resample trials with replacement, assuming trials are independent.
    n_resamples : int
        Number of bootstrap draws.
    confidence_level : float
        Pointwise confidence level, between zero and one.
    batch : int
        Number of index resamples processed together by SciPy. Reduces working
        memory, but SciPy still stores all bootstrap curves in its result.
    seed : int, numpy.random.Generator, or None
        Random seed or generator passed through numpy.random.default_rng.

    Notes
    -----
    The estimate is always weighted equally over trials, including when
    resampling animals with unequal trial counts. No-event trials remain in
    the denominator. These are percentile intervals, not simultaneous bands.
    Columns where all resampling units have the same probability give a
    zero-width interval. This limitation does not establish certainty about
    the underlying population probability. Few independent units can give
    unreliable coverage, regardless of the number of bootstrap draws.
    """
    qualifying = np.asarray(qualifying)
    if qualifying.ndim != 2 or 0 in qualifying.shape:
        raise ValueError("qualifying must be a non-empty 2D array")
    if not np.all((qualifying == 0) | (qualifying == 1)):
        raise ValueError("qualifying must contain only Boolean or 0/1 values")

    # True from the first qualifying event onward, independently for each trial.
    cumulative = np.maximum.accumulate(qualifying.astype(bool), axis=1)
    probability = cumulative.mean(axis=0)
    n_trials, n_times = cumulative.shape

    if subject_ids is None:
        unit_sums = cumulative
        unit_sizes = np.ones(n_trials, dtype=int)
    else:
        ids = np.asarray(subject_ids)
        if ids.shape != (n_trials,):
            raise ValueError("subject_ids must have one animal ID per trial")
        codes, animals = pd.factorize(ids, sort=False)
        if np.any(codes < 0):
            raise ValueError("subject_ids cannot contain missing values")
        unit_sums = np.zeros((len(animals), n_times), dtype=np.int64)
        np.add.at(unit_sums, codes, cumulative)
        unit_sizes = np.bincount(codes)

    n_units = len(unit_sizes)
    if n_units < 2:
        raise ValueError("Need at least two independent trials or animals")

    def statistic(indices):
        # Reusing the same indices at every time preserves each unit's curve.
        return unit_sums[indices].sum(axis=0) / unit_sizes[indices].sum()

    result = bootstrap(
        (np.arange(n_units),),
        statistic=statistic,
        vectorized=False,
        n_resamples=n_resamples,
        confidence_level=confidence_level,
        batch=batch,
        method="percentile",
        rng=np.random.default_rng(seed),
    )
    return probability, result.confidence_interval.low, result.confidence_interval.high