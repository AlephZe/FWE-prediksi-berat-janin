import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from formula import calculate_integrate_volume, calculate_distance, calculate_head_volume

# init tkinter
root = tk.Tk()
# Variables to store clicked points
bottom_feet_coordinates = []
upper_feet_coordinates = []
hand_coordinates = []
body_coordinates = []
head_diameter = []
status_text = 'Click on the four points of the bottom feet'
image = None

# Function to draw lines and distance text between points
def draw_lines_and_distances(image, points, color=(0, 255, 0)):
    for i in range(1, len(points)):
        cv2.line(image, points[i - 1], points[i], color, 2)
        distance = calculate_distance(points[i - 1], points[i])
        text_position = (
            int((points[i - 1][0] + points[i][0]) / 2),
            int((points[i - 1][1] + points[i][1]) / 2)
        )
        # cv2.putText(image, f'{distance:.2f} cm', text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# Function to handle mouse clicks
def mark_point(event, x, y, flags, param):
    global bottom_feet_coordinates, upper_feet_coordinates, body_coordinates, head_diameter, marked_image, hand_coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(bottom_feet_coordinates) < 4:
            bottom_feet_coordinates.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 3, (0, 0, 255), -1)

            if len(bottom_feet_coordinates) == 4:
                draw_lines_and_distances(marked_image, bottom_feet_coordinates)
                draw_lines_and_distances(marked_image, [bottom_feet_coordinates[0], bottom_feet_coordinates[3]])
                draw_instruction(marked_image, "draw upper feet points")
        elif len(upper_feet_coordinates) < 4:
            upper_feet_coordinates.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 3, (0, 0, 255), -1)

            if len(upper_feet_coordinates) == 4:
                draw_lines_and_distances(marked_image, upper_feet_coordinates)
                draw_lines_and_distances(marked_image, [upper_feet_coordinates[0], upper_feet_coordinates[3]])
                draw_instruction(marked_image, "draw hands points")
        elif len(hand_coordinates) < 4:
            hand_coordinates.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 3, (0, 0, 255), -1)

            if len(hand_coordinates) == 4:
                draw_lines_and_distances(marked_image, hand_coordinates)
                draw_lines_and_distances(marked_image, [hand_coordinates[0], hand_coordinates[3]])
                draw_instruction(marked_image, "draw body points")

        elif len(body_coordinates) < 4:
            body_coordinates.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 3, (0, 0, 255), -1)
            # If both points are obtained for diameter, draw lines and distances
            if len(body_coordinates) == 4:
                draw_lines_and_distances(marked_image, body_coordinates, (0, 255, 255))
                draw_lines_and_distances(marked_image, [body_coordinates[0], body_coordinates[3]], (0, 255, 255))
                draw_instruction(marked_image, "draw head diameter")

        elif len(head_diameter) < 2:
            head_diameter.append((x, y))
            # Draw a dot at the clicked point
            cv2.circle(marked_image, (x, y), 3, (255, 0, 255), -1)
            # If both points are obtained for diameter, draw lines and distances
            if len(head_diameter) == 2:
                draw_lines_and_distances(marked_image, head_diameter)

        # If both sets of points are obtained, proceed to the next screen
        if len(bottom_feet_coordinates) == 4 and len(upper_feet_coordinates) == 4 and len(body_coordinates) == 4 and len(hand_coordinates) == 4 and len(head_diameter) == 2:
            cv2.destroyAllWindows()
            next_screen()  # You can define the next screen function here

        # Display the marked image
        cv2.imshow('Marked Image', marked_image)

# function to draw white instruction and a black rect
def draw_instruction(image, text):
    # create a black rectangle
    cv2.rectangle(image, (0, 0), (200, 50), (0, 0, 0), -1)
    # create text
    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return image

