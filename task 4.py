import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt


def plot_dft_discrete(frequency_values, amplitudes, phases):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Plot frequency vs amplitude
    ax1.stem(frequency_values, amplitudes, use_line_collection=True)
    ax1.set_xlabel('Frequency Index (k)')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Frequency vs Amplitude')

    # Plot frequency vs phase
    ax2.stem(frequency_values, phases, use_line_collection=True)
    ax2.set_xlabel('Frequency Index (k)')
    ax2.set_ylabel('Phase (radians)')
    ax2.set_title('Frequency vs Phase')

    return fig


def modify_dft_signal(amplitudes, phases, index, new_amplitude, new_phase):
    if 0 <= index < len(amplitudes):
        amplitudes[index] = new_amplitude
        phases[index] = new_phase


def create_new_window(fig):
    new_window = tk.Toplevel(root)
    new_window.title("Plots")

    canvas = FigureCanvasTkAgg(fig, master=new_window)
    canvas.get_tk_widget().pack()
    canvas.draw()


def read_file(filename):
    x = []
    y = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                x.append(float(parts[0]))
                y.append(float(parts[1]))
    return x, y


def read_dft_data(file_path):
    try:
        with open(file_path, 'r') as file:
            dft_output = []
            skip_lines = 0

            for line in file:
                if skip_lines < 3:
                    skip_lines += 1
                    continue  # Skip the first three lines

                parts = line.strip().split(',')
                if len(parts) == 2:
                    amplitude_str = parts[0].strip()
                    phase_str = parts[1].strip()

                    # Remove 'f' suffix if present
                    if amplitude_str.endswith('f'):
                        amplitude_str = amplitude_str[:-1]

                    if phase_str.endswith('f'):
                        phase_str = phase_str[:-1]

                    amplitude = float(amplitude_str)
                    phase = float(phase_str)
                    dft_output.append((amplitude, phase))
            return dft_output
    except Exception as e:
        print(f"Error reading DFT data: {e}")
        return None


def save_to_txt_file(amplitudes, phases, file_path):
    with open(file_path, 'w') as file:
        file.write("Amplitude\tPhase (radians)\n")
        for amp, phase in zip(amplitudes, phases):
            file.write(f"{amp:.2f}\t{phase:.2f}\n")


def calculate_dft_and_save():
    def load_files():
        file_path1 = filedialog.askopenfilename(title="Load Input Data")
        if not file_path1:
            return
        data1 = read_file(file_path1)
        if data1 is not None:
            x, y = data1

            N = len(x)

            amplitudes = []
            phases = []

            for k in range(N):
                real_sum = 0
                imag_sum = 0

                for n in range(N):
                    angle = -2 * np.pi * k * n / N
                    real_sum += y[n] * np.cos(angle)
                    imag_sum += y[n] * np.sin(angle)

                amplitude = np.sqrt(real_sum ** 2 + imag_sum ** 2)
                phase = np.arctan2(imag_sum, real_sum)

                amplitudes.append(amplitude)
                phases.append(phase)

            save_to_txt_file(amplitudes, phases, 'dft_results.txt')

            input_window = tk.Toplevel(root)
            input_window.title("Sampling Frequency")

            entry_label = tk.Label(input_window, text="Enter Sampling Frequency:")
            entry_label.pack()

            entry = tk.Entry(input_window)
            entry.pack()

            def process_input():
                integer_input = int(entry.get())
                input_window.destroy()

                N = len(amplitudes)
                Ts = 1 / integer_input
                fundamental_frequency = (2 * np.pi) / (N * Ts)
                frequencies = [fundamental_frequency * i for i in range(N)]

                fig = plot_dft_discrete(frequencies, amplitudes, phases)
                create_new_window(fig)

        confirm_button = tk.Button(input_window, text="Confirm", command=process_input)
        confirm_button.pack()

        def modify_and_save():
            try:
                index = int(index_entry.get())
                new_amplitude = float(amplitude_entry.get())
                new_phase = float(phase_entry.get())

                modify_dft_signal(amplitudes, phases, index, new_amplitude, new_phase)
                modified_file_path = filedialog.asksaveasfilename(title="Save Modified DFT Results",
                                                                  defaultextension=".txt")

                if modified_file_path:
                    save_to_txt_file(amplitudes, phases, modified_file_path)
            except ValueError:
                print("Invalid input. Make sure amplitude and phase are valid numbers.")

        # Create a window for modifying DFT results
        modify_window = tk.Toplevel(root)
        modify_window.title("Modify DFT Results")

        index_label = tk.Label(modify_window, text="Signal Index:")
        index_label.pack()

        index_entry = tk.Entry(modify_window)
        index_entry.pack()

        amplitude_label = tk.Label(modify_window, text="New Amplitude:")
        amplitude_label.pack()

        amplitude_entry = tk.Entry(modify_window)
        amplitude_entry.pack()

        phase_label = tk.Label(modify_window, text="New Phase (radians):")
        phase_label.pack()

        phase_entry = tk.Entry(modify_window)
        phase_entry.pack()

        modify_button = tk.Button(modify_window, text="Modify and Save", command=modify_and_save)
        modify_button.pack()

    load_files()


def calculate_idft_and_save():
    def load_files():
        file_path1 = filedialog.askopenfilename(title="Load IDFT Data")
        if not file_path1:
            return
        dft_output = read_dft_data(file_path1)
        if dft_output is not None:
            N = len(dft_output)
            reconstructed_input = []

            for n in range(N):
                real_sum = 0
                imag_sum = 0

                for k, (amplitude, phase) in enumerate(dft_output):
                    angle = 2 * np.pi * k * n / N
                    real_sum += amplitude * np.cos(angle + phase)
                    imag_sum += amplitude * np.sin(angle + phase)

                reconstructed_input.append((n, real_sum / N))

            result_window = tk.Toplevel()
            result_window.title("Reconstructed Input")

            # Create a Text widget to display the reconstructed input
            text_widget = tk.Text(result_window)
            text_widget.pack()

            for n, x_n in reconstructed_input:
                text_widget.insert(tk.END, f"{n} {x_n:.0f}\n")

    load_files()


root = tk.Tk()
root.geometry("220x80")
root.title("DFT && IDFT")

menu_frame = tk.Frame(root)
menu_frame.pack()

bits_button = tk.Button(menu_frame, text="DFT", command=calculate_dft_and_save)
bits_button.pack()

b_button = tk.Button(menu_frame, text="IDFT", command=calculate_idft_and_save)
b_button.pack()

root.mainloop()
