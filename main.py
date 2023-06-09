import tkinter as tk
import tkinter.colorchooser as colorchooser
from PIL import Image, ImageDraw
from random import randint, uniform, sample
import colorsys
from math import sqrt
import cv2
import numpy as np
from scipy import spatial
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from tkinter import filedialog
import concurrent.futures
import os
import colorgram

# Set the dark theme colors
bg_color = "#282828"
fg_color = "#ffffff"
button_color = "#4a4a4a"
accent_color = "#f05454"


def resize_image(image_path):
    img = cv2.imread(image_path)

    # Get the original image dimensions
    height, width, _ = img.shape

    # Calculate the new dimensions while maintaining the aspect ratio
    if height > width:
        new_height = 750
        new_width = int(width * (new_height / height))
    else:
        new_width = 750
        new_height = int(height * (new_width / width))

    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_img


def get_color_palette():
    # Open file dialog to select image
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename()
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Resize the image
        img = resize_image(file_path)
        # Convert to RGB color space
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get number of available threads
        num_threads = os.cpu_count()

        # Divide image up into slices
        slice_size = len(img) // num_threads
        slices = [(i*slice_size, (i+1)*slice_size) for i in range(num_threads)]
        slices[-1] = (slices[-1][0], len(img))

        # Process each slice in parallel
        sorted_colors = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for start, end in slices:
                futures.append(executor.submit(process_slice, img, start, end))
            for future in concurrent.futures.as_completed(futures):
                sorted_colors.extend(future.result())

        # Display the color palette
        palette = np.zeros((105, 90, 3), dtype=np.uint8)  # 15 * 7, 15 * 6
        start = 0
        for i in range(7):
            for j in range(6):
                color = sorted_colors[start]
                palette[i * 15:(i + 1) * 15, j * 15:(j + 1) * 15] = color
                start += 1
        # height in inches, width in inches, DPI
        fig, ax = plt.subplots(num=f'{file_name} Color Palette', figsize=(3.34, 3.84), dpi=100)
        ax.imshow(palette, interpolation='nearest', extent=[0, 90, 0, 105])
        fig.patch.set_facecolor('black')
        root.title('Extracted Color Palette') # Set the window title
        ax.axis('off')
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        plt.show()

        # Properly close the ThreadPoolExecutor
        executor.shutdown(wait=False)
    except AttributeError:
        print("File not opened.")


def sort_colors_by_similarity(colors):
    # Calculate the similarity matrix
    similarity_matrix = np.zeros((len(colors), len(colors)))
    for i in range(len(colors)):
        for j in range(i, len(colors)):
            similarity = 1 - spatial.distance.cosine(colors[i], colors[j])
            similarity_matrix[i][j] = similarity
            similarity_matrix[j][i] = similarity

    # Sort the colors by similarity
    sorted_indices = []
    remaining_indices = set(range(len(colors)))
    while remaining_indices:
        index = remaining_indices.pop()
        sorted_indices.append(index)
        similarities = similarity_matrix[index]
        for i in np.argsort(similarities)[::-1]:
            if i in remaining_indices:
                remaining_indices.remove(i)
                sorted_indices.append(i)

    return [colors[i] for i in sorted_indices]


def process_slice(img, start_row, end_row):
    # Flatten slice of image to a 2D array
    img_slice = img[start_row:end_row, :]
    img_flattened = np.reshape(img_slice, (-1, 3))

    # Apply KMeans clustering to cluster colors
    kmeans = KMeans(n_clusters=6, n_init=10)
    kmeans.fit(img_flattened)

    # Get the labels for each pixel
    labels = kmeans.labels_

    # Get the frequency of each label
    label_counts = np.bincount(labels)

    # Get the indices of the most frequent labels
    most_frequent_label_indices = np.argsort(label_counts)[::-1][:7]

    # Get the most frequent colors
    most_frequent_colors = kmeans.cluster_centers_[most_frequent_label_indices]

    # Sort the most frequent colors based on their luminance value
    luminance_values = np.sqrt(np.sum(most_frequent_colors**2, axis=1))
    sorted_indices = np.argsort(luminance_values)
    sorted_colors = most_frequent_colors[sorted_indices]

    return sorted_colors