# Function to proceed to the next screen
def next_screen():
    # close opencv window
    cv2.destroyAllWindows()
    # change tkinter window
    root.geometry("300x300")
    # calculate length and diameter
    
    #vottom feet
    feet_x2 = calculate_distance(bottom_feet_coordinates[0], bottom_feet_coordinates[1])
    feet_y1 = calculate_distance(bottom_feet_coordinates[0], bottom_feet_coordinates[3]) 
    feet_y2 = calculate_distance(bottom_feet_coordinates[1], bottom_feet_coordinates[2]) 

    # print button feet coordinates
    print("x2 bottom feet", feet_x2)
    print("y1 bottom feet", feet_y1)
    print("y2 bottom feet", feet_y2)
    
    # upper feet
    upper_feet_x2 = calculate_distance(upper_feet_coordinates[0], upper_feet_coordinates[1])
    upper_feet_y1 = calculate_distance(upper_feet_coordinates[0], upper_feet_coordinates[3])
    upper_feet_y2 = calculate_distance(upper_feet_coordinates[1], upper_feet_coordinates[2])

    # print upper feet coordinates
    print("x2 upper feet", upper_feet_x2)
    print("y1 upper feet", upper_feet_y1)
    print("y2 upper feet", upper_feet_y2)
    
    #hand 
    hand_x2 = calculate_distance(hand_coordinates[0], hand_coordinates[1])
    hand_y1 = calculate_distance(hand_coordinates[0], hand_coordinates[3])
    hand_y2 = calculate_distance(hand_coordinates[1], hand_coordinates[2])

    # print hand coordinates
    print("x2 hand", hand_x2)
    print("y1 hand", hand_y1)
    print("y2 hand", hand_y2)
    
    # body
    body_x2 = calculate_distance(body_coordinates[0], body_coordinates[1])
    body_y1 = calculate_distance(body_coordinates[0], body_coordinates[3])
    body_y2 = calculate_distance(body_coordinates[1], body_coordinates[2])
    head_diameter_cm = calculate_distance(head_diameter[0], head_diameter[1])

    # print body coordinates
    print("x2 body", body_x2)
    print("y1 body", body_y1)
    print("y2 body", body_y2)
    print("head diameter", head_diameter_cm)

    feet_volume = calculate_integrate_volume([0, feet_x2, feet_y1, feet_y2])

    upper_feet_volume = calculate_integrate_volume([0, upper_feet_x2, upper_feet_y1, upper_feet_y2])
    
    hand_volume = calculate_integrate_volume([0, hand_x2, hand_y1, hand_y2])

    body_volume = calculate_integrate_volume([0, body_x2, (body_y1), body_y2])

    # print each volume
    print("feet volume", feet_volume)
    print("upper feet volume", upper_feet_volume)
    print("hand volume", hand_volume)
    print("body volume", body_volume)
    

    head_volume = calculate_head_volume(head_diameter_cm)

    # print head volume
    print("head volume", head_volume)
    total = ((feet_volume + upper_feet_volume) * 2) + (hand_volume * 2) +  body_volume + head_volume

    # print total volume
    print("total volume", total)
    
    # hide choose image button
    open_button.pack_forget()
    description.pack_forget()
    # create text
    # show results estimated weight in kg, covert to to kg from g
    text = f"Estimated Weight: {total * 0.001:.2f} kg\nFeet Volume: {feet_volume * 0.001:.2f} kg\nBody Volume: {body_volume * 0.001:.2f} kg\nHead Volume: {head_volume * 0.001:.2f} kg\nHand Volume: {hand_volume * 0.001:.2f} kg"

    # add text to tkinter window
    label = tk.Label(root, text=text)
    label.pack()
    # add button to close program
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack()

# Function to process the selected image
def process_image(image_path):
    global image, marked_image
    # Load the ultrasound image
    image = cv2.imread(image_path)

    # Create a copy of the image for marking points
    marked_image = image.copy()
    draw_instruction(marked_image, "draw feet points")
    # Create a window for the image
    cv2.namedWindow('Marked Image')
    cv2.setMouseCallback('Marked Image', mark_point)

    # Get the image dimensions
    height, width, _ = marked_image.shape

    # Create a grid matrix image
    grid_image = np.zeros((height, width, 3), np.uint8)

    # Define the grid spacing (adjust as needed)
    grid_spacing = 50  # Adjust the spacing as needed

    # Draw grid lines and label coordinates
    for x in range(width // 2, width, grid_spacing):
        cv2.line(grid_image, (x, 0), (x, height), (255, 255, 255), 1)

    for x in range(width // 2, 0, -grid_spacing):
        cv2.line(grid_image, (x, 0), (x, height), (255, 255, 255), 1)

    for y in range(height // 2, height, grid_spacing):
        cv2.line(grid_image, (0, y), (width, y), (255, 255, 255), 1)

    for y in range(height // 2, 0, -grid_spacing):
        cv2.line(grid_image, (0, y), (width, y), (255, 255, 255), 1)

    # Combine the grid matrix image with the marked image
    marked_image = cv2.addWeighted(marked_image, 1, grid_image, 0.5, 0)

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
    global image, marked_image, bottom_feet_coordinates, body_coordinates, head_diameter, upper_feet_coordinates, hand_coordinates
    image = None
    bottom_feet_coordinates = []
    upper_feet_coordinates = []
    hand_coordinates = []
    body_coordinates = []
    head_diameter = []



if __name__ == '__main__':
    root.title("Image Measurement Tool")
    # windoww settings
    root.geometry("300x300")
    root.eval('tk::PlaceWindow . center')

    # add program description
    description = tk.Label(root, text="This program allows you to measure weight \n of a fetal in KG.")
    description.pack()

    # Add a button to open the file dialog
    open_button = tk.Button(root, text="Choose Image", command=open_image)
    open_button.pack()

    root.mainloop()