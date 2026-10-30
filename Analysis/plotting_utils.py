import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import pandas as pd
import scipy.stats as st

class MplColorHelper:
    def __init__(self, cmap_name, start_val, stop_val):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mpl.colors.Normalize(vmin=start_val, vmax=stop_val)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data,cmap='coolwarm',vmin=0,vmax=2,**kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, orientation="horizontal", location='top',aspect=80 ,**cbar_kw)
    cbar.ax.set_ylabel(cbarlabel,rotation=-90,va="bottom")


    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                  rotation=-30, rotation_mode="xtick")
    ax.set_yticks(range(data.shape[0]), labels=row_labels)
    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=False, bottom=True,
                   labeltop=False, labelbottom=True)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_xlabel("step size (n consecutive frames)", fontsize=14)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.set_ylabel(r'threshold (rad s$^{-1}$)', fontsize=14)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar

def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = mpl.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
    
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
    using_bs_ci=True
    use_mean=False
    stimulus_velocity=64 #unit degree/s
    walk_threshold_tbt=10
    premature_turn=0.25#set this criteria to remove animals starting to make turn turing ISI
    fig, axes = plt.subplots(
        nrows=2, ncols=1, figsize=(12, 8))
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
            confidence_level = 0.95
            #data=(these_angular_velocity,)
            res=st.bootstrap(data=(these_headings,),statistic=np.median,n_resamples=999,vectorized=True,batch=100,random_state=1)
            y1=res.confidence_interval[0]
            y2=res.confidence_interval[1]
            res=st.bootstrap(data=(these_angular_velocity,),statistic=np.median,n_resamples=999,vectorized=True,batch=100,random_state=1)
            w_y1=res.confidence_interval[0]
            w_y2=res.confidence_interval[1]
            ##to plot distribution with 95% confidence interval with normal distribution because it is faster not because it is correct
            #cl95=st.norm.interval(confidence_level,loc=headings_to_plot,scale=st.sem(these_headings))
            # y1=cl95[0][:]
            # y2=cl95[1][:]
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

