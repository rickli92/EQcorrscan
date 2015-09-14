#!/usr/bin/python
"""
Utility code for most of the plots used as part of the EQcorrscan package.

Copyright 2015 Calum Chamberlain

This file is part of EQcorrscan.

    EQcorrscan is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    EQcorrscan is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with EQcorrscan.  If not, see <http://www.gnu.org/licenses/>.

"""
import numpy as np
import matplotlib.pylab as plt
def triple_plot(cccsum, trace, threshold, save=False, savefile=''):
    """
    Main function to make a triple plot with a day-long seismogram, day-long
    correlation sum trace and histogram of the correlation sum to show normality

    :type cccsum: numpy.array
    :type trace: obspy.Trace
    :type threshold: float
    :type save: Bool, optional
    :type savefile: String, optional
    """
    if len(cccsum) != len(trace.data):
        print 'cccsum is: '+str(len(cccsum))+' trace is: '+str(len(trace.data))
        raise ValueError('cccsum and trace must have the same number of data points')
    df = trace.stats.sampling_rate
    npts = trace.stats.npts
    t = np.arange(npts, dtype=np.float32) / (df*3600)
    # Generate the subplot for the seismic data
    ax1 = plt.subplot2grid((2,5), (0,0), colspan=4)
    ax1.plot(t, trace.data, 'k')
    ax1.axis('tight')
    ax1.set_ylim([-15*np.mean(np.abs(trace.data)),15*np.mean(np.abs(trace.data))])
    # Generate the subplot for the correlation sum data
    ax2 = plt.subplot2grid((2,5), (1,0), colspan=4, sharex=ax1)
    # Plot the threshold values
    ax2.plot([min(t), max(t)], [threshold, threshold], color='r', lw=1, label="Threshold")
    ax2.plot([min(t), max(t)], [-threshold,-threshold], color='r', lw=1)
    ax2.plot(t, cccsum, 'k')
    ax2.axis('tight')
    ax2.set_ylim([-1.7*threshold, 1.7*threshold])
    ax2.set_xlabel("Time after %s [hr]" % trace.stats.starttime.isoformat())
    # ax2.legend()
    # Generate a small subplot for the histogram of the cccsum data
    ax3 = plt.subplot2grid((2,5), (1,4), sharey=ax2)
    ax3.hist(cccsum, 200, normed=1, histtype='stepfilled', \
             orientation='horizontal', color='black')
    ax3.set_ylim([-5, 5])
    fig=plt.gcf()
    fig.suptitle(trace.id)
    fig.canvas.draw()
    if not save:
        plt.show()
    else:
        plt.savefig(savefile)
    return

def peaks_plot(data, starttime, samp_rate, save=False, peaks=[(0,0)], \
               savefile=''):
    """
    Simple utility code to plot the correlation peaks to check that the peak
    finding routine is running correctly, used in debugging for the EQcorrscan
    module.

    :type data: numpy.array
    :type starttime: obspy.UTCDateTime
    :type samp_rate: float
    :type save: Boolean, optional
    :type peaks: List of Tuple, optional
    :type savefile: String, optional
    """
    npts=len(data)
    t = np.arange(npts, dtype=np.float32) / (samp_rate*3600)
    fig=plt.figure()
    ax1=fig.add_subplot(111)
    ax1.plot(t, data, 'k')
    ax1.scatter(peaks[0][1]/(samp_rate*3600),abs(peaks[0][0]),color='r', label='Peaks')
    for peak in peaks:
        ax1.scatter(peak[1]/(samp_rate*3600),abs(peak[0]),color='r')
    ax1.legend()
    ax1.set_xlabel("Time after %s [hr]" % starttime.isoformat())
    ax1.axis('tight')
    fig.suptitle('Peaks')
    if not save:
        plt.show()
    else:
        plt.savefig(savefile)
    return

