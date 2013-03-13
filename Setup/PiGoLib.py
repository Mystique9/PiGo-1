#       File: PiGoLib.py
#       Description: PiGo board IO library
#       
#       Copyright 2013 Matevz Bosnak <matevz@poscope.com>
#
#       Parts of this library consist of code written by other authors:
#            Mike McCauley (mikem@open.com.au) - primary bcm2835 library
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#      
#       Dependencies:
#         Raspberry Pi and PiGo board: obviously...
#         bcm2835.so: shared library for the peripherals support, provided with this library
#         pyserial-2.6: library for serial (UART) communication
#
#  CHANGELOG:
#  	February 2 (v1.00):
#     - initial release

from ctypes import *
import serial
import PiGoBoardData

class PiGoBoard:

	# Initialize SPI interface
	# Arguments:
	#   SPIdivider: a constant that is used to divide the original 250 MHz clock for SPI, default value is 1024, giving 244 kHz SPI clock
	def SPIinit(self, SPIdivider = PiGoBoardData.BCM2835_SPI_CLOCK_DIVIDER_1024):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return
			
		# Save some space and bring the libObj to function space
		libObj = self.libObj
		
		# Initialize SPI pins
		libObj.bcm2835_spi_begin()
		# Set mode 0 (CPOL = 0, CPHA = 0: Rest state of clock is low, first CLK transition at middle of data bit)
		libObj.bcm2835_spi_setDataMode(PiGoBoardData.BCM2835_SPI_MODE0)        
		# Set clock divider (250 kHz SPI clock)        
		libObj.bcm2835_spi_setClockDivider(SPIdivider)
		
		# Set default chip select and polarity
		self.SPIsetCS()

	# Set chip select and polarity of it
	# Arguments:
	#   CS: chip select constant (BCM2835_SPI_CS0 for the primary chip select, BCM2835_SPI_CS1 for the secondary chip select)
	def SPIsetCS(self, CS = PiGoBoardData.BCM2835_SPI_CS0, polarity = 0):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return

		# Set chip select
		self.libObj.bcm2835_spi_chipSelect(CS)
		# Set chip select polarity
		self.libObj.bcm2835_spi_setChipSelectPolarity(PiGoBoardData.BCM2835_SPI_CS0, polarity)      


	# SPI transfer data
	# Arguments:
	#   data: array of integers (8-bit) to be written to target SPI device
	# Returns:
	#   an array of integers, returned by the SPI device,  with the same size as provided in data
	def SPItransfer(self, data):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return []

		# If user provided only single integer, transfer it...
		if isinstance(data, int):
			numBytes = 1
			SPIdata = c_ubyte * 1
			buf = SPIdata(data)
			
		else:
			# Construct a c_byte array of numBytes bytes
			numBytes = len(data)
			SPIdata = c_ubyte * numBytes
			
			# Copy the Python array to c_byte array
			buf = SPIdata()
			for i in range(0, numBytes):
				buf[i] = data[i]

		# Transfer the data to SPI device and read it back
		self.libObj.bcm2835_spi_transfern(buf, numBytes)	
		
		# Return the array with the results
		return [buf[i] for i in range(0, numBytes)]
		
	# SPI read data
	# Arguments:
	#   numBytes: number of bytes to be read from SPI device
	# Returns:
	#   an array of integers, returned by the SPI device, with the size of numBytes
	def SPIread(self, numBytes):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return []
		
		# Construct the c_byte array of numBytes bytes
		SPIdata = c_ubyte * numBytes
		buf = SPIdata()
		
		# Read the data from SPI device
		self.libObj.bcm2835_spi_transfern(buf, numBytes)
		
		return [buf[i] for i in range(0, numBytes)]		
	
	# Initialize PWM module
	# Arguments:
	#   none
	# Returns:
	#   none
	def PWMinit(self):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return
			
		# Save some space and bring the libObj to function space
		libObj = self.libObj
		
		libObj.bcm2835_gpio_fsel(PiGoBoardData.RPI_GPIO_P1_12, PiGoBoardData.BCM2835_GPIO_FSEL_ALT5)
		# User fixed 32 for clock divider
		libObj.bcm2835_pwm_init(PiGoBoardData.BCM2835_PWM0_ENABLE | PiGoBoardData.BCM2835_PWM0_MS_MODE, 32)
		
  # Setup PWM period
	# Arguments:
	#   period: PWM period in seconds
	# Returns:
	#   none
	def PWMsetPeriod(self, period):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return
		
		libObj = self.libObj
		self.PWMperiod = period * 4800000 
		libObj.bcm2835_pwm0_setRange(int(self.PWMperiod))
		
  # Setup PWM duty cycle
	# Arguments:
	#   period: PWM duty cycle (in the range from 0 to 1)
	# Returns:
	#   none
	def PWMsetDuty(self, duty):
		# Check if library was initialized successfully, if not, raise the exception
		if self.libInitialized == False:
			return
		
		if duty > 1:
			duty = 1
		elif duty < 0:
			duty = 0

		libObj = self.libObj
		libObj.bcm2835_pwm0_setData(int(duty * self.PWMperiod))
			
	
	# Set target I2C device address
	# Arguments:
	#   addr: I2C device address (in the range from 0 to 127)
	# Returns:
	#   none
	def I2CsetTargetAddress(self, addr):
		if self.libInitialized == False:
			return
		
		libObj = self.libObj
		libObj.bcm2835_i2c_setAddr(addr)

	# Write to I2C device
	# Arguments:
	#   data: data to be written to I2C device
	# Returns:
	#   True if data was acknowledged, False otherwise
	def I2CWrite(self, data):
		if self.libInitialized == False:
			return
		
		libObj = self.libObj
	
		# If user provided only single integer, transfer it...
		if isinstance(data, int):
			numBytes = 1
			I2Cdata = c_ubyte * 1
			buf = I2Cdata(data)
			
		else:
			# Construct a c_byte array of numBytes bytes
			numBytes = len(data)
			I2Cdata = c_ubyte * numBytes
			
			# Copy the Python array to c_byte array
			buf = I2Cdata()
			for i in range(0, numBytes):
				buf[i] = data[i]

		# Write the data to I2C device
		if self.libObj.bcm2835_i2c_write(buf, numBytes) < numBytes:
			return False
		else:
			return True
		
	# Read from I2C device
	# Arguments:
	#   numBytes: number of bytes to be read from I2C device
	# Returns:
	#   Array of data if data was send by the device, empty array otherwise
	def I2CRead(self, numBytes):
		if self.libInitialized == False:
			return []
		
		libObj = self.libObj

		I2Cdata = c_ubyte * numBytes
		buf = I2Cdata()
		
		# Read the data from I2C device
		if self.libObj.bcm2835_i2c_read(buf, numBytes) < 0:
			return []
		else:
			# Return the array with the results
			return [buf[i] for i in range(0, numBytes)]
					
			
	# Open serial port using pySerial module
	# Arguments:
	#   baud: baudrate (default: 9600)
	#   port: serial port name (default: '/dev/ttyAMA0')
	#   timeoutValue: read timeout in seconds (default: 1s)
	#   bytesizeValue: length of the data byte (default: serial.EIGHTBITS)
	#       possible values: serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS
	#   parityValue: parity check (default: PARITY_NONE)
	#       possible values: serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, 
	#												 serial.PARITY_MARK, serial.PARITY_SPACE)
	#   stopbitsValue: number of stop bits (default: serial.STOPBITS_ONE)
	#       possible values: serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO
	# Returns:
	#   none
	def serialOpen(self, baud = 9600, port = '/dev/ttyAMA0', timeoutValue = 1, parityValue = serial.PARITY_NONE,
								bytesizeValue = serial.EIGHTBITS, stopbitsValue = serial.STOPBITS_ONE):
		if self.libInitialized == False:
			return
			
		if self.serObj is not None:
			if serlf.serObj.isOpen():
				self.serObj.close()
		
		self.serObj = serial.Serial(port, baud, timeout=timeoutValue, bytesize = bytesizeValue, stopbits = stopbitsValue)
		self.serObj.flush()
		
	# Close serial port
	# Arguments:
	#   none
	# Returns:
	#   none		
	def serialClose(self):
		if self.libInitialized == False:
			return
		if self.serObj is not None:
			if self.serObj.isOpen():
				self.serObj.close()
			
		self.serObj = None
		
	# Write to serial port
	# Arguments:
	#   data: data to write to serial port
	# Returns:
	#   none				
	def serialWrite(self, data):
		if self.libInitialized == False:
			return
		if self.serObj is not None:
			if self.serObj.isOpen():
				self.serObj.write(data)
			
	# Check serial port input buffer
	# Arguments:
	#   none
	# Returns:
	#   True if data is in the input buffer					
	def serialkbhit(self):
		if self.libInitialized == False:
			return False
		if self.serObj is not None:
			if self.serObj.isOpen():
				return (self.serObj.inWaiting() > 0)
		
		return False
	
	# Read from serial port
	# Arguments:
	#   length: number of bytes to read from serial port
	# Returns:
	#   Array of length-bytes. 
	# from pySerial manual: If a timeout is set it may return less characters as requested. 
	# With no timeout it will block until the requested number of bytes is read.			
	def serialRead(self, length):
		if self.libInitialized == False:
			return ""
		if self.serObj is not None:
			if self.serObj.isOpen():
				return self.serObj.read(length)
		
		return ""
		

		
		
	# *********************************
	#       HIGH-LEVEL commands 
	# *********************************
	
	# Refresh extended IOs directions
	# Arguments:
	#   none
	# Returns:
	#   none
	def refreshIOdir(self):
		if self.libInitialized == False:
			return

		# Refresh only the IO register that has changed
		for i in range(0,4):
			if self.portDirPrev[i] != self.portDir[i]:
				#print("refreshing..." + str(i) + ": " + str(self.portDir[i]))
				if i < 2:
					self.I2CsetTargetAddress(0x20)
				else:
					self.I2CsetTargetAddress(0x24)
				# Set IODIR register
				if self.I2CWrite([0x01 * int(i % 2), self.portDir[i]]) == False:
					print("Error writing to I2C")
						
			self.portDirPrev[i] = self.portDir[i];

	# Refresh extended IO - outputs' states
	# Arguments:
	#   none
	# Returns:
	#   none
	def refreshOstat(self):
		if self.libInitialized == False:
			return

		# Refresh only the IOLAT registers that have changed
		for i in range(0,4):
			if self.portStatPrev[i] != self.portStat[i]:
				#print("refreshing..." + str(i))
				if i < 2:
					self.I2CsetTargetAddress(0x20)
				else:
					self.I2CsetTargetAddress(0x24)

				# Set IOLAT register
				self.I2CWrite([0x14 + 0x01 * int(i % 2), self.portStat[i]])
							
			self.portStatPrev[i] = self.portStat[i];
			
	# Refresh extended IO - inputs' states
	# Arguments:
	#   none
	# Returns:
	#   none
	def refreshIstat(self):
		if self.libInitialized == False:
			return

		# Refresh all GPIO registers
		self.I2CsetTargetAddress(0x20)
		self.I2CWrite([0x12])
		iostat = self.I2CRead(2)
		self.portStat[0] = iostat[0]
		self.portStat[1] = iostat[1]

		self.I2CsetTargetAddress(0x24)
		self.I2CWrite([0x12])
		iostat = self.I2CRead(2)
		self.portStat[2] = iostat[0]
		self.portStat[3] = iostat[1]    
					

	# ********************************************
	# Raspberry IO
	# ********************************************
	
	# Set Raspberry IO direction
	# Arguments:
	#   raspIOpin: Raspberry IO pin index
	# 	IODir: pin direction (0 for output, 1 for input)
	# Returns:
	#   none
	def RaspSetIOdir(self, raspIOpin, IODir):
		if self.libInitialized == False:
			return
		
		if IODir:
			self.libObj.bcm2835_gpio_fsel(raspIOpin, PiGoBoardData.BCM2835_GPIO_FSEL_INPT)
			self.libObj.bcm2835_gpio_set_pud(raspIOpin, PiGoBoardData.BCM2835_GPIO_PUD_UP)
		else:
			self.libObj.bcm2835_gpio_fsel(raspIOpin, PiGoBoardData.BCM2835_GPIO_FSEL_OUTP)

	# Set Raspberry digital output state
	# Arguments:
	#   raspIOpin: Raspberry IO pin index
	#		IOvalue: output pin state
	# Returns:
	#   none
	def RaspSetOutput(self, raspIOpin, IOvalue):
		if self.libInitialized == False:
			return

		self.libObj.bcm2835_gpio_write(raspIOpin, IOvalue)

	# Get Raspberry digital input state
	# Arguments:
	#   raspIOpin: Raspberry IO pin index
	# Returns:
	#   Digital input state
	def RaspGetInput(self, raspIOpin):
		if self.libInitialized == False:
			return 0

		return self.libObj.bcm2835_gpio_lev(raspIOpin)
		

	# ********************************************
	# Buffered IO
	# ********************************************    

	# Set buffered IO direction
	# Arguments:
	#   IONr: Buffered IO pin (0-7)
	#		IODir: Buffered IO direction (0 for output, 1 for input)
	#		SetValues: if 0, no I2C operation is executed (default: 1)
	# Returns:
	#   none
	def setIOdir(self, IONr, IODir, SetValues = 1):
		if self.libInitialized == False:
			return

		self.portDir[0] &= ~(1 << int(IONr % 8))
		if IODir:
				self.portStat[0] |= (1 << int(IONr % 8))
		else:
				self.portStat[0] &= ~(1 << int(IONr % 8))            
		if SetValues:
				self.refreshIOdir()
				self.refreshOstat()

		self.RaspSetIOdir(self.IOpins[IONr], IODir) 


	# Return buffered IO direction
	# Arguments:
	#   IONr: Buffered IO pin (0-7)
	# Returns:
	#   Direction of the buffered IO pin
	def getIOdir(self, IONr):
		if self.libInitialized == False:
			return 0
		if self.portDir[0] & (1 << int(IONr % 8)):
			return 1
		else:
			return 0    

	# Set buffered IO state
	# Arguments:
	#   IONr: Buffered IO pin (0-7)
	#		IOvalue: Set buffered digital output state
	# Returns:
	#   none
	def setIO(self, IONr, IOvalue):
		if self.libInitialized == False:
			return
		self.RaspSetOutput(self.IOpins[IONr], IOvalue)

	# Return buffered IO value
	# Arguments:
	#   IONr: Buffered IO pin (0-7)
	# Returns:
	#   State of the input pin
	def getIO(self, IONr):
		if self.libInitialized == False:
			return 0
		return self.RaspGetInput(self.IOpins[IONr])


	# ********************************************
	# External IO
	# ********************************************    

	# Set external IO direction
	# Arguments:
	#   ExtPinNr: External IO number (0-15)
	#		PinDir: Pin direction (0 for output, 1 for input)
	#		SetValues: if 0, no I2C refresh operation is executed (default: 1)
	# Returns:
	#   none
	def setExtIOdir(self, ExtPinNr, PinDir, SetValues = 1):
		if self.libInitialized == False:
			return
		if PinDir:
			self.portDir[1 + 2 * int(ExtPinNr / 8)] |= (1 << int(ExtPinNr % 8))
		else:
			self.portDir[1 + 2 * int(ExtPinNr / 8)] &= ~(1 << int(ExtPinNr % 8))
		if SetValues:
			self.refreshIOdir()

	# Return external IO direction   
	# Arguments:
	#   ExtPinNr: External IO number (0-15)
	# Returns:
	#   Pin direction
	def getExtIOdir(self, ExtPinNr):
		if self.libInitialized == False:
			return 0
			
		if self.portDir[1 + 2 * int(ExtPinNr / 8)] & (1 << int(ExtPinNr % 8)):
			return 1
		else:
			return 0

	# Set external IO value
	# Arguments:
	#   ExtPinNr: External IO number (0-15)
	#		PinValue: Output pin state
	#		SetValues: if 0, no I2C refresh operation is executed (default: 1)
	# Returns:
	#   none
	def setExtIO(self, ExtPinNr, PinValue, SetValues = 1):
		if self.libInitialized == False:
			return
			
		if PinValue:
			self.portStat[1 + 2 * int(ExtPinNr / 8)] |= (1 << int(ExtPinNr % 8))
		else:
			self.portStat[1 + 2 * int(ExtPinNr / 8)] &= ~(1 << int(ExtPinNr % 8))

		self.refreshOstat()

	# Get external IO value
	# Arguments:
	#   ExtPinNr: External IO number (0-15)
	#		ReadValues: if 0, no I2C refresh operation is executed (default: 1)
	# Returns:
	#   State of the input pin
	def getExtIO(self, ExtPinNr, ReadValues = 1):
		if self.libInitialized == False:
			return 0
		if ReadValues == 1:
			self.refreshIstat()
		
		if self.portStat[1 + 2 * int(ExtPinNr / 8)] & (1 << int(ExtPinNr % 8)):
			return 1
		else:
			return 0				
			
			
	def delay(self, time_ms):
		if self.libInitialized == False:
			return 0

		self.libObj.bcm2835_delay(time_ms);
		
		
	def TestSPI(self):
		self.SPIinit()
		self.SPIsetCS()
		
		libObj = self.libObj
		
		print("SPI read:")
		print(self.SPItransfer([0xAA, 0x00]))
		libObj.bcm2835_delay(1000);
		print("Knight rider effect...")


		for i in range(0, 255):
			self.SPItransfer(i)
			libObj.bcm2835_delay(1)
		
		i = 0
		while True:
			if i > 7:
				data = 1 << (15 - i)
			else:
				data = 1 << i
				
			if i >= 15: 
				i = 0
			else:
				i += 1
				
			self.SPItransfer([data])

			libObj.bcm2835_delay(80)	

	# Initialize PiGo library class
	# Arguments:
	#   RPi_Rev: Raspberry Pi board revision
	#		TestMode: If set to 1, the library is run in test mode and no hardware is accessed
	# Returns:
	#   none
	def __init__(self, RPi_Rev = 1, TestMode = 0):
		self.libInitialized = False
		
		self.TEST_MODE = TestMode
				
		if self.TEST_MODE == 0:
			# Try and load the libBCM.so shared library for communication with the peripherals
			try:
				self.libObj = cdll.LoadLibrary("libBCM.so")
				#print("PiGo library loaded succesfully!")
			except OSError:
				# The library was not found - raise an error
				raise OSError("ERROR: PiExp library not found!\nHint: Please check that you have successfully installed the PiExp library!")
				return

			# If library was found and loaded, continue and initialize the memory mapping
			if RPi_Rev == 1:
				i2cBus = 0
			else:
				i2cBus = 1
				
			if self.libObj.bcm2835_add_init(i2cBus) == 0:
				# Memory mapping was not successfull - apparently user has no right to access the peripherals
				raise EnvironmentError("ERROR: Current user has no direct access to Raspberry Pi Hardware!\nHint: Check that you are running as root") 
				return
			else:
				self.libInitialized = True

		# Serial connection (UART) has not yet been initialized
		self.serObj = None
		
		# Initialize IO drivers
		self.portDir = [ 0xFF, 0xFF, 0xFF, 0xFF]
		self.portStat = [ 0, 0, 0, 0]

		self.portDirPrev = [1, 1, 1, 1]
		self.portStatPrev = [1, 1, 1, 1]
		self.refreshIOdir()
		self.refreshOstat()	
		
		self.piRev = RPi_Rev		

		if RPi_Rev == 1:
			self.IOpins = [18, 23, 24, 25, 4, 17, 21, 22]
		else:
			self.IOpins = [18, 23, 24, 25, 4, 17, 27, 22]
			
