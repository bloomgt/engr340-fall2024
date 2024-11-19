import numpy as np
import scipy
#import matplotlib.pyplot as plt
from scipy.signal import find_peaks, square
from ekg_testbench import EKGTestBench

def detect_heartbeats(filepath):
    """
    Perform analysis to detect location of heartbeats
    :param filepath: A valid path to a CSV file of heart beats
    :return: signal: a signal that will be plotted
    beats: the indices of detected heartbeats
    """
    if filepath == '':
        return list()

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    ## your code here
    data = np.genfromtxt(path, delimiter=',')

    # save each vector as own variable
    ## your code here
    time = data[2:, 0]
    mlii = data[2:, 1]
    voltage = data[2:, 2]

    # identify one column to process. Call that column signal

    signal = voltage[:3000] ## your code here

    # plt.plot(time[:len(signal)], signal)
    # plt.title("Raw Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # pass data through LOW PASS FILTER (OPTIONAL)
    ## your code here
    fs = 250  # Sampling frequency
    fc = 12  # Cutoff frequency (Hz)
    n = 6  # Filter order
    # Normalize cutoff frequency to Nyquist frequency (fs/2)
    nyquist = 0.5 * fs
    normal_cutoff = fc / nyquist
    # Generate Butterworth filter coefficients
    b, a = scipy.signal.butter(n, normal_cutoff, btype="low", analog=False)
    # Apply filter to the voltage data
    low_pass_data = scipy.signal.filtfilt(b, a, signal)

    # plt.plot(time[:len(low_pass_data)], low_pass_data)
    # plt.title("Low Pass Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
    ## your code here
    fs = 250  # Sampling frequency
    fc = 5  # Cutoff frequency (Hz)
    n = 6  # Filter order
    # Normalize cutoff frequency to Nyquist frequency (fs/2)
    nyquist = 0.5 * fs
    normal_cutoff = fc / nyquist
    # Generate Butterworth filter coefficients
    b, a = scipy.signal.butter(n, normal_cutoff, btype="high", analog=False)
    # Apply filter to the voltage data
    bandpass_data = scipy.signal.filtfilt(b, a, low_pass_data)

    # plt.plot(time[:len(bandpass_data)], bandpass_data)
    # plt.title("Band Pass Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # pass data through differentiator
    ## your code here
    diffs = np.diff(bandpass_data)

    # plt.plot(time[:len(diffs)], diffs)
    # plt.title("Differentiated Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # pass data through square function
    ## your code here
    square_data = np.square(diffs)


    # plt.plot(time[:len(square_data)], square_data)
    # plt.title("Squared Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # pass through moving average window
    ## your code here
    window_size = 35 #calcualted to be 37.5 for 150ms window at 250 samp/s
    window = np.ones(window_size)
    moving_average = np.convolve(square_data, window)

    # plt.plot(time[:len(moving_average)], moving_average)
    # plt.title("Moving Average Signal")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Voltage [V]")

    # use find_peaks to identify peaks within averaged/filtered data
    # save the peaks result and return as part of testbench result
    ## your code here peaks,_ = find_peaks(....)

    ######### beats, _ = find_peaks(moving_average, height=0.0075, width=5)

    # set a detection threshold (YOUR VALUE BELOW)
    detection_threshold = 0.1
    # set a heart beat time out (YOUR VALUE BELOW)
    detection_time_out = 100
    # track the last time we found a beat
    last_detected_index = -1
    # keep not of where we are in the data
    current_index = 0
    # store indices of all found beats
    peaks = [0]
    noise = []
    beats = []
    # initialize rr variables
    rr = 100
    rrlast = 100
    # initialize peak variables
    pp = 0.001
    pplast = 0.001
    # initialize noise variables
    nn = 0.001
    nnlast = 0.001

    # loop through signal finding beats
    for value in moving_average:
        if current_index > 3 and value < moving_average[current_index - 1] and moving_average[current_index - 1] > moving_average[current_index - 2]:
            if (current_index - last_detected_index) > detection_time_out:
                if (current_index - last_detected_index) > (1.66*rr) and value > (0.5*detection_threshold):
                    peaks.append(value)
                    pplast = value
                    beats.append(current_index)
                    rrlast = current_index - last_detected_index
                    last_detected_index = current_index
                if value > detection_threshold:
                    peaks.append(value)
                    pplast = value
                    beats.append(current_index)
                    rrlast = current_index - last_detected_index
                    last_detected_index = current_index
                else:
                    noise.append(value)
                    nnlast = value

        if current_index > 5:
            peak_avg = np.mean(peaks)
            pp = (0.125*pplast) + (0.875*peak_avg)
            noise_avg = np.mean(noise)
            nn = (0.125*nnlast) + (0.875*noise_avg)
            detection_threshold = nn + (0.25*(pp-nn))
            rr = (0.125*rrlast) +(0.875*rr)
        else:
            detection_threshold = 0.1
        current_index += 1

    beats = np.asarray(beats)

    # Create a figure with 7 subplots in a single column
    fig, axs = plt.subplots(7, 1, figsize=(10, 15))

    axs[0].plot(time[:len(signal)], signal)
    axs[0].set_title("Raw Signal")

    axs[1].plot(time[:len(low_pass_data)], low_pass_data)
    axs[1].set_title("Low Pass Signal")

    axs[2].plot(time[:len(bandpass_data)], bandpass_data)
    axs[2].set_title("Band Pass Signal")

    axs[3].plot(time[:len(diffs)], diffs)
    axs[3].set_title("Differentiated Signal")

    axs[4].plot(time[:len(square_data)], square_data)
    axs[4].set_title("Squared Signal")

    axs[5].plot(time[:len(diffs)], moving_average[:len(diffs)])
    axs[5].set_title("Moving Average Signal")

    axs[6].plot(time[:len(diffs)], moving_average[:len(diffs)])
    axs[6].plot(time[beats], moving_average[beats], 'X')
    axs[6].set_title("Moving Average Signal")

    plt.tight_layout()
    plt.show()

    # do not modify this line
    return signal, beats


# when running this file directly, this will execute first
if __name__ == "__main__":

    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    database_name = 'mitdb_201'

    # set to true if you wish to generate a debug file
    file_debug = False

    # set to true if you wish to print overall stats to the screen
    print_debug = True

    # set to true if you wish to show a plot of each detection process
    show_plot = False

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    path_to_folder = "../../../data/ekg/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = detect_heartbeats(signal_filepath)

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    print("Done!")
