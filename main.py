import numpy as np
import sys
from ecgdetectors import Detectors
import hrv
import matplotlib.pyplot as plt

SAMPLE_RATE = 250


def openData():
    dataDir = 'Data/ECG.tsv'
    unfiltered_ecg_dat = np.loadtxt(dataDir)
    unfiltered_ecg_dat = unfiltered_ecg_dat[:, 0]
    return unfiltered_ecg_dat


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


if __name__ == '__main__':
    data = openData()
    expandedData = np.expand_dims(data, axis=0)
    r_peaks_indice: list[int] = r_peaks(data)
    show_r_peaks(data, r_peaks_indice)

    r_peaks_distance: list[int] = []
    for i in range(1, len(r_peaks_indice)):
        r_peaks_distance.append(r_peaks_indice[i] - r_peaks_indice[i - 1])

    length: int = len(r_peaks_distance)
    if length > 1:
        plt.title("R Distance")
        plt.xlabel("R1")
        plt.ylabel("R2")
        x = np.arange(1, length)

        distanceRelationToBase: list[float] = []
        distIndex: int = 1
        baseDistance = r_peaks_distance[0]

        for x_element in x:
            distanceRelationToBase.append(
                x_element * (r_peaks_distance[distIndex] / baseDistance))
            distIndex += 1
        plt.scatter(x, distanceRelationToBase)
        plt.show()
