#dxTuber

dxTuber is the first cavity detection tool that takes into account protein and cavity dynamics 
using solvent and protein residence probabilities derived from molecular dynamics (MD) simulations. 
dxTuber supports all MD packages that VMD can process.

dxTuber results can be exported in PDB format where each cavity is an individually selectable object 
of coherent voxels written as pseudo atoms, each holding the residence probability information, 
in the form of mass-weighted solvent densities encoded as formal b-factors.

It calculates pore and tunnel profiles along principal axis, 
furthermore cavity volumes and solvent densities can be directly extracted from the PDB files. 
Based on this data cavity statistics can be obtained easily.

dxTuber is licensed under the GPLv2 (-> gpl2-2.0.txt)


#Dependencies 

- GTK+ / Bonobo
- Python 2.5 and 2.6 are tested (please mail me if you tested other versions successfull ;)
- Python-gtk  
  - Required for GUI version
- Python-argparse for python < 2.7 (The argparse lib should be available in python 2.7+)
  http://code.google.com/p/argparse/  
  - Required for cmd version 
  
    
#Installation 

1. extract and copy all files in a directory you like 
   (e.g. /opt/dxTuber)
2. create in your home folder a .dxTuber folder (~/.dxTuber)
3. copy dxTuber.conf into ~/.dxTuber/
4. modify dxTuber.conf <INSTALL_DIR> (full path of [1.] e.g. /opt/dxTuber)
5. create softlinks of 
   dxTuber_gtk.py       | gui version
   dxTuber_cmd.py       | command line version
   analyzeCavity.py     | cmd version of analyze function 
   dx2pdb.py            | OpenDX -> PDB  convertor
   pdb2dx.py            | PDB -> OpenDX  convertor // supports only previously processed dxTuber PDB files.
   postgroupcavities.py | Pythonscript that devides cavities into subcavities
   in /usr/bin (optional) 
6. start dxTuber_gtk.py 


#How to use dxTuber 

The program is started from the console by typing dxTuber_gtk.py. 
While the dxTuber is driven by a graphical user interface, general status messages 
and information on calculation progress are printed to the console. Protein and water 
OpenDX VolMap files are imported via the OpenDX panel and specified in the Files tab. 
Scan initiates a cavity search using the protein density threshold and scanning method 
specified in the Settings tab. 

Once a search is completed, the found set of cavity voxels appears as a new row in the 
Files tab that can be selected for clustering into coherent cavities (Group DX), 
filtering (Filter), analysis (Analyze) or export. The latter can be done via the Save to DX or 
Save to PDB dialogue to save a selected set of cavity voxels in PDB or OpenDX format at any time.    

Coherent cavities can be analyzed in respect to their cross-sectional area along one of 
the principal axes. Therefore a principal axis and the cavity of interest need to be 
specified which is done based on each cavity's unique denomination that is encoded 
as atom name in the exported PDB file. 


#Tested on 

- Suse Linux 10.3 Enterprise / 11 (32 Bit)
- openSuse 11.3 (32 Bit)
- Ubuntu 10.4 LTS (32 Bit)
- Fefora 19
- Fedora 20
- Debian 8 (64 Bit)

#Known Bugs / Issues 

- Compiz can disturb the dxTuber widget so that the main window title is not shown. 
-> Disable Compiz

- dxTuber stops reading / calculating / saving / grouping ... 
-> Keep the shell in focus

- To stop or shut down dxTuber_gtk hit 'ctrl +c' in the shell where dxTuber was startet from. 
(I tried several hours to catch the term signal from gtk window with no success...)

- After reading / scanning / saving all radio buttons are resetted
-> Ensure your selections are correct until this bug is fixed. 

- pyGTK gets outdated & can not be compiled / installed
-> use the command line version of dxTuber


#Acknowledgements 

## Research lab: Computational Structural Biology @ University of Bonn: 

Christian Kandt			Supervising, Bugtesting
Nadine Fischer 			Bugtesting
Thomas H. Schmidt		Bugtesting, Typos ;)

## Extranal:
Mattia Sturlese			Bugreport


#Developed by 

Martin Raunest 
Contact
e-mail: m.raunest@gmx.de
xmpp: raunest@jabber.org 
