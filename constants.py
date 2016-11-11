# constants.py
# Contains the constants that other classes and files will use

# Units conversions
MB_TO_BYTES = 1000000		# Convert megabytes to bytes
SEC_TO_MS = 1000 			# Convert seconds to milliseconds

DATA_PKT_SIZE = 1024		# Bytes per data packet
ACK_PKT_SIZE = 64			# Bytes per acknowledgement packet

LINK_BUFFER_UNIDIR_CAPACITY = 50 # The capacity for a link buffer in one direction. Pick a better number plz.

global system_EQ 			# the global event queue struct
global system_analytics		# the global analytics class
