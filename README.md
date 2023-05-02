## Palette Pro
This program allows you to create stunning 16-color paint palettes with matching light and dark variants for each color. 

With just a few clicks, you can generate randomized color combinations and save them as beautifully crafted 320x60 PNG grids. It's the perfect tool for designers, artists, and anyone who loves to experiment with colors.

## Palette Pro v2.0 Release and Install instructions:
Review the code here - https://github.com/JAMadison/Palette_Pro/blob/main/main.py

1. Requires python 3.10+ and Git

Open a command prompt or terminal window.

Change the working directory to where you want to clone your repository. You can do this by running the cd command followed by the path to the directory. For example:

	cd C:\Users\YourUsername\Documents

Clone your repository using the git clone command followed by the URL of your repository. For example:

	git clone https://github.com/JAMadison/Palette_Pro.git

Change the working directory to the root directory of your cloned repository. For example:

	cd <i>YourRepository</i>

Pull the latest changes from your remote repository using the git pull command. For example:

	git pull

Run the run.bat file by typing the following command in the terminal or simply double clicking it:

    run.bat

The first time this is ran it will execute the commands in the run.bat file, which will create a virtual environment, install the required dependencies, and start Palette Pro. After the first time, this will also be how you start Palette Pro.

And that's it! Just follow these steps and Palette Pro should run smoothly on your machine.


## New to v2
*Now you can select an image and extract a color palette from that image*

1. Click "Select Image".

![alt text](README/Palette_Pro_v2.png "New GUI")

2. Select any image file, and click "Open". *Depending on the available threads on your PC, this could take a bit.*

![alt text](README/selection.png "image selection")

3. A new window will open with your extracted color palette! Here you can save the palette or view individual color tones listed in the bottom right.

![alt text](README/example_extraction.png "Plotted Colors")

This selected the 42 most used colors, determined algorithmically with a slight variation added, meaning, each time it's used on a single image will generate slightly different results.

![alt text](README/example_1_Color_Palette.png "Example Palette 1")![alt text](README/example_2_Color_Palette.png "Example Palette 2")![alt text](README/example_3_Color_Palette.png "Example Palette 2")


## Select Color
By selecting the first color you set the tone for the rest of the 15 colors and their varients.

*There is random logic to all the colors, if you select the same color twice you will get a different color palette.*

![alt text](README/Choose_Starting_Color.png "Select a color to start the palette off of")

![alt text](README/Choose_Starting_Color_Palette.png "Example of selected color palette")

## Example Random Color Palettes
![alt text](README/color_palette.png "Example Palette 1")

![alt text](README/color_palette_2.png "Example Palette 2")

![alt text](README/color_palette_3.png "Example Palette 3")

## Palette From Image


## New to v2
*Now you can select an image and extract a color palette from that image*
1. Click "Select Image".
2. Select any image file, and click "Open". *Depending on the available threads on your PC, this could take a bit.*
3. A new window will open with your extracted color palette!

This uses an agorithm to select the colors, so each time its ran will generate slightly different results.
