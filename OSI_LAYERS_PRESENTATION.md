# OSI Model Layer-by-Layer Presentation
## MQTT Protocol Data Flow Simulation

---

## Slide 1: Title & Overview

### OSI Model: Understanding Data Flow Through 7 Layers
**MQTT Protocol Simulation**

**What We'll Cover:**
- How each layer processes data during encapsulation (sending)
- How each layer processes data during decapsulation (receiving)
- Real-world example using MQTT protocol

**Duration:** 5-10 minutes

---

## Slide 2: Introduction - The OSI Model

### What is the OSI Model?
The **Open Systems Interconnection (OSI) Model** is a conceptual framework that standardizes network communication into 7 distinct layers.

**Two Main Processes:**
- **Encapsulation**: Adding headers as data moves DOWN the layers (Application → Physical)
- **Decapsulation**: Removing headers as data moves UP the layers (Physical → Application)

**Our Example:** Simulating an MQTT message from a Mosquitto broker through all 7 layers

---

## Slide 3: Layer 7 - Application Layer

### Layer 7: Application Layer (MQTT Protocol)

**INPUT:**
- User message (plain text): `"Temperature: 23.5C"`

**PROCESSING:**
- Adds MQTT PUBLISH packet structure
- Creates fixed header: packet type, QoS level, retain flag
- Creates variable header: topic name, packet ID
- Packages user message as MQTT payload

**OUTPUT:**
```
MQTT Packet:
- Type: PUBLISH
- QoS: 1
- Topic: Test/message
- Packet ID: 12345
- Payload: "Temperature: 23.5C"
```

**Key Point:** This layer handles the application-specific protocol (MQTT) and prepares data for transmission.

---

## Slide 4: Layer 6 - Presentation Layer

### Layer 6: Presentation Layer (Data Translation & Encryption)

**INPUT:**
- MQTT packet structure (JSON format)

**PROCESSING:**
- **Serialization**: Converts MQTT packet to JSON string
- **Encoding**: Applies UTF-8 character encoding
- **Encryption**: Uses XOR cipher (key=42) for data security
- Result: Encrypted byte array

**OUTPUT:**
- Encrypted and encoded data
- Example: `5a4f5e5a...` (hex representation)
- Length: ~212 bytes (varies with message size)

**Key Point:** This layer handles data format translation, encoding, and encryption for secure transmission.

---

## Slide 5: Layer 5 - Session Layer

### Layer 5: Session Layer (Session Management)

**INPUT:**
- Encrypted data from Presentation Layer

**PROCESSING:**
- Generates unique Session ID (16 characters, alphanumeric)
- Uses cryptographically secure random number generator
- Prepends Session ID to the data
- Example Session ID: `A7k9Xp2Qr4Wn8Zm5`

**OUTPUT:**
- Data with Session ID header
- Format: `[Session ID][Encrypted Data]`

**Key Point:** This layer establishes and manages the communication session, ensuring proper connection tracking.

---

## Slide 6: Layer 4 - Transport Layer

### Layer 4: Transport Layer (Segmentation & Ports)

**INPUT:**
- Session data from Layer 5

**PROCESSING:**
- **Segmentation**: Splits data into 10-byte chunks (MTU simulation)
- Adds transport metadata to each segment:
  - Source Port: 8080
  - Destination Port: 443
  - Sequence number (0, 1, 2, ...)
  - Total segments count
- **Checksum**: Generates MD5 hash (8 chars) for each segment for integrity

**OUTPUT:**
```
Segments:
- Segment 0: [10 bytes] + metadata + checksum
- Segment 1: [10 bytes] + metadata + checksum
- Segment N: [remaining bytes] + metadata + checksum
```

**Key Point:** This layer ensures reliable data transfer through segmentation and error checking.

---

## Slide 7: Layer 3 - Network Layer

### Layer 3: Network Layer (Routing & IP Addressing)

**INPUT:**
- Multiple segments from Transport Layer

**PROCESSING:**
- Adds IP addressing to each segment/packet
- **Source IP**: 192.168.1.2
- **Destination IP**: 192.168.1.10
- Simulates packet routing information

