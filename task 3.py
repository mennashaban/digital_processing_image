import math
import tkinter as tk
from tkinter import filedialog
#from QuanTest1 import QuantizationTest1
class Signal:
    def __init__(self, samples, periodic):
        self.Samples = samples
        self.Periodic = periodic

def quantize_signal(input_signal, input_num_bits=None, input_level=None):
    _SignalSamples = input_signal.Samples
    _periodic = input_signal.Periodic

    if input_num_bits is None and input_level is None:
        input_num_bits = int(input("Enter the number of bits for quantization: "))

    if input_num_bits is not None:
        input_level = 2 ** input_num_bits

    mini = min(_SignalSamples)
    maxi = max(_SignalSamples)
    delta = (maxi - mini) / input_level

    levels_intervals = []
    levels_midpoints = []
    start = mini
    end = maxi
    for i in range(input_level):
        end = start + delta
        levels_intervals.append((start, end))
        levels_midpoints.append(round((start + end) / 2.0, 3))
        start = end

    OutputQuantizedSignal = Signal([], _periodic)
    OutputIntervalIndices = []
    OutputEncodedSignal = []
    OutputSamplesError = []

    for sample in _SignalSamples:
        interval = (((sample - mini) / (maxi - mini)) * input_level)
        interval_index = round(interval)
        if interval_index > interval:
            interval_index -= 1
        if interval_index == input_level:
            interval_index -= 1

        OutputIntervalIndices.append(interval_index + 1)
        OutputQuantizedSignal.Samples.append(levels_midpoints[interval_index])
        encoded = format(interval_index, '0' + str(input_num_bits) + 'b')
        OutputEncodedSignal.append(encoded)
        OutputSamplesError.append(levels_midpoints[interval_index] - sample)

    return OutputQuantizedSignal, OutputIntervalIndices, OutputEncodedSignal, OutputSamplesError

def load_signal_from_file(file_path):
    samples = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    value = float(parts[1])
                    samples.append(value)
    except Exception as e:
        print("Error loading the input signal:", e)
    return Signal(samples, False)

def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    file_path = filedialog.askopenfilename(title="Select the input file")

    if not file_path:
        print("No file selected. Exiting.")
        return

    input_signal = load_signal_from_file(file_path)

    if input_signal:
        OutputQuantizedSignal, OutputIntervalIndices, OutputEncodedSignal, OutputSamplesError = quantize_signal(input_signal)

        print("Quantized Signal:", OutputQuantizedSignal.Samples)
        print("Interval Indices:", OutputIntervalIndices)
        print("Encoded Signal:", OutputEncodedSignal)
        print("Quantization Error:", OutputSamplesError)
    #QuantizationTest1("Quan1_Out.txt", OutputEncodedSignal, OutputQuantizedSignal)

if __name__ == '__main__':
    main()

