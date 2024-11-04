# Development ideas

## How to add a new logo

The thermal printer can only print a BMP.  There's likely a more efficient way to convert an SVG to a consumable icon; however, this is my current process:

* Open Inkscape with SVG
* Export SVG to 75x75 pixel PNG
* Use ImageMagick to convert PNG to BMP
  * `convert azure-monochrome.png -resize 250x75 -gravity east -extent 250x75 azure-monochrome.bmp`

NOTE: I don't know how to convert SVG to BMP in one step without the graphic turning blurry

https://learn.adafruit.com/mini-thermal-receipt-printer/bitmap-printing

## Talking to printer via serial

https://github.com/adafruit/Python-Thermal-Printer/blob/678e13ae918deadf2b350b3f866a21de6ff1ad6d/README.md#getting-started

## Generate offline responses

```
. ./venv/bin/activate
# Update helpers/generate_offline_responses.py with the menu option to generate
python helpers/generate_offline_responses.py
```