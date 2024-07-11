# **Hello! These are some fun tools built with the Arduino Mouse and Keyboard libraries.**

***Requirements:***
One ATmega32u4 or SAMD board connected to laptop, another connected to phone, communicate to each other via nRF24L01 modules.
Upload the appropriate .ino code and check that the port name matches at the top of .py program.

## ***General Fun:***

**track.py** - Basic program that relays touchpad moves, clicks, and scrolls as well as keyboard input to the phone
> USAGE: Start the python program, cursor will automatically move to the center of the screen on both phone and laptop. (Adjust screen dimensions if necessary)

**draw.py** - Use this first to save drawing files
> USAGE: Start the python program, hold down left click to draw in one stroke, lift to release and name the drawing file. Hold down again to start a new drawing. CTRL+D to exit the program.

**trashy_drawing_replicator.py** -> Use this to push saved drawings to be replicated on the phone
> USAGE: Start the python program, use arrow keys to adjust cursor on phone screen, press '/' then type the drawing file name and press ENTER to draw.

## ***GamePigeon assists:***

**wordhunt.py** - Automatically finds and inputs all Word Hunt answers
> USAGE: Open the Word Hunt game and start the Python program. If the starting cursor is not aligned in the top left box, enter 'm' to reposition until it looks good. Enter the 16 letters on the board with spaces to separate each row.

**anagrams.py** - Automatically finds and inputs all Anagrams answers (uses same word list as Word Hunt so may have extra words that aren't in Anagrams dictionary)
> USAGE: Open the Anagrams game and start the Python program. If the starting cursor is not aligned in the leftmost box, enter 'm' to reposition until it looks good. Enter the 6 letters on the board.

**darts.py** - Aim assistant for specific point values that can be scored
> USAGE: Open the Darts game and start the Python program. If the starting cursor is not aligned in the center of the moving dart, enter 'm' to reposition until it looks good. Write the intended point value you want to score and press ENTER when you see the tip of the moving dart just touch the bottom of the circular board.

## Enjoy and have fun!!

## Taliyah ^_^
