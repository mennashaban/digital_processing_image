import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize the original_signal globally
original_signal = []

#----------for normalization----------
def read_data(x, y):
    file_path = filedialog.askopenfilename()
    x.clear()
    y.clear()
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                values = line.split()
                if len(values) == 2:
                    x.append(float(values[0]))
                    y.append(float(values[1]))
#------------------------------------------
def normalization_frame_window():
    x = []
    y = []
    new_window = tk.Toplevel(window)
    new_window.geometry("200x150")
    normalizationFrame = tk.Frame(new_window)
    uploadButton = tk.Button(
        normalizationFrame, text="Upload Signal", command=lambda: read_data(x, y))
    uploadButton.pack(pady=10)
    label_val = tk.Label(normalizationFrame, text="Normalization Range")
    label_val.pack()
    types = ["-1 to 1", "0 to 1"]
    type_var = tk.StringVar(normalizationFrame)
    type_var.set("Select an option")
    menu = tk.OptionMenu(normalizationFrame, type_var, *types)
    menu.pack(pady=10)
#--------------------------------------------
    def normalization_plot(x, y):
        plt.subplot(2, 1, 1)
        plt.plot(x, y, label='Original')
        plt.legend()
        plt.subplot(2, 1, 2)
        if type_var.get() == "-1 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [(2 * (val - min_value) / (max_value - min_value)) - 1 for val in y]
            y = normalized_data
        elif type_var.get() == "0 to 1":
            min_value = min(y)
            max_value = max(y)
            normalized_data = [(val - min_value) / (max_value - min_value) for val in y]
            y = normalized_data
        plt.plot(x, y, label='Normalization Range: ' + type_var.get())
        plt.legend()
        plt.tight_layout()
        plt.show()

    plotButton = tk.Button(normalizationFrame, text="Plot", command=lambda: normalization_plot(x, y))
    plotButton.pack(pady=10)
    normalizationFrame.pack()
#--------------------------------------------------------------------------

def read_signal_from_file(filename):
    samples = []   #store the signals data
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                time, amplitude = map(float, parts)
                samples.append((time, amplitude))
    return np.array(samples)

def plot_signals(signal):
    if signal is not None:
        time, amplitude = zip(*signal)
        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
        ax1.plot(time, amplitude)
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Continuous Signal')
        ax2.stem(time, amplitude, linefmt='-', markerfmt='o', basefmt=' ')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Discrete Signal')
        plt.tight_layout()
        plt.show()

def generate_signal(wave_type, amplitude, phase_shift, analog_frequency, sampling_frequency, duration):
    t = np.linspace(0, duration, int(sampling_frequency * duration), endpoint=False)
    omega = 2 * np.pi * analog_frequency
    phase = np.deg2rad(phase_shift)

    if wave_type == 'sine':
        signal = amplitude * np.sin(2 * np.pi * analog_frequency / sampling_frequency * t + phase)
    elif wave_type == 'cosine':
        signal = amplitude * np.cos(2 * np.pi * analog_frequency / sampling_frequency * t + phase)
    else:
        raise ValueError('Invalid wave type. Must be either "sine" or "cosine."')

    return t, signal

def plot_signal(t, signal):
    plt.plot(t, signal)
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.title('Generated Signal')
    plt.grid(True)
    plt.show()

def generate_signal_button_click():
    wave_type = waveform_var.get()
    amplitude = float(amplitude_entry.get())
    phase_shift = float(phase_shift_entry.get())
    analog_frequency = float(analog_frequency_entry.get())
    sampling_frequency = float(sampling_frequency_entry.get())
    duration = float(duration_entry.get())

    t, signal = generate_signal(wave_type, amplitude, phase_shift, analog_frequency, sampling_frequency, duration)
    plot_signal(t, signal)


def perform_addition():
    file_paths = filedialog.askopenfilenames(filetypes=[('Text files', '*.txt')])
    if file_paths:
        signals = []
        for file_path in file_paths:
            signal = read_signal_from_file(file_path)
            signals.append(signal)

        if len(signals) >= 2:
            summed_signal = np.sum([signal[:, 1] for signal in signals], axis=0)
            plot_signal(signals[0][:, 0], summed_signal)
        else:
            print("Please select at least two files.")


def perform_subtraction():
    file_paths = filedialog.askopenfilenames(filetypes=[('Text files', '*.txt')])
    if file_paths:
        signals = []
        for file_path in file_paths:
            signal = read_signal_from_file(file_path)
            signals.append(signal[3:])

        subtracted_signal = np.subtract(signals[0], signals[1])

        for signal in signals[2:]:
            subtracted_signal = np.subtract(subtracted_signal, signal)

        plot_signal(subtracted_signal[:, 0], subtracted_signal[:, 1])

def perform_multiplication():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        signal = read_signal_from_file(file_path)
        constant = float(input("Enter the constant value: "))  # Prompt the user to enter the constant value

        multiplied_signal = signal.copy()
        multiplied_signal[:, 1] *= constant

        plot_signal(multiplied_signal[:, 0], multiplied_signal[:, 1])

