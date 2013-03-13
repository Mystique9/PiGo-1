PiGo
====

PiGo repository


# Install

The following install process is tailored for official distribution of 
Raspbian for Raspberry Pi. Install the Raspbian as usual.
To download the PiGo install, type the following commands in the 
command line (ssh access):
'''bash
  mkdir PiGo
  git clone https://github.com/designspark/PiGo.git
'''

Then, to install the PiGo library, type
'''Bash
  sudo sh Install.sh
'''
  
After the installation completes, reboot the Raspberry for changes to take
the effect 
'''BashLexer
  sudo reboot
'''  

# Running the demo

PiGo demo displays graphical user interface. To start the demo, open the
LXTerminal from Raspbian desktop and navigate to PiGo/Demo folder. Then,
type the following command
'''BashLexer
  sudo sh enableRoot.sh
'''
This will enable the python script running as root, to display a window
in the X11 window manager. Then, start the demo
* for Raspberry Pi boards revision 1:
'''BashLexer
  sudo python PiGo_demo.py rev1 
'''
* for Raspberry Pi boards revision 2:
'''BashLexer
  sudo python PiGo_demo.py rev2
'''  
  

