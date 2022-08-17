import numpy as np
import sys
from ecgdetectors import Detectors
import bwr
import matplotlib.pyplot as plt

SAMPLE_RATE = 250


def openData():
    dataDir = 'Data/ECG.tsv'
    unfiltered_ecg_dat = np.loadtxt(dataDir)
    return unfiltered_ecg_dat[:, 0]


def r_peaks(data) -> list[int]:
    detectors = Detectors(SAMPLE_RATE)
    # selected detector by the user (default is the two average one)
    seldet = -1

    if len(sys.argv) > 1:
        seldet = int(sys.argv[1])
    else:
        print("Select another detector by specifying the index as: {} <index>".format(
            sys.argv[0]))
        print("The following detectors are available:")
        for i in range(len(detectors.get_detector_list())):
            print(i, detectors.get_detector_list()[i][0])
        print("The default detector is the Two Average detector.")

    if seldet < 0:
        # default detector
        return detectors.two_average_detector(data)
    # We use the input argument to select a detector
    return detectors.get_detector_list()[seldet][1](data)


def show_r_peaks(data, r_peaks_indice: list[int]):
    plt.figure()
    plt.plot(data)
    plt.plot(r_peaks_indice, data[r_peaks_indice], 'ro')
    plt.title("Detected R peaks")
    plt.show()


def show_r_distances(r_peaks_indice: list[int]):
    r_peaks_distance: list[int] = []
    for i in range(1, len(r_peaks_indice)):
        r_peaks_distance.append(r_peaks_indice[i] - r_peaks_indice[i - 1])
    length: int = len(r_peaks_distance)
    if length > 1:
        plt.title("R Distance")
        plt.xlabel("R1")
        plt.ylabel("R2")

        distanceRelationToBase: list[float] = []
        for i in range(1, len(r_peaks_distance)):
            distanceRelationToBase.append(
                i * (r_peaks_distance[i] / r_peaks_distance[0]))
        plt.scatter(np.arange(1, length), distanceRelationToBase)
        xpoints = ypoints = plt.xlim()
        plt.plot(xpoints, ypoints, linestyle='--',
                 color='r', lw=1, scalex=False, scaley=False)
        plt.show()


def removeBaseLine(signal):
    baseline = bwr.calc_baseline(signal)

    # Remove baseline from orgianl signal
    ecg_out = signal - baseline

    plt.subplot(2, 1, 1)
    plt.plot(signal, "b-", label="signal")
    plt.plot(baseline, "r-", label="baseline")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(ecg_out, "b-", label="signal - baseline")
    plt.legend()
    plt.show()

    return ecg_out


if __name__ == '__main__':
    signal = openData()
    signalMinusBaseLine = removeBaseLine(signal)
    r_peaks_indice: list[int] = r_peaks(signalMinusBaseLine)
    show_r_peaks(signalMinusBaseLine, r_peaks_indice)
    show_r_distances(r_peaks_indice)
