import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, filedialog

class SignalProcessing:
    def __init__(self):
        self.signal = None

    def read_from_file(self,filename):
        with open(filename,'r') as file:
            data= file.readline()
            self.signal=np.array(list(map(float,data)))

    def plot_continuous_signal(self):
        if self.signal is None:
            print("no signal found")
        time = np.arange(len(self.signal))
        plt.plot(time, self.signal)
        plt.xlabel('time')
        plt.ylabel('x(t)')
        plt.title('Continuous Signal')
        plt.show()

    def plot_discrete_signal(self):
        if self.signal is None:
            print("no signal found")
        time = np.arange(len(self.signal))
        plt.plot(time, self.signal)
        plt.xlabel('time')
        plt.ylabel('x(n)')
        plt.title('discrete Signal')
        plt.show()

    def read_file(self):
        Tk().withdraw()
        filename = filedialog.askopenfilename()
        if filename:
            self.read_from_file(filename)

    def show_gui(self):
        window = Tk()
        window.title("Signal processing")

        label = Label(window, text="Signal processing", font=("Arial", 16))
        label.pack(pady=10)

        read_button = Button(window, text="read file", command=self.read_file)
        read_button.pack(pady=10)

        continuous_button = Button(window, text="Plot Continuous Signal", command=self.plot_continuous_signal)
        continuous_button.pack(pady=5)

        discrete_button = Button(window, text="Plot Discrete Signal", command=self.plot_discrete_signal)
        discrete_button.pack(pady=5)

        window.mainloop()

# Usage example
sp = SignalProcessing()
sp.show_gui()