**OUTPUT:**
```
IP Packets (one per segment):
- Packet with IP headers:
  Source: 192.168.1.2
  Destination: 192.168.1.10
  Data: [Transport segment]
```

**Key Point:** This layer handles logical addressing and routing, determining the path data takes across networks.

---

## Slide 8: Layer 2 - Data Link Layer

### Layer 2: Data Link Layer (MAC Addressing & Frame Creation)

**INPUT:**
- IP packets from Network Layer

**PROCESSING:**
- Adds MAC (Media Access Control) addresses for physical device identification
- **Source MAC**: AA:BB:CC:DD:EE:01
- **Destination MAC**: FF:GG:HH:II:JJ:02
- Creates frames ready for physical transmission

**OUTPUT:**
```
Frames (one per packet):
- Frame with MAC headers:
  Source MAC: AA:BB:CC:DD:EE:01
  Dest MAC: FF:GG:HH:II:JJ:02
  Data: [IP packet]
```

**Key Point:** This layer provides node-to-node data transfer and handles physical addressing on the local network.

---

## Slide 9: Layer 1 - Physical Layer

### Layer 1: Physical Layer (Binary Transmission)

**INPUT:**
- Frames from Data Link Layer

**PROCESSING:**
- Converts each byte to 8-bit binary representation
- Simulates physical signal transmission
- Example: 'A' (0x41) → `01000001`

**OUTPUT:**
- Binary data stream
- Example: `01000001 01000010 01000011...`
- Ready for transmission over physical medium (cable, wireless, etc.)

**Key Point:** This layer handles the actual physical transmission of raw bits over the communication medium.

---

## Slide 10: Decapsulation Process (Receiving Side)

### Decapsulation: Reversing the Process

When data is received, the process reverses (Physical → Application):

**Layer 1 (Physical):** Binary → Bytes → Frames
**Layer 2 (Data Link):** Removes MAC addresses → Packets
**Layer 3 (Network):** Removes IP addresses → Segments  
**Layer 4 (Transport):** Reassembles segments (verifies checksums) → Session data
**Layer 5 (Session):** Removes Session ID → Encrypted data
**Layer 6 (Presentation):** Decrypts & decodes → MQTT packet
**Layer 7 (Application):** Extracts payload → Original message

**Result:** `"Temperature: 23.5C"` ✓

---

## Slide 11: Verification & Summary

### Data Integrity Verification

**Original Message:** `"Temperature: 23.5C"`
**After Encapsulation:** Passed through 7 layers
**After Decapsulation:** `"Temperature: 23.5C"`
**Match:** ✓ **SUCCESS**

### Key Takeaways:

1. **Encapsulation:** Each layer adds its header/processing (wrapping data)
2. **Decapsulation:** Each layer removes its header/processing (unwrapping data)
3. **Layer Independence:** Each layer has a specific function
4. **Protocol Hierarchy:** Higher layers depend on lower layers
5. **Real-World Application:** MQTT protocol demonstrates practical OSI model usage in IoT

### Benefits of Layered Architecture:
- **Modularity:** Changes in one layer don't affect others
- **Standardization:** Different vendors can interoperate
- **Troubleshooting:** Easier to isolate problems to specific layers

---

## Slide 12: Questions & Demo

### Try It Yourself!

**Console Mode:**
```bash
python3 osi_simulator.py
```

**GUI Mode:**
```bash
python3 osi_gui.py
```

**What You'll See:**
- Complete encapsulation process with detailed layer information
- Complete decapsulation process showing data reconstruction
- Verification that original message is recovered correctly

### Questions?

Thank you for your attention!

---

## Additional Resources

- **Repository:** github.com/AlleeCabral/OSI_simulatedLayers
- **MQTT Protocol:** mqtt.org
- **OSI Model:** ISO/IEC 7498-1 standard

**Note:** This simulation uses simplified versions of protocols for educational purposes. Real-world implementations are more complex and include additional security, error handling, and optimization features.
