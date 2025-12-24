# OSI_simulatedLayers
Application that simulates the 7 layers of the OSI model using MQTT protocol

## Overview
This application simulates data flow through all 7 layers of the OSI (Open Systems Interconnection) model, demonstrating both **encapsulation** (top to bottom) and **decapsulation** (bottom to top) processes. The simulator uses **MQTT protocol** (simulating messages from a Mosquitto broker) to show realistic IoT/messaging scenarios.

## Features

### Layer-by-Layer Implementation

1. **Layer 7 - Application Layer**: Adds MQTT PUBLISH packet headers (packet type, QoS, topic, packet ID)
2. **Layer 6 - Presentation Layer**: Encrypts data (XOR encryption) and encodes to UTF-8
3. **Layer 5 - Session Layer**: Adds random Session ID (16 characters)
4. **Layer 4 - Transport Layer**: Splits data into 10-byte segments with port numbers (8080→443) and checksums
5. **Layer 3 - Network Layer**: Adds source IP (192.168.1.2) and destination IP (192.168.1.10)
6. **Layer 2 - Data Link Layer**: Adds MAC addresses (AA:BB:CC:DD:EE:01 → FF:GG:HH:II:JJ:02)
7. **Layer 1 - Physical Layer**: Converts data to binary representation

### Visualization Options

- **Console Mode**: Text-based visualization with detailed layer information for both encapsulation and decapsulation
- **GUI Mode**: Graphical interface with tabs for encapsulation, decapsulation, and visual layer diagram

## Installation

### Requirements
- Python 3.6 or higher
- tkinter (usually included with Python)

### Setup
No additional packages required. The application uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/AlleeCabral/OSI_simulatedLayers.git
cd OSI_simulatedLayers
```

## Usage

### Console Mode

Run the console version for text-based output:

```bash
python3 osi_simulator.py
```

You'll be prompted to enter a message (MQTT payload). The application will then:
1. Show the encapsulation process through all 7 layers with detailed information
2. Show the decapsulation process back through the layers with detailed information about what's being removed
3. Verify that the original message is correctly recovered

Example:
```
Enter a message to send through the OSI layers (MQTT payload): Temperature: 23.5C
```

The simulator shows how MQTT messages from a Mosquitto broker would be processed through the OSI layers.

### GUI Mode

Run the GUI version for graphical visualization:

```bash
python3 osi_gui.py
```

The GUI provides:
- Input field for your message
- Three tabs:
  - **Encapsulation Flow**: Shows data moving down through layers
  - **Decapsulation Flow**: Shows data moving up through layers
  - **Layer Visualization**: Visual diagram of all 7 OSI layers

## How It Works

### Encapsulation (Sending Data)
1. User enters a message at the Application Layer (MQTT payload)
2. Each layer adds its own header/processing:
   - Application: MQTT PUBLISH packet (packet type, QoS, topic, packet ID)
   - Presentation: Encryption + UTF-8 encoding
   - Session: Session ID
   - Transport: Segmentation + ports + checksums
   - Network: IP addresses
   - Data Link: MAC addresses
   - Physical: Binary conversion

### Decapsulation (Receiving Data)
1. Physical layer converts binary back to bytes
2. Each layer removes its header/processing in reverse order, showing:
   - What information is being removed
   - How the data is being transformed back
   - Details about the extracted information
3. Original MQTT message is recovered at the Application Layer

### Verification
The application verifies that the decapsulated message matches the original input, demonstrating the integrity of the OSI model simulation.

## Example Output

### Console Mode
```
================================================================================
OSI MODEL DATA FLOW SIMULATOR - MQTT Protocol
================================================================================

Simulating MQTT message from a Mosquitto broker
You can send a message from terminal and receive it through OSI layers

Enter a message to send through the OSI layers (MQTT payload): Temperature: 23.5C

================================================================================
ENCAPSULATION PROCESS (Application → Physical)
================================================================================

ENCAPSULATION - Layer 7: Application Layer
--------------------------------------------------------------------------------
Protocol: MQTT
MQTT Packet Type: PUBLISH
QoS Level: 1
Topic: sensor/temperature
Packet ID: 12345
Payload Length: 18 bytes
Message: Temperature: 23.5C

→ Added MQTT headers (packet type, QoS, topic, packet ID)

ENCAPSULATION - Layer 6: Presentation Layer
--------------------------------------------------------------------------------
Encoding: UTF-8
Encryption: XOR
Encrypted data length: 212 bytes
First 20 bytes (hex): 5a4f5e5a...

→ Encoded to UTF-8 and encrypted with XOR cipher

[... continues through all layers ...]

================================================================================
DECAPSULATION PROCESS (Physical → Application)
================================================================================

DECAPSULATION - Layer 1: Physical Layer
--------------------------------------------------------------------------------
Frames converted: 22 frames
Frames reconstructed from binary data

→ Converted binary signals back to frames

[... continues through all layers with detailed decapsulation info ...]

================================================================================
VERIFICATION
================================================================================
Original Message: Temperature: 23.5C
Decapsulated Message: Temperature: 23.5C
Match: True
```

## Technical Details

- **Encryption**: Simple XOR encryption (key=42) for demonstration purposes only (not for production use)
- **Segmentation**: 10-byte segments in Transport Layer
- **Checksum**: MD5 hash (first 8 characters) for segment verification in this educational context
- **Session ID**: Cryptographically secure random 16-character alphanumeric string
- **Binary**: Standard 8-bit binary representation

**Note**: This is an educational project. The encryption and hashing methods used here are for demonstration purposes to understand OSI layer concepts, not for production security systems.

## Project Structure

```
OSI_simulatedLayers/
├── README.md              # This file
├── osi_simulator.py       # Console version with core OSI logic
├── osi_gui.py            # GUI version with tkinter interface
├── examples.py           # Example usage and demonstrations
└── .gitignore            # Git ignore configuration
```

## Contributing

Feel free to submit issues or pull requests to improve the simulation or add features.

## License

This project is open source and available for educational purposes.
