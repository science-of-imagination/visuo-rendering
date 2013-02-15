Display objects from a LabelMe database.

If you don't have a dataset, run the main method from labelmeretriever.

To do the first time you use a dataset from LabelMe:
Run the main method from xmlindexer. The data folder should be in the same folder as the xmlindexer and display script.
It will create an index file inside the data folder, which will then be used to search for objects.

One way to use the script:

1. Open a command prompt inside the folder in which the script is placed.

2. Launch the Python interpreter within the command prompt and import the module display
 
3. Write "imagine('the_object_to_be_displayed', (x,y))" where x and y are values between 0 and 1.

4. A window will appear displaying the object. Close it with either the Escape key or the Close button to summon another object.

5. The objects are kept in memory. If you want to reset the screen, write "clear()"

To display from a file:
3. Write "display_from_file('filename')"
    where "filename" is the actual filename, with extension, of the text file.

To use the Oracle of Objects:
3. Write "proximity('the_object_to_be_displayed')"

GrabCut from OpenCV can be enabled in display.py parameters, to process the LabelMe outlines.

Science of Imagination Laboratory
