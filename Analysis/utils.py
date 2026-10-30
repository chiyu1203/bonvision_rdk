import warnings
from typing import Optional, Sequence
import numpy as np
import pandas as pd
import scipy.stats as st
def ffill(arr):
    mask = np.isnan(arr)
    if arr.ndim == 1:
        idx = np.where(~mask, np.arange(mask.shape[0]), 0)
        np.maximum.accumulate(idx, out=idx)
        out = arr[idx]
    elif arr.ndim == 2:
        idx = np.where(~mask, np.arange(mask.shape[1]), 0)
        np.maximum.accumulate(idx, axis=1, out=idx)
        out = arr[np.arange(idx.shape[0])[:, None], idx]
    return out


# Simple solution for bfill provided by financial_physician in comment below
#https://stackoverflow.com/questions/41190852/most-efficient-way-to-forward-fill-nan-values-in-numpy-array
def bfill(arr):
    if arr.ndim == 1:
        return ffill(arr[::-1])[::-1]
    elif arr.ndim == 2:
        return ffill(arr[:, ::-1])[:, ::-1]
def converting_follow_velocity(row):
    if row['stim_type'] < 0:
        row['stim_type'] = row['stim_type'] * -1  # Check condition on the first column
        row.loc['angular_velocity_f0':] = row.loc['angular_velocity_f0':] * -1
    return row

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

    result = st.bootstrap(
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
def sorting_trial_info(stim_info, analysis_methods,exp_date="XXXXXX"):
    #error related to cannot reshape array of size 1624 into shape (57,newaxis) is usually because the temperature is logged in the next row in the trial file
    #errpr related ValueError: Unable to parse string " " at position 0 is usually because the temperature is not logged in the current row in the trial file
    visual_paradigm_name = analysis_methods.get("experiment_name")
    exp_place = analysis_methods.get("exp_place")
    camera_fps=analysis_methods.get("camera_fps")
    pre_stim_interval = analysis_methods.get("prestim_duration")
    stim_info = stim_info.reset_index()
    if type(stim_info.iloc[0,0])==str:### this still has bug because in the session Y:\GN26041\260411\looming\session1\2026-04-11_17-22-53, first frame time is 89.14 sec based on stim_info.iloc[0,0] but it will be 62 sec based on stim_info.iloc[0,1]
        first_event_time=stim_info.iloc[0,1]/camera_fps
    else:
        first_event_time=stim_info.iloc[0,0]/camera_fps
    update_pre_stim_interval=False
    if first_event_time>pre_stim_interval and update_pre_stim_interval:
        analysis_methods.update({"prestim_duration":first_event_time})
    raw_column_number = stim_info.shape[1]
    col_index = [2, 3, 4, 5, 7, 11, 13, 15, 17]
    col_name = [
        "ID",
        "Duration",
        "Size",
        "Colour",
        "numDots",
        "Contrast",
        "VelX",
        "VelY",
        "Coherence",
    ]
    for i, j in zip(col_index, col_name):
        stim_info[["tmp", j]] = stim_info.iloc[:, i].str.split("=", expand=True)
        stim_info[j] = pd.to_numeric(stim_info[j])
    if exp_place.lower() == "zball" or exp_place.lower() == "matrexvr":
        if stim_info['Timestamp'].dtypes=='float64':
            stim_info["ts"]=stim_info['Timestamp']
            stim_info['temperature']=pd.to_numeric(stim_info["Value"].str.replace(r"[()]", "", regex=True).str.split(";",expand=True)[0])
            stim_info['humidity']=pd.to_numeric(stim_info["Value"].str.replace(r"[()]", "", regex=True).str.split(";",expand=True)[1])
            stim_info["temperature"] = stim_info["temperature"].astype("float32")
            stim_info["humidity"] = stim_info["humidity"].astype("float32")
        else:
            stim_info["ts"] = stim_info["Value"].str.replace(r"[()]", "", regex=True)
    elif exp_place.lower() == "vccball":
        stim_info["Value"] = stim_info["Value"].str.replace(r"[()]", "", regex=True)
        if stim_info["Timestamp"].dtypes == "object":
            stim_info["Timestamp"] = stim_info["Timestamp"].str.replace(
                r"[()]", "", regex=True
            )
        stim_info["Value"] = stim_info["Value"].fillna(0)
        stim_info["Timestamp"] = stim_info["Timestamp"].astype(str)
        stim_info["Value"] = stim_info["Value"].astype(str)
        stim_info["ts"] = stim_info[["Timestamp", "Value"]].agg(".".join, axis=1)
    stim_info["ts"] = pd.to_numeric(stim_info["ts"])
    stim_info["ts"] = stim_info["ts"].astype("float32")
    stim_info.drop(
        columns=stim_info.columns[0 : raw_column_number + 1], inplace=True
    )
    if visual_paradigm_name.endswith("sities") or visual_paradigm_name=="density":
        if stim_info["VelX"].unique()[0]==0:
            stim_variable_with_direction = (
                stim_info["VelY"] * stim_info["numDots"] / abs(stim_info["VelY"])
            )
        elif stim_info["VelY"].unique()[0]==0:
            stim_variable_with_direction = (
                stim_info["VelX"] * stim_info["numDots"] / abs(stim_info["VelX"])
            )
    elif visual_paradigm_name.lower() == "coherence":
        stim_variable_with_direction = (
            (stim_info["VelY"]+stim_info["VelX"]) * stim_info["Coherence"] / (abs(stim_info["VelY"])+abs(stim_info["VelX"]))
        )## needs to calculate the direction in this way is because due to some random setup, I made VelY to be the velocity during inter-stimulus interval (VelX to be 0). Vice versa for stimulus presentation.
        ## hence, there is no unique stim_info["VelX"].unique()[0]==0 in this protocol.
    
    if exp_place.lower() == "vccball":
        stim_info["stim_type"] = -1* stim_variable_with_direction.astype(int)
    else:
        stim_info["stim_type"] = stim_variable_with_direction.astype(int)
        # needs to add multiple by -1 because in VCC balls positive value means dots moves from right to left in a window (or counterclock-wise from the top-down view)
        # this is opposite from the parameters at zball. This is because the display environment (ViewWindow nodes were set differently)
        ## from now on, positive value means horizontal degree increment, a clockwise motion in panoroma setup
    stim_type = np.sort(stim_info.stim_type.unique()).tolist()
    return stim_info, stim_type