def perform_squaring():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        signal = read_signal_from_file(file_path)
        squared_signal = signal.copy()
        squared_signal[:, 1] = squared_signal[:, 1] ** 2

        plot_signal(squared_signal[:, 0], squared_signal[:, 1])

def accumulate_signal(signal):
    accumulated_signal = np.cumsum(signal[:, 1])
    return signal[:, 0], accumulated_signal

def perform_accumulation():
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        signal = read_signal_from_file(file_path)
        t, accumulated_signal = accumulate_signal(signal)
        plot_signal(t, accumulated_signal)

def browse_file():
    global signal
    file_paths = filedialog.askopenfilenames(filetypes=[('Text files', '*.txt')])
    if file_paths:
        signal = read_signal_from_file(file_paths[0])
        plot_signals(signal)


# Function to upload a signal file
def upload_signal():
    global original_signal  # Declare original_signal as a global variable
    file_path = filedialog.askopenfilename()
    if file_path:
        original_signal.clear()  # Clear the previous signal if any
        with open(file_path, 'r') as file:
            original_signal = [tuple(map(float, line.strip().split())) for line in file]
        result_label.config(text="Signal uploaded successfully!")
def shift_signal():
    try:
        constant = float(entry_constant.get())
        shifted_signal = [(x[0] + constant, x[1]) for x in original_signal]

        ax.clear()
        original_x = [x[0] for x in original_signal]
        shifted_x = [x[0] for x in shifted_signal]
        original_y = [x[1] for x in original_signal]
        shifted_y = [x[1] for x in shifted_signal]

        ax.plot(original_x, original_y, label='Original Signal', linestyle='-')
        ax.plot(shifted_x, shifted_y, label=f'Shifted Signal (+{constant})', linestyle='-')
        ax.legend()
        canvas.draw()
    except ValueError:
        result_label.config(text="Invalid constant value!")


# Create a tkinter window
window = tk.Tk()
window.title("Signal processing")

# Create and configure GUI elements
frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

#----------------------------------------------------
waveform_var = tk.StringVar()
waveform_var.set("sine")

waveform_label = tk.Label(window, text="Waveform:")
waveform_label.pack()
waveform_option_menu = tk.OptionMenu(window, waveform_var, "sine", "cosine")
waveform_option_menu.pack()

amplitude_label = tk.Label(window, text="Amplitude:")
amplitude_label.pack()
amplitude_entry = tk.Entry(window)
amplitude_entry.pack()

phase_shift_label = tk.Label(window, text="Phase Shift:")
phase_shift_label.pack()
phase_shift_entry = tk.Entry(window)
phase_shift_entry.pack()

analog_frequency_label = tk.Label(window, text="Analog Frequency:")
analog_frequency_label.pack()
analog_frequency_entry = tk.Entry(window)
analog_frequency_entry.pack()

sampling_frequency_label = tk.Label(window, text="Sampling Frequency:")
sampling_frequency_label.pack()
sampling_frequency_entry = tk.Entry(window)
sampling_frequency_entry.pack()

duration_label = tk.Label(window, text="Duration:")
duration_label.pack()
duration_entry = tk.Entry(window)
duration_entry.pack()

generate_signal_button = tk.Button(window, text="Generate Signal", command=generate_signal_button_click)
generate_signal_button.pack()

#------------normalization-----------------------
openWindowButton = tk.Button(window, text="Open Normalization Window", command=normalization_frame_window)
openWindowButton.pack()
#---------------------------------------------

# Signal processing widgets
addition_button = tk.Button(window, text="Perform Addition", command=perform_addition)
addition_button.pack()

subtraction_button = tk.Button(window, text="Perform Subtraction", command=perform_subtraction)
subtraction_button.pack()

multiplication_button = tk.Button(window, text="Perform Multiplication", command=perform_multiplication)
multiplication_button.pack()

multiplication_button = tk.Button(window, text="Perform squaring", command=perform_squaring)
multiplication_button.pack()

accumulation_button = tk.Button(window, text="Perform Accumulation", command=perform_accumulation)
accumulation_button.pack()

browse_button = tk.Button(window, text="Browse File", command=browse_file)
browse_button.pack()

upload_button = tk.Button(frame, text="Upload Signal", command=upload_signal)
upload_button.grid(row=0, column=8)

result_label = tk.Label(frame, text="")
result_label.grid(row=2, column=0, columnspan=3)


# Create a Matplotlib figure and canvas to display the signal
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()


label_constant = tk.Label(frame, text="Enter Constant:")
label_constant.grid(row=4, column=0)

entry_constant = tk.Entry(frame)
entry_constant.grid(row=4, column=1)

shift_button = tk.Button(frame, text="Shift Signal", command=shift_signal)
shift_button.grid(row=4, column=2)

result_label = tk.Label(frame, text="")
result_label.grid(row=5, column=3, columnspan=3)

window.mainloop()