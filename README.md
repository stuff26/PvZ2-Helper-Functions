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


## Conclusion
Feel free to reach out to stuff26 on discord if you have suggestions or issues. Some currently planned functions that will be added include:
- Zombie file organizer
- Redo SCG data.json (may or may not be possible though)