# A/D and D/A module class
# For A/D MCP3002 is used with dual channels, configurable as single ended or differential
class ModuleADDA:
	# ModuleADDA constructor
	# Arguments:
	#   PiGoBoardObject: reference to the PiGoBoard object for hardware access
	#		SocketID: PiGo board physical socket, where ADDA module is attached to ('A','B','C', or 'D')
	# Returns:
	#   none
	def __init__(self, PiGoBoardObject, SocketID):
		self.host = PiGoBoardObject
		self.socket = SocketID

		self.CS_AD = {
				'A': 0,
				'B': 2,
				'C': 4,
				'D': 6
		}[SocketID]
		self.CS_DA = self.CS_AD + 1

		# Initialize CS (chip-select) pins
		self.host.setExtIOdir(self.CS_AD, 0, 0)
		self.host.setExtIOdir(self.CS_DA, 0, 1)

		self.host.setExtIO(self.CS_AD, 1, 0)
		self.host.setExtIO(self.CS_DA, 1, 1)

		# Initialize SPI bus
		self.host.SPIinit()

		#print("ADDA board initialized on module " + SocketID + " with AD_CS=" + str(self.CS_AD) + " and DA_CS=" + str(self.CS_DA))

	# Read A/D
	# Arguments:
	#   channel: A/D channel (0-1)
	# Returns:
	#   10-bit analog input value
	def getAD(self, channel):

		# Assert AD CS signal
		self.host.setExtIO(self.CS_AD, 0)
		
		# Send conversion request
		cmd = [0x00, 0x00]
		cmd[0] |= (1 << 6) # Start bit
		cmd[0] |= (1 << 5) # Single ended mode
		if channel == 1:
			cmd[0] |= (1 << 4) # Channel 1 selection

		cmd[0] |= (1 << 3) # MSB data first, please

		adData = self.host.SPItransfer(cmd)
	
		# Deassert AD CS signal
		self.host.setExtIO(self.CS_AD, 1)
				
		# Return A/D value
		return ((adData[0] << 8) + adData[1]) & 0x3FF

	# Set D/A
	# Arguments:
	#   channel: D/A channel (0 for channel 'A' or 1 for channel 'B')
	#		value: 10-bit D/A value
	# Returns:
	#   none
	def setDA(self, channel, value):

		# Assert DA CS signal
		self.host.setExtIO(self.CS_DA, 0)

		# Send conversion request
		cmd = [0x0F & (value >> 6), (value << 2) & 0xFF]
		if channel == 1:
			cmd[0] |= (1 << 7) # Channel B selection

		cmd[0] |= (1 << 5) # Set 1x gain (0-VREF)
		cmd[0] |= (1 << 4) # Enable selected channel

		self.host.SPItransfer(cmd)

		# Deassert DA CS signal
		self.host.setExtIO(self.CS_DA, 1)
		return


