# Quick Start Guide

## Running the Application

### Console Mode (Recommended for first-time users)
```bash
python3 osi_simulator.py
```
Then enter your MQTT message when prompted, or press Enter for the default message.

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
1. **Layer 7**: Your message gets MQTT PUBLISH packet headers (packet type, QoS, topic, packet ID)
2. **Layer 6**: Message is encrypted and encoded to UTF-8
3. **Layer 5**: Session ID is added
4. **Layer 4**: Data split into 10-byte segments with ports and checksums
5. **Layer 3**: IP addresses added (192.168.1.2 → 192.168.1.10)
6. **Layer 2**: MAC addresses added (AA:BB:CC:DD:EE:01 → FF:GG:HH:II:JJ:02)
7. **Layer 1**: Everything converted to binary

### Decapsulation Process (Physical → Application)
The process reverses, removing each layer's additions until your original MQTT message is recovered.
**Each layer now shows detailed information about:**
- What headers/information are being removed
- How the data is being transformed
- The extracted information at each step

## Key Features

✓ **Full OSI Model**: All 7 layers implemented
✓ **MQTT Protocol**: Simulates messages from Mosquitto broker
✓ **Data Integrity**: Original message perfectly recovered
✓ **Detailed Logging**: Shows encapsulation AND decapsulation with full details
✓ **Visualization**: Both console and GUI options
✓ **Educational**: Clear output showing each layer's processing and transformation
✓ **Secure**: Uses cryptographically secure session IDs

## Example Session

```bash
$ python3 osi_simulator.py
================================================================================
OSI MODEL DATA FLOW SIMULATOR - MQTT Protocol
================================================================================

Simulating MQTT message from a Mosquitto broker
You can send a message from terminal and receive it through OSI layers

Enter a message to send through the OSI layers (MQTT payload): Temperature: 23.5C

[Shows detailed encapsulation through all 7 layers]
[Shows detailed decapsulation through all 7 layers with transformation info]

================================================================================
VERIFICATION
================================================================================
Original Message: Temperature: 23.5C
Decapsulated Message: Temperature: 23.5C
Match: True
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)
- For GUI: tkinter (usually pre-installed with Python)

## Quick Tips

- **IoT messages**: Try sensor data like "Temperature: 23.5C" or "Humidity: 45%"
- **JSON payloads**: Test with JSON like '{"sensor": "DHT22", "temp": 23.5}'
- **Short messages**: See how even small data goes through all layers
- **Long messages**: Watch data being split into segments
- **Special characters**: Test with symbols, numbers, unicode
- **GUI mode**: Use tabs to compare encapsulation vs decapsulation details

Enjoy learning about the OSI model with MQTT protocol!
