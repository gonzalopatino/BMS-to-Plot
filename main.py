import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from tkinter import Tk, Label, Button, filedialog

def load_data(filepath):
    # Load and preprocess the data
    data = pd.read_csv(filepath, skiprows=7, parse_dates=['DateTime'])
    data['TimeInHours'] = (data['DateTime'] - data['DateTime'].iloc[0]).dt.total_seconds() / 3600
    return data

def plot_data(data):
    # Create figure and axes
    fig, axs = plt.subplots(3, figsize=(10, 15), sharex=True)

    # Plotting the data
    axs[0].plot(data['TimeInHours'], data['Voltage'], 'b-', label='Voltage (mV)')
    axs[1].plot(data['TimeInHours'], data['AvgCurrent'], 'r-', label='Average Current (mA)')
    axs[2].plot(data['TimeInHours'], data['Temperature'], 'g-', label='Temperature (°C)')

    # Setting titles and labels
    axs[0].set_title('Voltage Over Time')
    axs[1].set_title('Average Current Over Time')
    axs[2].set_title('Temperature Over Time')
    axs[2].set_xlabel('Time (hours)')

    for ax in axs:
        ax.legend()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.minorticks_on()
        ax.xaxis.set_major_locator(plt.MaxNLocator(10))
        ax.yaxis.set_major_locator(plt.MaxNLocator(10))

    # Adding a cursor that displays the coordinate pair on the plot
    def ondblclick(event):
        if event.dblclick:
            if event.inaxes is not None:
                x, y = event.xdata, event.ydata
                event.inaxes.plot(x, y, 'ro')
                event.inaxes.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
                plt.draw()

    fig.canvas.mpl_connect('button_press_event', ondblclick)

    plt.tight_layout()
    plt.show()

def upload_file():
    root = Tk()
    root.withdraw()  # Hide the root window
    filepath = filedialog.askopenfilename()
    if filepath:
        data = load_data(filepath)
        plot_data(data)

def main():
    root = Tk()
    root.title("Battery Management Studio Data Plotter- Developed by Gonzalo Patino for Cadex Electronics")

    Label(root, text="Use this application to turn .log files from Battery Management Studio into plots for smart batteries at Cadex").pack(pady=10)

    Button(root, text="Upload File", command=upload_file).pack(pady=5)
    Button(root, text="Close", command=root.destroy).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
