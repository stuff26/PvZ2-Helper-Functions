NOTE: This is an OLD version of Helper Functions, this is archived and will no longer be maintained. Please view the [2.0 release of Helper Functions](https://github.com/stuff26/PvZ2-Helper-Functions-2.0) for the current version.

# PvZ2-Helper-Functions
Convenient functions meant for modding Plants vs Zombies 2. These functions are made by stuff26 and are mainly made for usage with Sen 4.0. All of this is coded in python. Below will explain each current function.

### Redo XFL data.json
The function will take in the data.json of an xfl and a list of media that is part of an xfl. From there it will ask for an ID prefix to use for the sprite IDs. After that, it will rewrite the entire image section of the data.json and overwrite it.

### Redo OBB data.json
The function will take in a data.json from an obb and a packet folder then overwrite the data.json with all the SCGs found in the packet folder.

### Convert Sen 3.0 Resource Group to 4.0 SCG
The function will take in the necessary split resource files and any other necessary files to convert the files from a Sen 3.0 resource group and then compile it into an SCG compatible with Sen 4.0. Ensure you pack with regular and not modding when you pack the SCG.

### Update All Coordinates in Worldmap JSON
The function will take in a world map file and ask how much to increase/decrease the x and y coordinates of every single map piece. From there it will spit out a new worldmap file with the edits.

### Organize Plant Files
The function will take in a packages folder and organize plant types, props, levels, and almanac data based on what is in property sheets

### Make Zombie and GI Templates
The function will turn a template base file and make several copies of the templates inside, perfect for people wanting to add templates for level makers. The function can also spit out a templates base file so you know how to edit it.

### Level Error Checker
The function will take in a level and the packages folder of an obb. From there it will cross check each part of a level to find any missing modules or other potential errors in a level and spit out a message of what is found.

### Check For Errors
The function checks for a few potential errors that can cause issues with XFLs that prevent them from packing or can cause them to glitch out. Some errors scanned for include:
- If any layers have more than one type of symbol
- If there are any tweens
- If there are frames with more than one sprite attached
- If there are any layers with keyframes with gaps of empty keyframes between ones with symbols attached
- If there are any bitmaps in sprite/label/main symbols or other symbols in image symbols

### Split Multi Sprite Layers
The function splits layers that use multiple different symbols, which can prevent XFLs from packing

### Rename Layers
The function renames layers either by number (ascending or descending) or by the symbol they use, useful for those who prefer to be more organized

### PP.DAT Cleaner
The function takes in a PP.DAT JSON file and then changes some of the keys to be more easily readable. This doesn't change all of the keys due to me not knowing what they do. The function will also convert the cleaner version back to a game readable one, ensure you do this before converting it back to a PP.DAT

### Offset Sprite Positions
The function takes in an XFL or individual symbol file then will change all of the sprite positions in the symbol(s) by a certain amount in the x and y direction. This is mainly for animations that don't have any sort of built in offseter in game).


## Conclusion
Feel free to reach out to stuff26 on discord if you have suggestions or issues. Some currently planned functions that will be added include:

- Redo SCG data.json (may or may not be possible though)
- Add labels to DOMDocument automatically
- Find objects found in save files
- Consistent image/bitmap namer
- Snowie Lib action frame maker (?)
