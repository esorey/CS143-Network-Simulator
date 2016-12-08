# constants.py
# Contains the constants that other classes and files will use
testcase = 2                # Chose which test case to run

cngstn_ctrl = 2             # Choose which congestion control algorithm to run
NO_CNGSTN_CTRL = 0
TCP_RENO = 1
FAST_TCP = 2

# Unit Conversions
MB_TO_BYTES = 1000000.0     # Multiplier to convert MB to bytes
KB_TO_BYTES = 1000.0        # Multiplier to convert KB to bytes 
BYTES_TO_MBITS = 0.000008   # Multiplier to convert bytes to megabits
SEC_TO_MS = 1000.0          # Multiplier to convert seconds to milliseconds
MS_TO_SEC = 0.001           # Multiplier to convert milliseconds to seconds

# Packet Sizes
DATA_PKT_SIZE = 1024.0      # Bytes per data packet
ACK_PKT_SIZE = 64.0         # Bytes per acknowledgement packet
RTABLE_PKT_SIZE = 64.0      # Bytes per routing table packet

# Time Delays
CONSECUTIVE_PKT_DELAY = 0.5     # Send new packets every 0.5 ms when sending consecutive packets
TIMEOUT_TIME = 1000             # Default packet timeout time, otherwise use avg RTT 
FAST_PERIOD = 100                # Time to update window size for Fast TCP
BELLMAN_PERIOD = 5000           # Time between each bellman ford event enqueued in ms

# Other
DEFAULT_NUM_WINDOWS = 1000      # Default window size for windowed averages
DEC_PLACES = 2

# Global Variables
global system_EQ            # the global event queue struct
global system_analytics     # the global analytics class

global Bellman_not_done     # Determines if bellman ford is done running
global debug                # When debugging
global all_flows_done       # Indicates if all flows are completed
global bellman_ford         # If we are running bellman ford

debug = False
bellman_ford = True
