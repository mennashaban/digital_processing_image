import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog

class SignalProcessor:
    def __init__(self):
        self.signal = None

    def read_signal_from_file(self, filename):
        with open(filename, 'r') as file:
            data = file.readlines()
        self.signal = np.array(list(map(float, data)))

    def plot_continuous_signal(self):
        if self.signal is None:
            print("No signal found. Please read a signal first.")
            return
        time = np.arange(len(self.signal))
        plt.plot(time, self.signal)
        plt.xlabel('Time')
        plt.ylabel('x(t)')
        plt.title('Continuous Signal')
        plt.show()

    def plot_discrete_signal(self):
        if self.signal is None:
            print("No signal found. Please read a signal first.")
            return
        time = np.arange(len(self.signal))
        plt.stem(time, self.signal)
        plt.xlabel('Time')
        plt.ylabel('x(n)')
        plt.title('Discrete Signal')
        plt.show()

    def browse_file(self):
        Tk().withdraw()
        filename = filedialog.askopenfilename()
        if filename:
            self.read_signal_from_file(filename)

    def show_gui(self):
        window = Tk()
        window.title("Signal Processor")

        label = Label(window, text="Signal Processor", font=("Arial", 16))
        label.pack(pady=10)

        browse_button = Button(window, text="Browse", command=self.browse_file)
        browse_button.pack(pady=10)

        continuous_button = Button(window, text="Plot Continuous Signal", command=self.plot_continuous_signal)
        continuous_button.pack(pady=5)

        discrete_button = Button(window, text="Plot Discrete Signal", command=self.plot_discrete_signal)
        discrete_button.pack(pady=5)

        window.mainloop()

# Usage example
sp = SignalProcessor()
sp.show_gui()