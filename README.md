## VESinverse
### How to run
-The code is in resistivity/VESinverse

-VESgui.py runs the gui 

-VESinverse.py is all the computational code tha the gui and tests access

-tests.py runs the automatic tests

### Pyinstaller
-Pyinstaller can be installed using the command promp and using the command
```
        pip install pyinstaller
```
-To compile use the following command
```
        pyinstaller --windowed --onefile --name <name> <path-to-script>
```
-windowed flag makes it so that the command line does not open behind the gui

-onefile flag results in a single executable file in the dist folder

-name sets the name for the executable (does not work in Windows XP)

-<path-to-script> is the path to the script that is to be compiled

link to explanations for geophysical methods
https://gpg.geosci.xyz/

link for Univ of British Columbia open source inversion software
https://simpeg.xyz/

and here is a link to the Univ fo British Columbia jupyter notebooks for the resistivity inversions used in their
Myanmar Geoscientists withiout Borders project
https://github.com/simpeg-research/gwb-dc-inversions/blob/master/README.md

executables can be download at https://ajvrieland.github.io/
