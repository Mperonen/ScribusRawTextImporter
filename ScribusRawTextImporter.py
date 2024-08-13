import sys
try:
    import scribus
except ImportError:
    print("Unable to import the Scribus module.")
    sys.exit(1)

def alert_dialog(title, message):
    scribus.messageBox(title, str(message), icon=scribus.ICON_NONE, button1=scribus.BUTTON_OK|scribus.BUTTON_DEFAULT)


def create_page(page_number):
    try:
        scribus.gotoPage(page_number)
    except scribus.IndexError:
        scribus.newPage(-1)



def create_text_frame(target_layer, prev_text_frame = False, text_data = ""):
    page_size = scribus.getPageSize()
    page_margins = scribus.getPageMargins()

    text_frame_width = page_size[0] - (page_margins[0] + page_margins[2])
    text_frame_height = page_size[1] - (page_margins[1] + page_margins[3])

    new_text_frame = scribus.createText(page_margins[0], page_margins[1], text_frame_width, text_frame_height, target_layer)
    if prev_text_frame:
        scribus.linkTextFrames(prev_text_frame, new_text_frame)
    else:
        scribus.setText(text_data, new_text_frame)

    return new_text_frame








# STEP 0: open a new document dialog if none is open.
try:
    document_info = scribus.getInfo()
except scribus.NoDocOpenError:
    document_info = scribus.newDocDialog()

if document_info == 0:
    alert_dialog("No document created", "Document creation was cancelled. Script terminated.")
    sys.exit(1)


# STEP 1: fetch/create a layer for imported text content.
layer_name = "ImportedText"
try:
    # For some reason running scribus.setActiveLayer(layer_name) at this point crashes Sribus, so I use the function below to check if the layer exists.
    scribus.isLayerPrintable(layer_name)
except scribus.NotFoundError:
    scribus.createLayer(layer_name)
scribus.setActiveLayer(layer_name)


# STEP 2: select text file to be imported and import it.
imported_text = ""
with open(scribus.fileDialog("Import raw text", "txt files (*.txt)"), "r", encoding='utf-8') as handle:
    imported_text = handle.read()


current_page_number = 1
scribus.gotoPage(current_page_number)

# STEP 3: create the first text frame and set the imported text on to it.
previous_text_frame = create_text_frame(layer_name, False, imported_text)

# STEP 4: Iterate. As long as the text frame linking is overflowing, create a new page and add a new linked textrame
while scribus.textOverflows(previous_text_frame) == 1:
    current_page_number += 1
    scribus.newPage(-1)
    scribus.gotoPage(current_page_number)
    previous_text_frame = create_text_frame(layer_name, previous_text_frame, "")