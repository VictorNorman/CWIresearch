# Geophysical Modeling Software for The Clean Water Institute
> When clean water is scarce, groundwater can be an excellent source, but drilling is expensive. Geophysical equipment, which relies on various types of signal modulation to model strata for the optimal siting of wells, can easily cost tens of thousands of dollars. This project seeks to develop low cost (<$500) instrumentation with software for data interpretation in Python. The software models geophysical data (electrical resistivity, seismic refraction, etc.) to identify choice sites for drilling a well. Software should incorporate an easy-to-use GUI, trap errors, and be easily deployable on any PC. Some code will also be used for interfacing with microcomputers recording real time data and this must be robust under trying field conditions. 

## VESinverse
### How to run
- The code is in resistivity/VESinverse
- VESgui.py runs the gui 
- VESinverse.py is all the computational code tha the gui and tests access
- tests.py runs the automatic tests


## SeismicRefraction
### How to run
- The code is in seismicRefraction/ReadSorted
- gui.py runs the gui which runs both ReadSorted.py and SortFiles.py
- SortFiles.py takes in 1+ csv files with Seismic data, or a .zip files that contains 1+ csv files
- ReadSorted.py reads the output files from SortFiles (i.e. the sorted seismic data) and displays an interactive graph


## Pyinstaller
- Pyinstaller can be installed using the command promp and using the command
```
        pip install pyinstaller
```
- To compile use the following command
```
        pyinstaller --windowed --onefile --name <name> <path-to-script>
```
- --windowed flag makes it so that the command line does not open behind the gui
- --onefile flag results in a single executable file in the dist folder
- --name sets the name for the executable (does not work in Windows XP)
- path-to-script is the path to the script that is to be compiled

#### If pyinstaller runs on a system with Anaconda, the resulting executable will likely be 300+ mb


***
***
## Links
link to explanations for geophysical methods
https://gpg.geosci.xyz/

link for Univ of British Columbia open source inversion software
https://simpeg.xyz/

and here is a link to the Univ fo British Columbia jupyter notebooks for the resistivity inversions used in their
Myanmar Geoscientists withiout Borders project
https://github.com/simpeg-research/gwb-dc-inversions/blob/master/README.md

- executables can be download at https://ajvrieland.github.io/

## TODO
- Remove Scale in SeismicRefracton/ReadSorted/ReadSorted.py
- Make the Navigation bar update correctly in SeismicRefraction/ReadSorted/gui.py

### Known bugs
- Navigation bar in the Seismic Refraction GUI duplicates when updating the graph
- Output clicks button only outputs when GUI is closed
- executable for SeismicReadnSort is only for windows 10