import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt

def read_signal_from_file(filename):
    samples = []
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

def browse_file():
    global signal
    file_path = filedialog.askopenfilename(filetypes=[('Text files', '*.txt')])
    if file_path:
        signal = read_signal_from_file(file_path)
        plot_signals(signal)

window = tk.Tk()
window.title("Signal Processing")

# Signal generation widgets
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

phase_shift_label = tk.Label(window, text="Phase Shift (degrees):")
phase_shift_label.pack()

phase_shift_entry = tk.Entry(window)
phase_shift_entry.pack()

analog_frequency_label = tk.Label(window, text="Analog Frequency (Hz):")
analog_frequency_label.pack()

analog_frequency_entry = tk.Entry(window)
analog_frequency_entry.pack()

sampling_frequency_label = tk.Label(window, text="Sampling Frequency (Hz):")
sampling_frequency_label.pack()

sampling_frequency_entry = tk.Entry(window)
sampling_frequency_entry.pack()

duration_label = tk.Label(window, text="Duration (seconds):")
duration_label.pack()

duration_entry = tk.Entry(window)
duration_entry.pack()

generate_signal_button = tk.Button(window, text="Generate Signal", command=generate_signal_button_click)
generate_signal_button.pack()

# Load signal from file widgets
browse_button = tk.Button(window, text='Load Signal from File', command=browse_file)
browse_button.pack(pady=10)

# Global signal variable
signal = None

window.mainloop()
