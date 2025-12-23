# Quick Start Guide

## Running the Application

### Console Mode (Recommended for first-time users)
```bash
python3 osi_simulator.py
```
Then enter your message when prompted, or press Enter for the default message.

### GUI Mode (Visual Interface)
```bash
python3 osi_gui.py
```
Click "Simulate" to see the visualization with tabs for encapsulation, decapsulation, and layer diagram.

### Examples (See Various Use Cases)
```bash
python3 examples.py
```

## What You'll See

### Encapsulation Process (Application → Physical)
1. **Layer 7**: Your message gets HTTP POST headers
2. **Layer 6**: Message is encrypted and encoded to UTF-8
3. **Layer 5**: Session ID is added
4. **Layer 4**: Data split into 10-byte segments with ports and checksums
5. **Layer 3**: IP addresses added (192.168.1.2 → 192.168.1.10)
6. **Layer 2**: MAC addresses added (AA:BB:CC:DD:EE:01 → FF:GG:HH:II:JJ:02)
7. **Layer 1**: Everything converted to binary

### Decapsulation Process (Physical → Application)
The process reverses, removing each layer's additions until your original message is recovered.

## Key Features

✓ **Full OSI Model**: All 7 layers implemented
✓ **Data Integrity**: Original message perfectly recovered
✓ **Visualization**: Both console and GUI options
✓ **Educational**: Clear output showing each layer's processing
✓ **Secure**: Uses cryptographically secure session IDs

## Example Session

```bash
$ python3 osi_simulator.py
================================================================================
OSI MODEL DATA FLOW SIMULATOR
================================================================================

Enter a message to send through the OSI layers: Hello World!

[Shows encapsulation through all 7 layers]
[Shows decapsulation through all 7 layers]

================================================================================
VERIFICATION
================================================================================
Original Message: Hello World!
Decapsulated Message: Hello World!
Match: True
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)
- For GUI: tkinter (usually pre-installed with Python)

## Quick Tips

- **Short messages**: See how even small data goes through all layers
- **Long messages**: Watch data being split into segments
- **Special characters**: Test with symbols, numbers, unicode
- **GUI mode**: Use tabs to compare encapsulation vs decapsulation

Enjoy learning about the OSI model!