# Motor module class
class ModuleMotor:
	# Motor module constructor
	# Arguments:
	#   PiGoBoardObject: reference to the PiGoBoard object for hardware access
	#		SocketID: PiGo board physical socket, where the module is attached to ('A','B','C', or 'D')
	#   Mode: 0 (digital mode) or 1 (PWM mode)
	# Returns:
	#   none
	def __init__(self, PiGoBoardObject, SocketID, mode, PWMfreq = 1000.0):
		self.host = PiGoBoardObject
		self.socket = SocketID
		self.mode = mode

		if self.mode == 0:
			# user selected digital mode...
			self.IN1 = {
					'A': 0,
					'B': 2,
					'C': 4,
					'D': 6
			}[SocketID]
			self.IN2 = self.IN1 + 1

			
			# Initialize control pins
			self.host.setExtIOdir(self.IN1, 0, 0)
			self.host.setExtIOdir(self.IN2, 0, 1)

			self.host.setExtIO(self.IN1, 0, 0)
			self.host.setExtIO(self.IN2, 0, 1)
			print("Motor board initialized on module " + SocketID + " with IN1=" + str(self.IN1) + " and IN2=" + str(self.IN2))
		else:
			# user selected PWM mode
			
			# Initialize PWM output
			self.host.setIOdir(0, 0, 1)
			self.host.PWMinit()
			self.host.PWMsetPeriod(1.0/PWMfreq)
			self.host.PWMsetDuty(0)
						
						
			# Initialize the second control pin
			self.host.setIOdir(1, 0, 1)
			self.host.setIO(1, 0)
			
			print("Motor board initialized on module " + SocketID + " in PWM mode on buffered pins 1 and 2")
			
		self.prevPower = 0

	# Set motor power
	# Arguments:
	#   power: motor power (-1 to 1)
	# Returns:
	#   none
	def setOutput(self, power):
		if self.prevPower == power:
			return
						
		if self.mode == 0:
			if power < 0:
				self.host.setExtIO(self.IN1, 0, 0)
				self.host.setExtIO(self.IN2, 1, 1)
			elif power > 0:
				self.host.setExtIO(self.IN1, 1, 0)
				self.host.setExtIO(self.IN2, 0, 1)
			else:
				self.host.setExtIO(self.IN1, 0, 0)
				self.host.setExtIO(self.IN2, 0, 1)
			
		else:
			if power > 1:
				power = 1
			if power < -1:
				power = -1
				
			if power >= 0:
				if self.prevPower < 0:
					self.host.setIO(1, 0)

				self.host.PWMsetDuty(power)
			else:
				if self.prevPower >= 0:
					self.host.setIO(1, 1)

				self.host.PWMsetDuty(1+power)
			
		
		self.prevPower = power
		
		
def main():
	lib = PiGoBoard()
	
	# Open serial port and send Hello
	lib.serialOpen(19200)
	lib.serialWrite("Hello")
	if lib.serialkbhit():
		print("Received '" + lib.serialRead(1) + "'")
	else:
		print("No serial data...")
		
	lib.serialClose()
	
	
	# Setup PWM with 1s period and 50% duty cycle
	lib.PWMinit()
	lib.PWMsetPeriod(1);
	lib.PWMsetDuty(0.5);
	
	# Scan for all I2C devices
	for a in range(0, 127):
		lib.I2CsetTargetAddress(a)
		if lib.I2CWrite([0]) == True:
			print "Device found at address " + hex(a)

	# Test read the LM75 sensor
	lib.I2CsetTargetAddress(0x48)
	if lib.I2CWrite([0]) == True:
		result = lib.I2CRead(2)
	
		# Second element holds the 0.5 deg. C
		if (result[1] < 0):
			halfDegree = 5
		else:
			halfDegree = 0
			
		print "LM75: " + str(result[0]) + "." + str(halfDegree) + " deg. C"
	else:
		print "LM75 was not found at the specified address!"
	
	
	return 0
	

	lib.TestSPI()
	
	
	return 0

if __name__ == '__main__':
	main()
