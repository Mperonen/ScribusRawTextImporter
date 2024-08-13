# ScribusRawTextImporter
This Python script allows you to import raw text file (txt) content into Scribus. It will automatically generate the needed pages and linked textframes.

The script aims to be well commented and pretty self-explanatory. You can run the script for active open document or if you run the script while no document is open, it will open the new document dialog for you.
1. After document creation the script will create a layer used by the script (or select if it already exists)
2. Then you will get a dialog to choose the raw text file (.txt) for importing.
3. After (hopefully succesful) import, the script will create the initial text frame on to the first page.
4. Then the script will loop and as long as last created text frame is overflowing, it will create a new page, a new textfame on to it and link it with the previous frame.
