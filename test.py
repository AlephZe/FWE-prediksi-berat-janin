import tkinter as tk
from tkinter import filedialog
import cv2
import math

# Variables to store clicked points
length_points = []
diameter_points = []
image = None
# Known scale (for example, in millimeters per pixel)
scale = 0.02855   # Adjust this value according to your scale

# Function to calculate and display the distance between two points in physical units
def calculate_distance(point1, point2):
    # Calculate the Euclidean distance in physical units
    distance = math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2) * scale
    # print real pixel distance
    return distance

# Function to draw lines and distance text between points
def draw_lines_and_distances(image, points):
    for i in range(1, len(points)):
        cv2.line(image, points[i - 1], points[i], (0, 255, 0), 2)
        distance = calculate_distance(points[i - 1], points[i])
        text_position = (
            int((points[i - 1][0] + points[i][0]) / 2),
            int((points[i - 1][1] + points[i][1]) / 2)
        )
        cv2.putText(image, f'{distance:.2f} cm', text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Function to handle mouse clicks
def mark_point(event, x, y, flags, param):
    global length_points, diameter_points, marked_image

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(length_points) < 2:
            length_points.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 5, (0, 0, 255), -1)
            # If both points are obtained for length, draw lines and distances
            if len(length_points) == 2:
                draw_lines_and_distances(marked_image, length_points)
        elif len(diameter_points) < 2:
            diameter_points.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 5, (0, 0, 255), -1)
            # If both points are obtained for diameter, draw lines and distances
            if len(diameter_points) == 2:
                draw_lines_and_distances(marked_image, diameter_points)

        # If both sets of points are obtained, proceed to the next screen
        if len(length_points) == 2 and len(diameter_points) == 2:
            cv2.destroyAllWindows()
            next_screen()  # You can define the next screen function here

        # Display the marked image
        cv2.imshow('Marked Image', marked_image)

# Function to proceed to the next screen
def next_screen():
    # close opencv window
    cv2.destroyAllWindows()
    # change tkinter window
    root.geometry("300x300")
    # calculate length and diameter
    length = calculate_distance(length_points[0], length_points[1])
    diameter = calculate_distance(diameter_points[0], diameter_points[1])
    # coordinates of the first point and the second point
    x1, y1 = length_points[0]
    x2, y2 = length_points[1]

    # show coordinates of the first point
    x1_label = tk.Label(root, text=f"x1: {x1}")
    x1_label.pack()
    y1_label = tk.Label(root, text=f"y1: {y1}")
    y1_label.pack()
    
    # hide choose image button
    open_button.pack_forget()
    description.pack_forget()
    # create text
    text = f"Length: {length:.2f} cm\nDiameter: {diameter:.2f} cm"
    # add text to tkinter window
    label = tk.Label(root, text=text)
    label.pack()
    # add button to close program
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()
    
    # print("Length Points:", length_points)
    # print("Diameter Points:", diameter_points)
    # # length and diameter in cm
    # length = calculate_distance(length_points[0], length_points[1])
    # diameter = calculate_distance(diameter_points[0], diameter_points[1])
    # print("Length:", length)
    # print("Diameter:", diameter)

# Function to process the selected image
def process_image(image_path):
    global image, marked_image
    # Load the ultrasound image
    image = cv2.imread(image_path)

    # Create a copy of the image for marking points
    marked_image = image.copy()

    # Create a window for the image
    cv2.namedWindow('Marked Image')
    cv2.setMouseCallback('Marked Image', mark_point)

    # Display the initial image
    cv2.imshow('Marked Image', marked_image)

    cv2.waitKey(0)
    reset_globals()
    cv2.destroyAllWindows()
def open_image():
    file_path = filedialog.askopenfilename()
    print(file_path)
    if file_path:
        process_image(file_path)

def reset_globals():
    global image, marked_image, length_points, diameter_points
    image = None
    length_points = []
    diameter_points = []

# Create a Tkinter window
root = tk.Tk()
root.title("Image Measurement Tool")
# windoww settings
root.geometry("300x300")
root.eval('tk::PlaceWindow . center')

# add program description
description = tk.Label(root, text="This program allows you to measure distances \n in an image in physical units.")
description.pack()

# Add a button to open the file dialog
open_button = tk.Button(root, text="Choose Image", command=open_image)
open_button.pack()

root.mainloop()