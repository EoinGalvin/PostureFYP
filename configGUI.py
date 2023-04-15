import tkinter as tk
from configparser import ConfigParser

config = ConfigParser()


def saveConfig(heightMax, heightMin, distanceMax, distanceMin, cOffsetMax, eyeAngleMax):
    try:
        config.read('config.ini')
        config.set('ergonomics', 'HEIGHT_MAX', heightMax)
        config.set('ergonomics', 'HEIGHT_MIN', heightMin)
        config.set('ergonomics', 'DISTANCE_MAX', distanceMax)
        config.set('ergonomics', 'DISTANCE_MIN', distanceMin)
        config.set('ergonomics', 'C_OFFSET_MAX', cOffsetMax)
        config.set('ergonomics', 'EYE_ANGLE_MAX', eyeAngleMax)
    except IOError:
        print("failed to save configuration.")

    with open('config.ini', 'w') as f:
        config.write(f)


def configGUI():
    configWindow = tk.Tk()
    configWindow.geometry("400x400")
    configWindow.title("Configuration")

    heightMinFrame = tk.Frame(configWindow)
    heightMinLabel = tk.Label(heightMinFrame, text="Min Height:")
    heightMinLabel.grid(row=0, column=0)
    heightMinEntry = tk.Entry(heightMinFrame)
    heightMinEntry.grid(row=0, column=1)

    heightMaxFrame = tk.Frame(configWindow)
    heightMaxLabel = tk.Label(heightMaxFrame, text="Max Height:")
    heightMaxLabel.grid(row=0, column=0)
    heightMaxEntry = tk.Entry(heightMaxFrame)
    heightMaxEntry.grid(row=0, column=1)

    distanceMinFrame = tk.Frame(configWindow)
    distanceMinLabel = tk.Label(distanceMinFrame, text="Min Distance:")
    distanceMinLabel.grid(row=0, column=0)
    distanceMinEntry = tk.Entry(distanceMinFrame)
    distanceMinEntry.grid(row=0, column=1)

    distanceMaxFrame = tk.Frame(configWindow)
    distanceMaxLabel = tk.Label(distanceMaxFrame, text="Max Distance:")
    distanceMaxLabel.grid(row=0, column=0)
    distanceMaxEntry = tk.Entry(distanceMaxFrame)
    distanceMaxEntry.grid(row=0, column=1)

    cOffsetMaxFrame = tk.Frame(configWindow)
    cOffsetMaxLabel = tk.Label(cOffsetMaxFrame, text="Max C-Offset:")
    cOffsetMaxLabel.grid(row=0, column=0)
    cOffsetMaxEntry = tk.Entry(cOffsetMaxFrame)
    cOffsetMaxEntry.grid(row=0, column=1)

    eyeAngleMaxFrame = tk.Frame(configWindow)
    eyeAngleMaxLabel = tk.Label(eyeAngleMaxFrame, text="Max Eye Angle:")
    eyeAngleMaxLabel.grid(row=0, column=0)
    eyeAngleMaxEntry = tk.Entry(eyeAngleMaxFrame)
    eyeAngleMaxEntry.grid(row=0, column=1)

    try:
        config.read('config.ini')
        heightMaxEntry.insert(10, config.get('ergonomics', 'HEIGHT_MAX'))
        heightMinEntry.insert(10, config.get('ergonomics', 'HEIGHT_MIN'))
        distanceMaxEntry.insert(10, config.get('ergonomics', 'DISTANCE_MAX'))
        distanceMinEntry.insert(10, config.get('ergonomics', 'DISTANCE_MIN'))
        cOffsetMaxEntry.insert(10, config.get('ergonomics', 'C_OFFSET_MAX'))
        eyeAngleMaxEntry.insert(10, config.get('ergonomics', 'EYE_ANGLE_MAX'))
    except IOError:
        print("failed to read configuration file.")

    heightMaxFrame.place(x=16, y=0)
    heightMinFrame.place(x=18, y=30)
    distanceMaxFrame.place(x=7, y=60)
    distanceMinFrame.place(x=9, y=90)
    cOffsetMaxFrame.place(x=7, y=120)
    eyeAngleMaxFrame.place(x=0, y=150)

    submitButton = tk.Button(configWindow, text="Submit Configuration", command=lambda: saveConfig(
        heightMaxEntry.get(),
        heightMinEntry.get(),
        distanceMaxEntry.get(),
        distanceMinEntry.get(),
        cOffsetMaxEntry.get(),
        eyeAngleMaxEntry.get()
    ))
    submitButton.place(x=87, y=180)

    configWindow.mainloop()



