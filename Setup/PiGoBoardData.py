# Port function select modes
BCM2835_GPIO_FSEL_INPT = 0b000	# Input
BCM2835_GPIO_FSEL_OUTP  = 0b001 # Output
BCM2835_GPIO_FSEL_ALT0  = 0b100 # Alternate function 0
BCM2835_GPIO_FSEL_ALT1  = 0b101 # Alternate function 1
BCM2835_GPIO_FSEL_ALT2  = 0b110 # Alternate function 2
BCM2835_GPIO_FSEL_ALT3  = 0b111 # Alternate function 3
BCM2835_GPIO_FSEL_ALT4  = 0b011 # Alternate function 4
BCM2835_GPIO_FSEL_ALT5  = 0b010 # Alternate function 5
BCM2835_GPIO_FSEL_MASK  = 0b111 # Function select bits mask

# Pull-up and Pull-down resistor configuration
BCM2835_GPIO_PUD_OFF     = 0b00 # Off ? disable pull-up/down
BCM2835_GPIO_PUD_DOWN    = 0b01 # Enable Pull Down control
BCM2835_GPIO_PUD_UP      = 0b10 # Enable Pull Up control


# Raspberry Pi GPIO pins
RPI_GPIO_P1_03        =  0 # Pin P1-03
RPI_GPIO_P1_05        =  1 # Pin P1-05
RPI_GPIO_P1_07        =  4 # Pin P1-07
RPI_GPIO_P1_08        = 14 # Pin P1-08 defaults to alt function 0 UART0_TXD
RPI_GPIO_P1_10        = 15 # Pin P1-10 defaults to alt function 0 UART0_RXD
RPI_GPIO_P1_11        = 17 # Pin P1-11
RPI_GPIO_P1_12        = 18 # Pin P1-12
RPI_GPIO_P1_13        = 21 # Pin P1-13
RPI_GPIO_P1_15        = 22 # Pin P1-15
RPI_GPIO_P1_16        = 23 # Pin P1-16
RPI_GPIO_P1_18        = 24 # Pin P1-18
RPI_GPIO_P1_19        = 10 # Pin P1-19 MOSI when SPI0 in use
RPI_GPIO_P1_21        =  9 # Pin P1-21 MISO when SPI0 in use
RPI_GPIO_P1_22        = 25 # Pin P1-22
RPI_GPIO_P1_23        = 11 # Pin P1-23 CLK when SPI0 in use
RPI_GPIO_P1_24        =  8 # Pin P1-24 CE0 when SPI0 in use
RPI_GPIO_P1_26        =  7 # Pin P1-26 CE1 when SPI0 in use

RPI_GPIO_P1_03_v2        =  2 # Pin P1-03
RPI_GPIO_P1_05_v2        =  3 # Pin P1-05
RPI_GPIO_P1_07_v2        =  4 # Pin P1-07
RPI_GPIO_P1_08_v2        = 14 # Pin P1-08 defaults to alt function 0 UART0_TXD
RPI_GPIO_P1_10_v2        = 15 # Pin P1-10 defaults to alt function 0 UART0_RXD
RPI_GPIO_P1_11_v2        = 17 # Pin P1-11
RPI_GPIO_P1_12_v2        = 18 # Pin P1-12
RPI_GPIO_P1_13_v2        = 27 # Pin P1-13
RPI_GPIO_P1_15_v2        = 22 # Pin P1-15
RPI_GPIO_P1_16_v2        = 23 # Pin P1-16
RPI_GPIO_P1_18_v2        = 24 # Pin P1-18
RPI_GPIO_P1_19_v2        = 10 # Pin P1-19 MOSI when SPI0 in use
RPI_GPIO_P1_21_v2        =  9 # Pin P1-21 MISO when SPI0 in use
RPI_GPIO_P1_22_v2        = 25 # Pin P1-22
RPI_GPIO_P1_23_v2        = 11 # Pin P1-23 CLK when SPI0 in use
RPI_GPIO_P1_24_v2        =  8 # Pin P1-24 CE0 when SPI0 in use
RPI_GPIO_P1_26_v2        =  7 # Pin P1-26 CE1 when SPI0 in use

# PWM constants
BCM2835_PWM0_MS_MODE    = 0x0080 # Run in MS mode
BCM2835_PWM0_USEFIFO    = 0x0020 # Data from FIFO
BCM2835_PWM0_REVPOLAR   = 0x0010 # Reverse polarity
BCM2835_PWM0_OFFSTATE   = 0x0008 # Ouput Off state
BCM2835_PWM0_REPEATFF   = 0x0004 # Repeat last value if FIFO empty
BCM2835_PWM0_SERIAL     = 0x0002 # Run in serial mode
BCM2835_PWM0_ENABLE     = 0x0001 # Channel Enable	

# Defines for SPI
# GPIO register offsets from BCM2835_SPI0_BASE. 
# Offsets into the SPI Peripheral block in bytes per 10.5 SPI Register Map	
BCM2835_SPI0_CS                      = 0x0000 # SPI Master Control and Status
BCM2835_SPI0_FIFO                    = 0x0004 # SPI Master TX and RX FIFOs
BCM2835_SPI0_CLK                     = 0x0008 # SPI Master Clock Divider
BCM2835_SPI0_DLEN                    = 0x000c # SPI Master Data Length
BCM2835_SPI0_LTOH                    = 0x0010 # SPI LOSSI mode TOH
BCM2835_SPI0_DC                      = 0x0014 # SPI DMA DREQ Controls