def cumulative_detections(dates, template_names, save=False, savefile=''):
    """
    Simple plotting function to take a list of datetime objects and plot
    a cumulative detections list.  Can take dates as a list of lists and will
    plot each list seperately, e.g. if you have dates from more than one
    template it will overlay them in different colours.

    :type dates: list of lists of datetime.datetime
    :param dates: Must be a list of lists of datetime.datetime objects
    :type template_names: list of strings
    :param template_names: List of the template names in order of the dates
    :type save: Boolean, optional
    :type savefile: String, optional
    """
    # Set up a default series of parameters for lines
    colors=['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', \
            'firebrick', 'purple', 'darkgoldenrod', 'gray']
    linestyles=['-','-.', '--', ':']
    # Check that dates is a list of lists
    if type(dates[0]) != list:
        dates=[dates]
    i=0
    j=0
    k=0
    plothandles=[]
    for template_dates in dates:
        template_dates.sort()
        counts=np.arange(0,len(template_dates))
        print str(i)+' '+str(j)+' '+str(k)
        filename,=plt.plot(template_dates,counts, linestyles[j], \
                           color=colors[i], label=template_names[k],\
                           linewidth=3.0)
        k+=1
        plothandles.append(filename)
        if i < len(colors)-1:
            i+=1
        else:
            i=0
            if j < len(linestyles)-1:
                j+=1
            else:
                j=0
    plt.xlabel('Date')
    plt.ylabel('Cumulative detections')
    plt.title('Cumulative detections for all templates')
    plt.legend(loc=2,prop={'size':8},ncol=2)#handles=plothandles)
    if save:
        plt.savefig(savefile)
    else:
        plt.show()
    return