def color_distance(c1, c2):
    rmean = (c1[0] + c2[0]) / 2
    r = c1[0] - c2[0]
    g = c1[1] - c2[1]
    b = c1[2] - c2[2]
    return int(sqrt((((512+rmean)*r*r)//256) + 4*g*g + (((767-rmean)*b*b)//256)))


def generate_palette(start_color=None):
    if not start_color:
        start_color = (randint(0, 255), randint(0, 255), randint(0, 255))

    # Create a list of 16 colors based on the starting color
    palette = [start_color]
    for i in range(1, 16):
        hue = (i / 16.0) * 360
        saturation = uniform(0.0001, 1.0)
        lightness = uniform(0.1, 0.55)
        new_color = tuple(int(c * 255) for c in colorsys.hls_to_rgb(hue / 360.0, lightness, saturation))
        palette.append(new_color)

    # Sort the palette based on the distance from each color to the start color
    palette.sort(key=lambda c: color_distance(c, start_color))

    # Generate a darker version of each color in the palette
    dark_palette = []
    for color in palette:
        h, l, s = colorsys.rgb_to_hls(*color)
        l = max(1, l - 0.10)  # reduce lightness by 0.2
        rgb = colorsys.hls_to_rgb(h, l, s)
        dark_color = tuple(min(255, max(0, int(c * uniform(0.45, 0.65)))) for c in rgb)
        dark_palette.append(dark_color)

    # Generate a lighter version of each color in the palette
    light_palette = []
    for color in palette:
        h, l, s = colorsys.rgb_to_hls(*color)
        l = max(1, l + 32)
        rgb = colorsys.hls_to_rgb(h, l, s)
        light_color = tuple(min(255, max(0, int(c * uniform(1.15, 1.35)))) for c in rgb)
        light_palette.append(light_color)

    # Calculate the height of each color band
    # Display the main colors
    for i, color in enumerate(palette):
        x0 = i * 20 + 3
        y0 = 23
        x1 = x0 + 18
        y1 = y0 + 18
        canvas.create_rectangle(x0, y0, x1, y1, fill="#{:02x}{:02x}{:02x}".format(*color))

    # Display the dark colors
    for i, color in enumerate(palette):
        x0 = i * 20 + 3
        y0 = 43
        x1 = x0 + 18
        y1 = y0 + 18
        dark_color = dark_palette[i]
        canvas.create_rectangle(x0, y0, x1, y1, fill="#{:02x}{:02x}{:02x}".format(*dark_color))

    # Display the light colors
    for i, color in enumerate(light_palette):
        x0 = i * 20 + 3
        y0 = 3
        x1 = x0 + 18
        y1 = y0 + 18
        light_color = light_palette[i]
        canvas.create_rectangle(x0, y0, x1, y1, fill="#{:02x}{:02x}{:02x}".format(*light_color))

    # Update the global palette variables
    global current_palette
    current_palette = palette

    global current_dark_palette
    current_dark_palette = dark_palette

    global current_light_palette
    current_light_palette = light_palette


def choose_starting_color():
    global start_color
    color = tk.colorchooser.askcolor(title="Choose Starting Color")
    if color is not None:
        start_color = tuple(int(c) for c in color[0])
        generate_palette(start_color)
    else:
        start_color = None


def save_palette():
    # Create a new image
    img = Image.new("RGBA", (20*16, 60), "white")
    draw = ImageDraw.Draw(img)

    # Draw the light colors on the image
    for i, color in enumerate(current_light_palette):
        x0 = i * 20
        x1 = (i + 1) * 20 - 1
        draw.rectangle([x0, 0, x1, 19], fill=color, outline="black")

    # Draw the color palette on the image
    for i, color in enumerate(current_palette):
        x0 = i * 20
        x1 = (i + 1) * 20 - 1
        draw.rectangle([x0, 20, x1, 39], fill=color, outline="black")

    # Draw the dark colors on the image
    for i, color in enumerate(current_dark_palette):
        x0 = i * 20
        x1 = (i + 1) * 20 - 1
        draw.rectangle([x0, 40, x1, 59], fill=color, outline="black")

    # Create the "palettes" directory if it doesn't exist
    if not os.path.exists("palettes"):
        os.mkdir("palettes")

    # Save the image as a PNG file in the "palettes" directory
    count = 1
    while True:
        filename = f"palettes/color_palette{'_' + str(count) if count > 1 else ''}.png"
        if os.path.exists(filename):
            count += 1
        else:
            img.save(filename)
            print(f"Saved {filename}")
            break


def sort_by_brightness_and_hue(hex_color):
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return (v, h)


def define_palette():
    def save_defined_palette():
        try:
            # Create a white image with the size of the canvas
            image = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
            draw = ImageDraw.Draw(image)

            # Draw each tile on the image
            min_x, min_y, max_x, max_y = canvas_width, canvas_height, 0, 0
            canvas_items = canvas.find_all()
            for item in canvas_items:
                x1, y1, x2, y2 = canvas.coords(item)
                color = canvas.itemcget(item, 'fill')

                # Draw the colored rectangle with a black border
                draw.rectangle((x1 - 2, y1 - 2, x2 + 2, y2 + 2), fill=color, outline=(0, 0, 0))

                min_x = min(min_x, x1)
                min_y = min(min_y, y1)
                max_x = max(max_x, x2)
                max_y = max(max_y, y2)

            # Crop the image to the bounding box of the tiles
            image = image.crop((min_x, min_y, max_x, max_y))

            # Ask the user for the save file path
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG Files", "*.png"),
                                                                ("JPEG Files", "*.jpg"),
                                                                ("Bitmap", ".bmp")])
            if file_path:
                # Save the cropped image to the file path
                image.save(file_path)
            else:
                print("Save Canceled")
        except ValueError as e:
            print("Save Canceled")
    try:
        # Open file dialog to select image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg .jpeg .png .bmp")])

        # Load image using Pillow library
        image = Image.open(file_path)

        color_test = colorgram.extract(image, -1)

        # Extract colors from image using colorgram library
        if not natural_extraction_entry.get() or not natural_extraction_entry.get().isdigit():
            num_colors = len(color_test)
            print(f"Full color palette in image is {len(color_test)} colors.")
        elif len(color_test) < int(natural_extraction_entry.get()):
            num_colors = len(color_test)
            print(f"User entered more colors than are present in image."
                  f"\nFull color palette in image is {len(color_test)} colors.")
        else:
            num_colors = int(natural_extraction_entry.get())  # Get number of colors from user input

        # Convert RGB color values to hex format

        hex_colors = []

        for color in color_test:
            r, g, b = color.rgb
            hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            hex_colors.append(hex_color)

        if natural_extraction_entry.get() != "" and int(natural_extraction_entry.get()) < len(color_test):
            hex_colors = sample(hex_colors, int(natural_extraction_entry.get()))

        hex_colors.sort(key=sort_by_brightness_and_hue)

        # Calculate grid size based on number of colors
        num_cols = 16
        num_rows = (num_colors + num_cols - 1) // num_cols

        # Create new window for color palette grid
        palette_window = tk.Toplevel(root)
        palette_window.title("Color Palette")

        # Set the dark theme colors
        bg_color = "#282828"
        fg_color = "#ffffff"
        button_color = "#4a4a4a"
        accent_color = "#f05454"

        palette_window.configure(bg=bg_color)

        # Create canvas for color palette grid
        box_size = 20  # Size of each color box
        canvas_width = num_cols * box_size
        canvas_height = num_rows * box_size
        canvas = tk.Canvas(palette_window, width=canvas_width, height=canvas_height, bg=bg_color, highlightthickness=0)
        canvas.pack()

        # Draw color palette grid
        for i in range(num_rows):
            for j in range(num_cols):
                index = i * num_cols + j
                if len(hex_colors) < num_colors:
                    print("Not enough colors in palette")
                    return

                if index < num_colors:
                    color_box = canvas.create_rectangle(j * box_size, i * box_size,
                                                        (j + 1) * box_size, (i + 1) * box_size,
                                                        fill=hex_colors[index], width=2, outline="black")

        # Resize window to fit color palette
        palette_window.geometry('{}x{}'.format(canvas_width, canvas_height + 50))

        # Add Save Palette button
        save_button = tk.Button(palette_window, text="Save Palette", command=save_defined_palette, bg=button_color,
                                 fg=fg_color, relief="flat", activebackground=accent_color, activeforeground=fg_color,
                                 bd=0, padx=20, pady=10, highlightthickness=0)
        save_button.pack()

    except (FileNotFoundError, AttributeError) as e:
        print("File not found or not a valid image file.")


if __name__ == '__main__':
    # Create a Tkinter window and canvas
    root = tk.Tk()
    root.title("Palette Pro v3.5.1")

    # Set the dark theme colors
    bg_color = "#282828"
    fg_color = "#ffffff"
    button_color = "#4a4a4a"
    accent_color = "#f05454"

    root.configure(bg=bg_color)

    bundle_dir = os.path.abspath(os.path.dirname(__file__))

    # Set the window icon
    icon_path = os.path.join(bundle_dir, 'images', 'icon.png')
    root.iconphoto(True, tk.PhotoImage(file=icon_path))

    root.resizable(False, False)

    canvas = tk.Canvas(root, width=16 * 20 + 3, height=70, bg=bg_color, bd=0, highlightthickness=0)
    canvas.pack(pady=10)

    # Generate the initial color palette
    generate_palette()

    # Create a new frame for the buttons
    button_frame = tk.Frame(root, bg=bg_color)
    button_frame.pack()

    # Create a "Generate New Palette" button to create a new color palette
    generate_button = tk.Button(button_frame, text="Random Palette", command=generate_palette, bg=button_color,
                                fg=fg_color, relief="flat", activebackground=accent_color, activeforeground=fg_color,
                                bd=0, padx=20, pady=10, highlightthickness=0)
    generate_button.pack(side="left", padx=5)

    choose_button = tk.Button(button_frame, text="Choose Color", command=choose_starting_color, bg=button_color,
                              fg=fg_color, relief="flat", activebackground=accent_color, activeforeground=fg_color,
                              bd=0, padx=20, pady=10, highlightthickness=0)
    choose_button.pack(side="left", padx=5)

    # Create a "Save" button to save the color palette as a PNG file
    save_button = tk.Button(button_frame, text="Save Random Palette", command=save_palette, bg=button_color,
                            fg=fg_color, relief="flat", activebackground=accent_color, activeforeground=fg_color, bd=0,
                            padx=20, pady=10, highlightthickness=0)
    save_button.pack(side="left", padx=5)

    # Create a frame and button to select an image
    frame_e = tk.Frame(root, bg=bg_color, bd=0)
    frame_e.pack(padx=10, pady=10)

    algorithm_button = tk.Button(frame_e, text="Algorithmic Extraction", command=get_color_palette, bg=button_color,
                                 fg=fg_color, relief="flat", activebackground=accent_color, activeforeground=fg_color,
                                 bd=0, padx=20, pady=10, highlightthickness=0)
    algorithm_button.pack()

    frame_ne = tk.Frame(root, bg=bg_color, bd=0)
    frame_ne.pack(padx=10, pady=10)

    natural_extraction_label = tk.Label(frame_ne, text="Enter desired palette size:", bg=bg_color, fg=fg_color)
    natural_extraction_label.grid(row=1, column=0, padx=5)

    natural_extraction_entry = tk.Entry(frame_ne, bg=button_color, fg=fg_color, insertbackground=fg_color)
    natural_extraction_entry.grid(row=1, column=1, pady=10, padx=5)

    natural_extraction_button = tk.Button(frame_ne, text="Natural Extraction", command=define_palette, bg=button_color,
                                          fg=fg_color, relief="flat", activebackground=accent_color,
                                          activeforeground=fg_color, bd=0, padx=20, pady=10, highlightthickness=0)
    natural_extraction_button.grid(row=1, column=2, pady=10, padx=5)

    # Run the Tkinter event loop
    root.mainloop()