# Register masks for SPI0_CS
BCM2835_SPI0_CS_LEN_LONG             = 0x02000000 # Enable Long data word in Lossi mode if DMA_LEN is set
BCM2835_SPI0_CS_DMA_LEN              = 0x01000000 # Enable DMA mode in Lossi mode
BCM2835_SPI0_CS_CSPOL2               = 0x00800000 # Chip Select 2 Polarity
BCM2835_SPI0_CS_CSPOL1               = 0x00400000 # Chip Select 1 Polarity
BCM2835_SPI0_CS_CSPOL0               = 0x00200000 # Chip Select 0 Polarity
BCM2835_SPI0_CS_RXF                  = 0x00100000 # RXF - RX FIFO Full
BCM2835_SPI0_CS_RXR                  = 0x00080000 # RXR RX FIFO needs Reading ( full)
BCM2835_SPI0_CS_TXD                  = 0x00040000 # TXD TX FIFO can accept Data
BCM2835_SPI0_CS_RXD                  = 0x00020000 # RXD RX FIFO contains Data
BCM2835_SPI0_CS_DONE                 = 0x00010000 # Done transfer Done
BCM2835_SPI0_CS_TE_EN                = 0x00008000 # Unused
BCM2835_SPI0_CS_LMONO                = 0x00004000 # Unused
BCM2835_SPI0_CS_LEN                  = 0x00002000 # LEN LoSSI enable
BCM2835_SPI0_CS_REN                  = 0x00001000 # REN Read Enable
BCM2835_SPI0_CS_ADCS                 = 0x00000800 # ADCS Automatically Deassert Chip Select
BCM2835_SPI0_CS_INTR                 = 0x00000400 # INTR Interrupt on RXR
BCM2835_SPI0_CS_INTD                 = 0x00000200 # INTD Interrupt on Done
BCM2835_SPI0_CS_DMAEN                = 0x00000100 # DMAEN DMA Enable
BCM2835_SPI0_CS_TA                   = 0x00000080 # Transfer Active
BCM2835_SPI0_CS_CSPOL                = 0x00000040 # Chip Select Polarity
BCM2835_SPI0_CS_CLEAR                = 0x00000030 # Clear FIFO Clear RX and TX
BCM2835_SPI0_CS_CLEAR_RX             = 0x00000020 # Clear FIFO Clear RX 
BCM2835_SPI0_CS_CLEAR_TX             = 0x00000010 # Clear FIFO Clear TX 
BCM2835_SPI0_CS_CPOL                 = 0x00000008 # Clock Polarity
BCM2835_SPI0_CS_CPHA                 = 0x00000004 # Clock Phase
BCM2835_SPI0_CS_CS                   = 0x00000003 # Chip Select

# bcm2835SPIBitOrder - Specifies the SPI data bit ordering
BCM2835_SPI_BIT_ORDER_LSBFIRST = 0  # LSB First
BCM2835_SPI_BIT_ORDER_MSBFIRST = 1   # MSB First

# bcm2835SPIMode - Specify the SPI data mode
BCM2835_SPI_MODE0 = 0  # CPOL = 0 CPHA = 0
BCM2835_SPI_MODE1 = 1  # CPOL = 0 CPHA = 1
BCM2835_SPI_MODE2 = 2  # CPOL = 1 CPHA = 0
BCM2835_SPI_MODE3 = 3  # CPOL = 1 CPHA = 1

# bcm2835SPIChipSelect - Specify the SPI chip select pin(s)
BCM2835_SPI_CS0 = 0     # Chip Select 0
BCM2835_SPI_CS1 = 1     # Chip Select 1
BCM2835_SPI_CS2 = 2     # Chip Select 2 (ie pins CS1 and CS2 are asserted)
BCM2835_SPI_CS_NONE = 3 # No CS control it yourself

# bcm2835SPIClockDivider - Specifies the divider used to generate the SPI clock from the system clock.
BCM2835_SPI_CLOCK_DIVIDER_65536 = 0       # 65536 = 262.144us = 3.814697260kHz
BCM2835_SPI_CLOCK_DIVIDER_32768 = 32768   # 32768 = 131.072us = 7.629394531kHz
BCM2835_SPI_CLOCK_DIVIDER_16384 = 16384   # 16384 = 65.536us = 15.25878906kHz
BCM2835_SPI_CLOCK_DIVIDER_8192  = 8192    # 8192 = 32.768us = 30/51757813kHz
BCM2835_SPI_CLOCK_DIVIDER_4096  = 4096    # 4096 = 16.384us = 61.03515625kHz
BCM2835_SPI_CLOCK_DIVIDER_2048  = 2048    # 2048 = 8.192us = 122.0703125kHz
BCM2835_SPI_CLOCK_DIVIDER_1024  = 1024    # 1024 = 4.096us = 244.140625kHz
BCM2835_SPI_CLOCK_DIVIDER_512   = 512     # 512 = 2.048us = 488.28125kHz
BCM2835_SPI_CLOCK_DIVIDER_256   = 256     # 256 = 1.024us = 976.5625MHz
BCM2835_SPI_CLOCK_DIVIDER_128   = 128     # 128 = 512ns = = 1.953125MHz
BCM2835_SPI_CLOCK_DIVIDER_64    = 64      # 64 = 256ns = 3.90625MHz
BCM2835_SPI_CLOCK_DIVIDER_32    = 32      # 32 = 128ns = 7.8125MHz
BCM2835_SPI_CLOCK_DIVIDER_16    = 16      # 16 = 64ns = 15.625MHz
BCM2835_SPI_CLOCK_DIVIDER_8     = 8       # 8 = 32ns = 31.25MHz
BCM2835_SPI_CLOCK_DIVIDER_4     = 4       # 4 = 16ns = 62.5MHz
BCM2835_SPI_CLOCK_DIVIDER_2     = 2       # 2 = 8ns = 125MHz fastest you can get
BCM2835_SPI_CLOCK_DIVIDER_1     = 1       # 0 = 262.144us = 3.814697260kHz same as 0/65536
  