def plot_example_trajectory(x_all,y_all,start_frame=0,end_frame=None,start_marker=[],end_marker=[],yaw_angular_velocity=[],analysis_methods=None):
    camera_fps=analysis_methods.get('camera_fps')
    markers_size=400
    trajectory_size=40
    colormap_name = "viridis"
    COL = MplColorHelper(colormap_name, 0, 6)
    visualise_section_by_colour=True
    fig, ax= plt.subplots(1, 1, figsize=(8, 8), tight_layout=True)
    fig2,(ax2,ax3)= plt.subplots(2, 1, figsize=(12, 7),sharex=True,tight_layout=True)
    if end_frame==None:
        ax.scatter(y_all[start_frame:],x_all[start_frame:],c=np.arange(len(y_all[start_frame:])), marker=".", alpha=0.5)
    else:
        if visualise_section_by_colour==True:
            ax.scatter(y_all[start_frame:start_marker[0]],x_all[start_frame:start_marker[0]],s=trajectory_size,c='grey',marker=".", alpha=0.5)
            ax.scatter(y_all[start_marker[0]:end_marker[0]],x_all[start_marker[0]:end_marker[0]],s=trajectory_size,c='blue', marker=".", alpha=0.5)
            ax.scatter(y_all[end_marker[0]:start_marker[1]],x_all[end_marker[0]:start_marker[1]],s=trajectory_size,c='grey',marker=".", alpha=0.5)
            ax.scatter(y_all[start_marker[1]:end_marker[1]],x_all[start_marker[1]:end_marker[1]],s=trajectory_size,c='red', marker=".", alpha=0.5)
            ax.scatter(y_all[end_marker[1]:end_frame],x_all[end_marker[1]:end_frame],s=trajectory_size,c='grey',marker=".", alpha=0.5)
            #travel_distance_tbt=euclidean_distance(x_all[start_frame:start_marker[0]],y_all[start_frame:start_marker[0]])
            #velocity_arr = travel_distance_tbt * camera_fps
            angular_velocity_interest=yaw_angular_velocity[start_frame:start_marker[0]]
            #delta_angular_velocity=np.diff(angular_velocity_interest)
            delta_angular_velocity=np.gradient(angular_velocity_interest, 1/camera_fps)
            ax2.plot(np.arange(angular_velocity_interest.shape[0])/camera_fps,angular_velocity_interest,color='grey')
            ax3.plot(np.arange(delta_angular_velocity.shape[0])/camera_fps,delta_angular_velocity,color='grey')
            angular_velocity_interest=yaw_angular_velocity[start_marker[0]:end_marker[0]]
            delta_angular_velocity=np.gradient(angular_velocity_interest, 1/camera_fps)
            
            relative_start=start_marker[0]-start_frame
            ax2.plot(np.arange(relative_start,angular_velocity_interest.shape[0]+relative_start)/camera_fps,angular_velocity_interest,color='blue')
            ax3.plot(np.arange(relative_start,delta_angular_velocity.shape[0]+relative_start)/camera_fps,delta_angular_velocity,color='blue')
            angular_velocity_interest=yaw_angular_velocity[end_marker[0]:start_marker[1]]
            delta_angular_velocity=np.gradient(angular_velocity_interest, 1/camera_fps)
            relative_start=end_marker[0]-start_frame
            ax2.plot(np.arange(relative_start,angular_velocity_interest.shape[0]+relative_start)/camera_fps,angular_velocity_interest,color='grey')
            ax3.plot(np.arange(relative_start,delta_angular_velocity.shape[0]+relative_start)/camera_fps,delta_angular_velocity,color='grey')
            angular_velocity_interest=yaw_angular_velocity[start_marker[1]:end_marker[1]]
            delta_angular_velocity=np.gradient(angular_velocity_interest, 1/camera_fps)
            relative_start=start_marker[1]-start_frame
            ax2.plot(np.arange(relative_start,angular_velocity_interest.shape[0]+relative_start)/camera_fps,angular_velocity_interest,color='red')
            ax3.plot(np.arange(relative_start,delta_angular_velocity.shape[0]+relative_start)/camera_fps,delta_angular_velocity,color='red')
            angular_velocity_interest=yaw_angular_velocity[end_marker[1]:end_frame]
            delta_angular_velocity=np.gradient(angular_velocity_interest, 1/camera_fps)
            relative_start=end_marker[1]-start_frame
            ax2.plot(np.arange(relative_start,angular_velocity_interest.shape[0]+relative_start)/camera_fps,angular_velocity_interest,color='grey')
            ax3.plot(np.arange(relative_start,delta_angular_velocity.shape[0]+relative_start)/camera_fps,delta_angular_velocity,color='grey')
            ax2.set_ylim(-5.4, 5.4)
            ax2.axhline(y=64*np.pi/180,ls='--', lw=1, c='k', alpha=1)
            ax2.axhline(y=-64*np.pi/180,ls='--', lw=1, c='k', alpha=1)
            ax2.set_ylabel('Angular velocity\n'+r'(rad s$^{-1}$)',fontsize=20)
            ax3.set_ylim(-30,30)
            ax2.spines['bottom'].set_visible(False)
            ax2.tick_params(axis='both', which='both', labelsize='large',
                        bottom=False, top=False, labelbottom=False,
                        left=True, right=False, labelleft=True)
            ax3.tick_params(axis='both', which='both', labelsize='large',
            bottom=False, top=False, labelbottom=True,
            left=True, right=False, labelleft=True)
            ax3.spines['top'].set_visible(False)
            ax3.set_ylabel('Angular acceleration\n'+r'(rad s$^{-2}$)',fontsize=20)
            ax3.set_xticks([0,20,40,60,80],labels=[0,20,40,60,80],fontsize=16)
            ax3.set_xlabel("Time (s)",fontsize=20)
        else:
            ax.scatter(y_all[start_frame:end_frame],x_all[start_frame:end_frame],s=trajectory_size,color=np.arange(len(y_all[start_frame:end_frame])), marker=".", alpha=0.5)
        #
        ax.set_xlim(-160, -120)
        ax.set_ylim(-320, -280)
        ax.axis('off')
    if type(start_marker) == list:
        if len(start_marker) > 0:
            for i in range(len(start_marker)):
                ax.scatter(y_all[start_marker[i]],x_all[start_marker[i]],s=markers_size,color=COL.get_rgb(6), marker="*",edgecolors='black')
    else:
        if start_marker > 0:
            ax.scatter(y_all[start_marker],x_all[start_marker],s=markers_size,color=COL.get_rgb(6), marker="*",edgecolors='black')

    if type(end_marker) == list:
        if len(end_marker) > 0:
            for i in range(len(end_marker)):
                ax.scatter(y_all[end_marker[i]],x_all[end_marker[i]],s=markers_size,color=COL.get_rgb(0), marker="*",edgecolors='black')
    else:
        if end_marker > 0:
            ax.scatter(y_all[end_marker],x_all[end_marker],s=markers_size,color=COL.get_rgb(0), marker="*",edgecolors='black')
    return fig,fig2