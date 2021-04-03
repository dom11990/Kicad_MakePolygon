# Kicad_MakePolygon

This is an action plugin for KiCad 5.x. It allows the user to convert an selection of arcs to individual line segments at configurable discretization lengths. Additionally an enclosed selection of line segments (drawings, not tracks!) can be converted to a filled polygon. The target use case of the plugin is to take RF structures exported from simulation programs such as CST as DXF files and quickly get them onto a board. In the future, export as a footprint will also be supported.

# Dependencies
 - Python3
 - Loguru (pip install loguru)
 - PyQt5 (pip install PyQt5
 - Qt5 (varies from distro to distro, for Arch sudo pacman -S qt5-base)

# How to Use
1. Select the structures you want to discretize or polygonize
2. Start the action script from the "Tools -> External Plugins... -> Polygonize" menu
3. Select your configuration: line width, result layer, if the selected items should be deleted afer generating the new objects
4. Click Polygonize or Discretize, depending on your needs

Note: Polygonize does several checks and structure changes to make life easier, such as allowing two enclosed structures that share endpoints to be considered one. This is particularly common in RF design exports. This may take some time. Even on a decent consumer computer, it can take several seconds to generate the polygon- just be patient. I may optimize this in the future.
