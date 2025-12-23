# OSI_simulatedLayers
Application that simulates the 7 layers of the OSI model

## Overview
This application simulates data flow through all 7 layers of the OSI (Open Systems Interconnection) model, demonstrating both **encapsulation** (top to bottom) and **decapsulation** (bottom to top) processes.

## Features

### Layer-by-Layer Implementation

1. **Layer 7 - Application Layer**: Adds HTTP POST protocol headers
2. **Layer 6 - Presentation Layer**: Encrypts data (XOR encryption) and encodes to UTF-8
3. **Layer 5 - Session Layer**: Adds random Session ID (16 characters)
4. **Layer 4 - Transport Layer**: Splits data into 10-byte segments with port numbers (8080→443) and checksums
5. **Layer 3 - Network Layer**: Adds source IP (192.168.1.2) and destination IP (192.168.1.10)
6. **Layer 2 - Data Link Layer**: Adds MAC addresses (AA:BB:CC:DD:EE:01 → FF:GG:HH:II:JJ:02)
7. **Layer 1 - Physical Layer**: Converts data to binary representation

### Visualization Options

- **Console Mode**: Text-based visualization with detailed layer information
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

You'll be prompted to enter a message. The application will then:
1. Show the encapsulation process through all 7 layers
2. Show the decapsulation process back through the layers
3. Verify that the original message is correctly recovered

Example:
```
Enter a message to send through the OSI layers: Hello, OSI Model!
```

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
1. User enters a message at the Application Layer
2. Each layer adds its own header/processing:
   - Application: HTTP POST header
   - Presentation: Encryption + UTF-8 encoding
   - Session: Session ID
   - Transport: Segmentation + ports + checksums
   - Network: IP addresses
   - Data Link: MAC addresses
   - Physical: Binary conversion

### Decapsulation (Receiving Data)
1. Physical layer converts binary back to bytes
2. Each layer removes its header/processing in reverse order
3. Original message is recovered at the Application Layer

### Verification
The application verifies that the decapsulated message matches the original input, demonstrating the integrity of the OSI model simulation.

## Example Output

### Console Mode
```
================================================================================
ENCAPSULATION PROCESS (Application → Physical)
================================================================================

ENCAPSULATION - Layer 7: Application Layer
--------------------------------------------------------------------------------
HTTP Header: POST /api/message HTTP/1.1...
Message: Hello, OSI Model!

ENCAPSULATION - Layer 6: Presentation Layer
--------------------------------------------------------------------------------
Encoding: UTF-8
Encryption: XOR
Encrypted data length: 123 bytes
First 20 bytes (hex): 5a4f5e5a...

[... continues through all layers ...]

================================================================================
VERIFICATION
================================================================================
Original Message: Hello, OSI Model!
Decapsulated Message: Hello, OSI Model!
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
