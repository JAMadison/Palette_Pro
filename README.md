## Palette Pro
This program offers a variety of powerful tools for creating and exploring color palettes. With just a few clicks, you can generate randomized color combinations and save them as beautifully crafted 320x60 PNG grids. In addition, you can extract color palettes from any image using two different methods: the Kmeans algorithm and Colorgram.

The Kmeans algorithm method clusters the pixels in the image into a specified number of groups to generate a color palette, while Colorgram extracts the dominant colors directly from the image. This gives you two powerful methods for generating color palettes based on existing images. Whether you're a designer, artist, or just looking to experiment with color, this program offers everything you need to create stunning and unique color schemes.

## Already have a copy of Palet Pro?

Pull the latest changes from your remote repository using the git pull command. Navigate to your Palette Pro directory and open a CMD window, copy and paste the command below and you are good to go! 

	git pull


## 

## Palette Pro v3.0.0 Release and Install instructions:

Review the code here - https://github.com/JAMadison/Palette_Pro/blob/main/main.py

1. Requires python 3.10+ and Git

Open a command prompt or terminal window.

Change the working directory to where you want to clone your repository. You can do this by running the cd command followed by the path to the directory. For example:

	cd C:\Users\YourUsername\Documents

Clone your repository using the git clone command followed by the URL of your repository. For example:

	git clone https://github.com/JAMadison/Palette_Pro.git

Change the working directory to the root directory of your cloned repository. For example:

	cd YourRepository

Pull the latest changes from your remote repository using the git pull command. For example:

	git pull

Run the run.bat file by typing the following command in the terminal or simply double clicking it:

    run.bat

The first time this is ran it will execute the commands in the run.bat file, which will create a virtual environment, install the required dependencies, and start Palette Pro. After the first time, this will also be how you start Palette Pro.

And that's it! Just follow these steps and Palette Pro should run smoothly on your machine.

## UI Features

* In the updated UI, chose your palette extraction method or generate random palettes.

![alt text](README/UI_v3.png "New GUI")

## Natural Extraction
* Select any image file, and click "Open".
![alt text](README/ne_palette_1.png "Chose your pallet size with Natural Extraction")![alt text](README/ne_palette_2.png "Chose your pallet size with Natural Extraction")

![alt text](README/size.png "Chose your pallet size with Natural Extraction")

* Save your file with various image formats.

* If palette size is left blank or too large of a number was requested, it will default to all the colors avaible to this method. *

## Algorithmic Extraction
![alt text](README/example_1_Color_Palette.png "Example Palette 1")![alt text](README/example_2_Color_Palette.png "Example Palette 2")![alt text](README/example_3_Color_Palette.png "Example Palette 2")

* Select any image file, and click "Open". * Depending on the available threads on your PC, this could take a bit. *

![alt text](README/selection.png "image selection")

* A new window will open with your extracted color palette! Here you can save the palette or view individual color tones listed in the bottom right.

![alt text](README/example_extraction.png "Plotted Colors")

This selected the 42 most used colors, determined algorithmically with a slight variation added, meaning, each time it's used on a single image will generate slightly different results.


## Select Color
By selecting the first color you set the tone for the rest of the 15 colors and their varients.

*There is random logic to all the colors, if you select the same color twice you will get a different color palette.*

![alt text](README/Choose_Starting_Color.png "Select a color to start the palette off of")

![alt text](README/Choose_Starting_Color_Palette.png "Example of selected color palette")

## Example Random Color Palettes
![alt text](README/color_palette.png "Example Palette 1")

![alt text](README/color_palette_2.png "Example Palette 2")

![alt text](README/color_palette_3.png "Example Palette 3")

## Update Notes

* v3.0.0
  * Added Colorgram extraction method
    * Extracts the dominant colors directly from the image

* v2.0.1
* Random palettes now save to palette/ folder
  * Added console print out of saved image name

* v2.0.0
  * Added Kmeans algorithm method
    * Clusters the pixels in the image into a specified number of groups to generate a color palette



## Photoshop users: 

1. Open Adobe Photoshop and create a new document or open an existing one.

2. Click on the "Swatches" panel to open it (if it's not already open, go to "Window" > "Swatches").

3. In the Swatches panel, click on the drop-down menu icon (the icon with three horizontal lines) in the top right corner and select "Load Swatches".

4. In the file dialog, navigate to the folder where your color_palette.png file is located and select it.

5. If the color_palette.png file is not in indexed color mode, you can convert it by going to "Image" > "Mode" > "Indexed Color" and selecting the "Exact" 
option in the "Palette" dropdown. Then save the file as a PNG.

6. The color swatches from your color_palette.png file will be loaded into the Swatches panel.

7. To use a color from the palette, simply click on the desired swatch in the Swatches panel. The color will be applied to your currently selected tool or 
layer.

8. You can also save the loaded color palette as a new swatch library by clicking on the Swatches panel drop-down menu icon and selecting "Save Swatches". Give your new swatch library a name and save it to your desired location.