def threeD_gridplot(nodes, save=False, savefile=''):
    """
    Function to plot in 3D a series of grid points.

    :type nodes: List of tuples
    :param nodes: List of tuples of the form (lat, long, depth)
    """
    lats=[]
    longs=[]
    depths=[]
    for node in nodes:
        lats.append(float(node[0]))
        longs.append(float(node[1]))
        depths.append(float(node[2]))
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(lats, longs, depths)
    ax.set_ylabel("Latitude (deg)")
    ax.set_xlabel("Longitude (deg)")
    ax.set_zlabel("Depth(km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    if not save:
        plt.show()
    else:
        plt.savefig(savefile)
    return

def multi_event_singlechan(streams, picks, clip=10.0, pre_pick=2.0):
    """
    Function to plot data from a single channel at a single station for multiple
    events - data will be alligned by their pick-time given in the picks

    :type streams: List of :class:obspy.stream
    :param streams: List of the streams to use, can contain more traces than\
        you plan on plotting
    :type picks: List of :class:PICK
    :param picks: List of picks, one for each stream
    :type clip: Float
    :param clip: Length in seconds to plot, defaults to 10.0
    :type pre_pick: Float
    :param pre_pick: Length in seconds to extract and plot before the pick,\
        defaults to 2.0
    """
    fig, axes = plt.subplots(len(picks), 1, sharex=True)
    axes = axes.ravel()
    for i in xrange(len(picks)):
        tr=streams[i].select(station=picks[i].station, \
            channel=picks[i].channel)[0]
        tr.trim(picks[i].time-pre_pick, picks[i].time-pre_pick+clip)
        y = tr.data
        x = np.arange(len(y))
        x = x/tr.stats.sampling_rate # convert to seconds
        axes[i].plot(x, y, 'k', linewidth=1.1)
        axes[i].set_ylabel(tr.stats.station+'.'+tr.stats.channel, rotation=0)
        axes[i].yaxis.set_ticks([])
        i+=1
    axes[i-1].set_xlabel('Time (s) from start of template')
    plt.subplots_adjust(hspace=0)
    plt.show()
    return

def detection_timeseries(stream, detector, detections):
    """
    Function to plot the data and detector with detections labelled in red,
    will downsample if too many data points.

    :type stream: obspy.Stream
    :type detector: np.array
    :type detections: np.array
    :param detections: array of positions of detections in samples
    """
    from obspy import Trace
    fig, axes = plt.subplots((len(stream)+1), 1, sharex=True)
    axes=axes.ravel()
    samp_rate=stream[0].stats.sampling_rate
    for i in xrange(len(stream)):
        tr=stream[i]
        if tr.stats.sampling_rate > 10:
            tr.decimate(int(tr.stats.sampling_rate/10))
        time=np.arange(0, tr.stats.npts)/float(tr.stats.delta)
        axes[i].plot(tr.data, time)
        axes[i].set_ylabel(tr.stats.station+'.'+tr.stats.channel)
    detector=Trace(detector)
    detector.stats.sampling_rate=samp_rate
    if detector.stats.sampling_rate > 10:
        detector.decimate(int(detector.stats.sampling_rate/10))
    time=np.arange(0, detector.stats.npts)/float(detector.stats.delta)
    detector=detector.data
    axes[len(axes)].plot(detector, time)
    axes[len(axes)].set_xlabel('Time')
    axes[len(axes)].set_ylabel('Detector')
    return

def detection_multiplot(stream, template, times, streamcolour='k',\
        templatecolour='r'):
    """
    Function to plot the stream of data that has been detected in, with the
    template on top of it timed according to a list of given times, just a
    pretty way to show a detection!

    :type stream: obspy.Stream
    :param stream: Stream of data to be plotted as the base (black)
    :type template: obspy.Stream
    :param template: Template to be plotted on top of the base stream (red)
    :type times: List of datetime.datetime
    :param times: list of times of detections in the order of the channels in
                template.
    """
    import datetime as dt
    fig, axes = plt.subplots(len(template), 1, sharex=True)
    axes = axes.ravel()
    print 'Template has '+str(len(template))+' channels'
    for i in xrange(len(template)):
        template_tr=template[i]
        print 'Working on: '+template_tr.stats.station+' '+\
                template_tr.stats.channel
        image=stream.select(station=template_tr.stats.station,\
                            channel='*'+template_tr.stats.channel[-1])
        if not image:
            print 'No data for '+template_tr.stats.station+' '+\
                    template_tr.stats.channel
            continue
        image=image.merge()[0]
        t_start=(times[i]-image.stats.starttime.datetime) # Gives a timedelta
        print t_start
        # Downsample if needed
        if image.stats.sampling_rate > 20:
            image.decimate(int(image.stats.sampling_rate/20))
        if template_tr.stats.sampling_rate > 20:
            template_tr.decimate(int(template_tr.stats.sampling_rate/20))
        image_times=[image.stats.starttime.datetime+dt.timedelta((j*image.stats.delta)/86400)\
                for j in xrange(len(image.data))] # Give list of datetime objects
        t_start=t_start+image.stats.starttime.datetime
        template_times=[t_start+dt.timedelta((j*template_tr.stats.delta)/86400)\
                for j in xrange(len(template_tr.data))]
        print image_times[0]
        print template_times[0]
        axes[i].plot(image_times, image.data,'k')
        axes[i].plot(template_times, template_tr.data,'r')
        axes[i].set_ylabel(template_tr.stats.station+'.'+template_tr.stats.channel)
    axes[len(axes)-1].set_xlabel('Time')
    plt.show()
    return

def threeD_seismplot(stations, nodes):
    """
    Function to plot seismicity and stations in a 3D, movable, zoomable space
    using matplotlibs Axes3D package.

    :type stations: list of tuple
    :param stations: list of one tuple per station of (lat, long, elevation),
                    with up positive
    :type nodes: list of tuple
    :param nodes: list of one tuple per event of (lat, long, depth) with down
                positive
    """
    stalats=[]
    stalongs=[]
    staelevs=[]
    evlats=[]
    evlongs=[]
    evdepths=[]
    for station in stations:
        stalats+=[station[0]]
        stalongs+=[station[1]]
        staelevs+=[station[2]]
    for node in nodes:
        evlats+=[node[0]]
        evlongs+=[node[1]]
        evdepths+=[-1*node[2]]
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(evlats, evlongs, evdepths, marker="x", c="k")
    ax.scatter(stalats, stalongs, staelevs, marker="v", c="r")
    ax.set_ylabel("Latitude (deg)")
    ax.set_xlabel("Longitude (deg)")
    ax.set_zlabel("Depth(km)")
    ax.get_xaxis().get_major_formatter().set_scientific(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    plt.show()
    return

def Noise_plotting(station, channel, PAZ, datasource):
    """
    Function to make use of obspy's PPSD functionality to read in data from
    a single station and the poles-and-zeros for that station before plotting
    the PPSD for this station.  See McNamara(2004) for more details.

    :type station: String
    :param station: Station name as it is in the filenames in the database
    :type channel: String
    :param channel: Channel name as it is in the filenames in the database
    :type PAZ: Dict
    :param PAZ: Must contain, Poles, Zeros, Sensitivity, Gain
        :type Poles: List of Complex
        :type Zeros: List of Complex
        :type Sensitivity: Float
        :type Gain: Float
    :type datasource: String
    :param datasource: The directory in which data can be found, can contain
                        wildcards.

    :returns: PPSD object
    """
    from obspy.signal import PPSD
    from obspy import read as obsread
    import glob

    stafiles=glob.glob(datasource+'/*'+station+'*'+channel+'*')
    stafiles.sort()
    # Initialize PPSD
    st=obsread(stafiles[0])
    ppsd = PPSD(st[0].stats, PAZ)
    for stafile in stafiles[1:]:
        print 'Adding waveform from: '+stafile
        st=obsread(stafile)
        # Add after read to conserve memory
        ppsd.add(st)
    # Plot the PPSD
    ppsd.plot()
    return ppsd

def pretty_template_plot(template, size=(18.5, 10.5), save=False, title=False,\
                        background=False):
    """
    Function to make a pretty plot of a single template, designed to work better
    than the default obspy plotting routine for short data lengths.

    :type template: :class: obspy.Stream
    :type size: tuple
    :type save: Boolean
    :type title: Boolean
    :type backrgound: :class: obspy.stream
    """
    fig, axes = plt.subplots(len(template), 1, sharex=True, figsize=size)
    axes = axes.ravel()
    if not background:
        mintime=template.sort(['starttime'])[0].stats.starttime
    else:
        mintime=background.sort(['starttime'])[0].stats.starttime
    i=0
    template.sort(['station', 'starttime'])
    for tr in template:
        delay=tr.stats.starttime-mintime
        delay*=tr.stats.sampling_rate
        y=tr.data
        x=np.arange(len(y))
        x+=delay
        x=x/tr.stats.sampling_rate
        # x=np.arange(delay, (len(y)*tr.stats.sampling_rate)+delay,\
            # tr.stats.sampling_rate)
        if background:
            btr=background.select(station=tr.stats.station, \
                                channel=tr.stats.channel)[0]
            bdelay=btr.stats.starttime-mintime
            bdelay*=btr.stats.sampling_rate
            by=btr.data
            bx=np.arange(len(by))
            bx+=bdelay
            bx=bx/btr.stats.sampling_rate
            axes[i].plot(bx,by,'k',linewidth=1)
        print tr.stats.station+' '+str(len(x))+' '+str(len(y))
        axes[i].plot(x, y, 'r', linewidth=1.1)
        axes[i].set_ylabel(tr.stats.station+'.'+tr.stats.channel, rotation=0)
        axes[i].yaxis.set_ticks([])
        i+=1
    axes[i-1].set_xlabel('Time (s) from start of template')
    plt.subplots_adjust(hspace=0)
    if title:
        axes[0].set_title(title)
    if not save:
        plt.show()
    else:
        plt.savefig(save)
