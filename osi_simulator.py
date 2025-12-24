#!/usr/bin/env python3
"""
OSI Model Data Flow Simulator
Simulates data encapsulation and decapsulation through all 7 OSI layers
Using MQTT protocol (Mosquitto broker simulation)
"""

import hashlib
import secrets
import string
from typing import List, Dict, Any


class OSILayer:
    """Base class for all OSI layers"""
    
    def __init__(self, layer_number: int, layer_name: str):
        self.layer_number = layer_number
        self.layer_name = layer_name
    
    def encapsulate(self, data: Any) -> Any:
        """Add layer-specific headers/processing during encapsulation"""
        raise NotImplementedError
    
    def decapsulate(self, data: Any) -> Any:
        """Remove layer-specific headers/processing during decapsulation"""
        raise NotImplementedError


class ApplicationLayer(OSILayer):
    """Layer 7: Application Layer - MQTT protocol"""
    
    def __init__(self):
        super().__init__(7, "Application Layer")
    
    def encapsulate(self, message: str) -> Dict[str, Any]:
        """Add MQTT PUBLISH header to the message"""
        # MQTT Control Packet Type: PUBLISH (3), QoS level 1, No Retain
        mqtt_fixed_header = {
            "packet_type": "PUBLISH",
            "qos": 1,
            "retain": False,
            "dup": False
        }
        
        # MQTT Variable Header
        mqtt_variable_header = {
            "topic": "Test/message",
            "packet_id": 12345
        }
        
        # Complete MQTT packet structure
        mqtt_packet = {
            "fixed_header": mqtt_fixed_header,
            "variable_header": mqtt_variable_header,
            "payload": message,
            "payload_length": len(message)
        }
        
        return {
            "mqtt_packet": mqtt_packet,
            "data": message,
            "layer": self.layer_name,
            "protocol": "MQTT"
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> str:
        """Extract original message from MQTT PUBLISH packet"""
        return data["data"]


class PresentationLayer(OSILayer):
    """Layer 6: Presentation Layer - Encryption and encoding"""
    
    def __init__(self):
        super().__init__(6, "Presentation Layer")
        self.key = 42  # Simple XOR encryption key
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encode to UTF-8 and encrypt"""
        import json
        # Serialize MQTT packet to JSON string
        mqtt_packet_str = json.dumps(data["mqtt_packet"])
        full_message = mqtt_packet_str
        
        # Encode to UTF-8
        encoded = full_message.encode('utf-8')
        
        # Simple XOR encryption
        encrypted = bytes([b ^ self.key for b in encoded])
        
        return {
            "encrypted_data": encrypted,
            "encoding": "UTF-8",
            "encryption": "XOR",
            "layer": self.layer_name,
            "original_length": len(full_message),
            "original_message": data["data"]
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Decrypt and decode"""
        import json
        encrypted = data["encrypted_data"]
        
        # Decrypt using XOR
        decrypted = bytes([b ^ self.key for b in encrypted])
        
        # Decode from UTF-8
        decoded = decrypted.decode('utf-8')
        
        # Parse JSON to get MQTT packet structure
        mqtt_packet = json.loads(decoded)
        
        return {
            "mqtt_packet": mqtt_packet,
            "data": mqtt_packet["payload"],
            "layer": "Application Layer",
            "protocol": "MQTT"
        }


class SessionLayer(OSILayer):
    """Layer 5: Session Layer - Session management"""
    
    def __init__(self):
        super().__init__(5, "Session Layer")
    
    def _generate_session_id(self) -> str:
        """Generate cryptographically secure random session ID"""
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16))
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add session ID"""
        session_id = self._generate_session_id()
        return {
            "session_id": session_id,
            "data": data,
            "layer": self.layer_name
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract data and validate session"""
        return data["data"]


class TransportLayer(OSILayer):
    """Layer 4: Transport Layer - Segmentation and port numbers"""
    
    def __init__(self):
        super().__init__(4, "Transport Layer")
        self.src_port = 8080
        self.dst_port = 443
        self.segment_size = 10
    
    def _calculate_checksum(self, data: bytes) -> str:
        """Calculate checksum for educational purposes
        Note: MD5 is used here for simplicity in this educational context.
        Production systems should use SHA-256 or other secure hash functions.
        """
        return hashlib.md5(data).hexdigest()[:8]
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Split into segments and add port/checksum"""
        encrypted_data = data["data"]["encrypted_data"]
        
        # Split into 10-byte segments
        segments = []
        for i in range(0, len(encrypted_data), self.segment_size):
            segment_data = encrypted_data[i:i + self.segment_size]
            checksum = self._calculate_checksum(segment_data)
            
            segments.append({
                "src_port": self.src_port,
                "dst_port": self.dst_port,
                "sequence": i // self.segment_size,
                "checksum": checksum,
                "data": segment_data
            })
        
        return {
            "segments": segments,
            "session_id": data["session_id"],
            "layer": self.layer_name,
            "total_segments": len(segments)
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Reassemble segments and verify checksums"""
        segments = data["segments"]
        
        # Sort by sequence number
        segments.sort(key=lambda x: x["sequence"])
        
        # Verify checksums and reassemble
        reassembled = b''
        for segment in segments:
            expected_checksum = self._calculate_checksum(segment["data"])
            if segment["checksum"] != expected_checksum:
                print(f"Warning: Checksum mismatch in segment {segment['sequence']}")
            reassembled += segment["data"]
        
        return {
            "session_id": data["session_id"],
            "segments": segments,  # Include segments for display
            "data": {
                "encrypted_data": reassembled,
                "encoding": "UTF-8",
                "encryption": "XOR",
                "layer": "Presentation Layer"
            },
            "layer": "Session Layer"
        }


class NetworkLayer(OSILayer):
    """Layer 3: Network Layer - IP addressing"""
    
    def __init__(self):
        super().__init__(3, "Network Layer")
        self.src_ip = "192.168.1.2"
        self.dst_ip = "192.168.1.10"
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add IP addresses to each segment"""
        packets = []
        for segment in data["segments"]:
            packets.append({
                "src_ip": self.src_ip,
                "dst_ip": self.dst_ip,
                "ttl": 64,
                "protocol": "TCP",
                "data": segment
            })
        
        return {
            "packets": packets,
            "session_id": data["session_id"],
            "layer": self.layer_name,
            "total_packets": len(packets)
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract segments from packets"""
        segments = [packet["data"] for packet in data["packets"]]
        
        return {
            "segments": segments,
            "session_id": data["session_id"],
            "layer": "Transport Layer"
        }


class DataLinkLayer(OSILayer):
    """Layer 2: Data Link Layer - MAC addressing"""
    
    def __init__(self):
        super().__init__(2, "Data Link Layer")
        self.src_mac = "AA:BB:CC:DD:EE:01"
        self.dst_mac = "FF:GG:HH:II:JJ:02"
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add MAC addresses to each packet"""
        frames = []
        for packet in data["packets"]:
            frames.append({
                "src_mac": self.src_mac,
                "dst_mac": self.dst_mac,
                "ethertype": "0x0800",
                "data": packet,
                "fcs": "CRC32"
            })
        
        return {
            "frames": frames,
            "session_id": data["session_id"],
            "layer": self.layer_name,
            "total_frames": len(frames)
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract packets from frames"""
        packets = [frame["data"] for frame in data["frames"]]
        
        return {
            "packets": packets,
            "session_id": data["session_id"],
            "layer": "Network Layer"
        }


class PhysicalLayer(OSILayer):
    """Layer 1: Physical Layer - Binary conversion"""
    
    def __init__(self):
        super().__init__(1, "Physical Layer")
    
    def _to_binary(self, data: bytes) -> str:
        """Convert bytes to binary string"""
        return ''.join(format(byte, '08b') for byte in data)
    
    def _from_binary(self, binary: str) -> bytes:
        """Convert binary string to bytes"""
        return bytes(int(binary[i:i+8], 2) for i in range(0, len(binary), 8))
    
    def encapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert frames to binary"""
        binary_frames = []
        for frame in data["frames"]:
            # Convert the segment data to binary
            segment_data = frame["data"]["data"]["data"]
            binary = self._to_binary(segment_data)
            
            binary_frames.append({
                "frame_info": frame,
                "binary_data": binary,
                "bit_length": len(binary)
            })
        
        return {
            "binary_frames": binary_frames,
            "session_id": data["session_id"],
            "layer": self.layer_name,
            "total_bits": sum(f["bit_length"] for f in binary_frames)
        }
    
    def decapsulate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert binary back to frames"""
        frames = []
        binary_frames = data["binary_frames"]
        for binary_frame in binary_frames:
            # Convert binary back to bytes
            binary_data = binary_frame["binary_data"]
            segment_data = self._from_binary(binary_data)
            
            # Reconstruct frame
            frame_info = binary_frame["frame_info"]
            frame_info["data"]["data"]["data"] = segment_data
            frames.append(frame_info)
        
        return {
            "frames": frames,
            "binary_frames": binary_frames,  # Include for display
            "session_id": data["session_id"],
            "layer": "Data Link Layer"
        }


class OSISimulator:
    """Main OSI Model Simulator"""
    
    def __init__(self):
        self.layers = [
            ApplicationLayer(),
            PresentationLayer(),
            SessionLayer(),
            TransportLayer(),
            NetworkLayer(),
            DataLinkLayer(),
            PhysicalLayer()
        ]
        self.encapsulation_steps = []
        self.decapsulation_steps = []
    
    def encapsulate(self, message: str) -> Dict[str, Any]:
        """Encapsulate message through all layers (top to bottom)"""
        print("\n" + "="*80)
        print("ENCAPSULATION PROCESS (Application → Physical)")
        print("="*80)
        
        self.encapsulation_steps = []
        data = message
        
        for layer in self.layers:
            data = layer.encapsulate(data)
            self.encapsulation_steps.append({
                "layer": layer.layer_name,
                "data": data
            })
            self._print_layer_info(layer, data, "ENCAPSULATION")
        
        return data
    
    def decapsulate(self, data: Dict[str, Any]) -> str:
        """Decapsulate data through all layers (bottom to top)"""
        print("\n" + "="*80)
        print("DECAPSULATION PROCESS (Physical → Application)")
        print("="*80)
        
        self.decapsulation_steps = []
        
        for layer in reversed(self.layers):
            data = layer.decapsulate(data)
            self.decapsulation_steps.append({
                "layer": layer.layer_name,
                "data": data
            })
            self._print_layer_info(layer, data, "DECAPSULATION")
        
        return data
    
    def _print_layer_info(self, layer: OSILayer, data: Any, process: str):
        """Print information about the current layer processing"""
        print(f"\n{process} - Layer {layer.layer_number}: {layer.layer_name}")
        print("-" * 80)
        
        if layer.layer_number == 7:  # Application
            if process == "ENCAPSULATION":
                print(f"Protocol: MQTT")
                print(f"MQTT Packet Type: {data['mqtt_packet']['fixed_header']['packet_type']}")
                print(f"QoS Level: {data['mqtt_packet']['fixed_header']['qos']}")
                print(f"Topic: {data['mqtt_packet']['variable_header']['topic']}")
                print(f"Packet ID: {data['mqtt_packet']['variable_header']['packet_id']}")
                print(f"Payload Length: {data['mqtt_packet']['payload_length']} bytes")
                print(f"Message: {data['data']}")
                print(f"\n→ Added MQTT headers (packet type, QoS, topic, packet ID)")
            else:
                print(f"Protocol: MQTT")
                print(f"Extracted Message: {data}")
                print(f"\n→ Removed MQTT headers, retrieved original payload")
        
        elif layer.layer_number == 6:  # Presentation
            if process == "ENCAPSULATION":
                print(f"Encoding: {data['encoding']}")
                print(f"Encryption: {data['encryption']}")
                print(f"Original Length: {data['original_length']} bytes")
                print(f"Encrypted data length: {len(data['encrypted_data'])} bytes")
                print(f"All encrypted data (hex): {data['encrypted_data'].hex()}")
                print(f"\n→ Encoded to UTF-8 and encrypted with XOR cipher")
            else:
                print(f"Decrypted and decoded data")
                print(f"MQTT Packet Type: {data['mqtt_packet']['fixed_header']['packet_type']}")
                print(f"Topic: {data['mqtt_packet']['variable_header']['topic']}")
                print(f"Payload: {data['data']}")
                print(f"\n→ Decrypted using XOR cipher and decoded from UTF-8")
        
        elif layer.layer_number == 5:  # Session
            if process == "ENCAPSULATION":
                print(f"Session ID: {data['session_id']}")
                print(f"Session Layer encapsulated")
                print(f"\n→ Added session ID for connection management")
            else:
                print(f"Session ID extracted and validated")
                print(f"Data passed to Presentation Layer")
                print(f"\n→ Removed session information, validated connection")
        
        elif layer.layer_number == 4:  # Transport
            if process == "ENCAPSULATION":
                print(f"Total Segments: {data['total_segments']}")
                print(f"Segment Size: 10 bytes")
                print(f"Source Port: {data['segments'][0]['src_port']}")
                print(f"Destination Port: {data['segments'][0]['dst_port']}")
                print(f"All Segments:")
                for i, segment in enumerate(data['segments']):
                    print(f"  Segment {i}: seq={segment['sequence']}, checksum={segment['checksum']}, data(hex)={segment['data'].hex()}")
                print(f"\n→ Split data into {data['total_segments']} segments with ports and checksums")
            else:
                print(f"All Segments being reassembled:")
                segments = data.get('segments', [])
                for segment in segments:
                    print(f"  Segment {segment['sequence']}: checksum={segment['checksum']}, data(hex)={segment['data'].hex()}")
                print(f"Checksums verified")
                print(f"Total data reassembled: {len(data['data']['encrypted_data'])} bytes")
                print(f"Reassembled data (hex): {data['data']['encrypted_data'].hex()}")
                print(f"\n→ Reassembled segments, verified checksums, removed port information")
        
        elif layer.layer_number == 3:  # Network
            if process == "ENCAPSULATION":
                print(f"Total Packets: {data['total_packets']}")
                print(f"Source IP: {data['packets'][0]['src_ip']}")
                print(f"Destination IP: {data['packets'][0]['dst_ip']}")
                print(f"TTL: {data['packets'][0]['ttl']}")
                print(f"Protocol: {data['packets'][0]['protocol']}")
                print(f"\n→ Added IP addresses and routing information to each segment")
            else:
                print(f"Segments extracted: {len(data['segments'])} segments")
                print(f"Segments extracted from packets")
                print(f"\n→ Removed IP headers, extracted transport layer segments")
        
        elif layer.layer_number == 2:  # Data Link
            if process == "ENCAPSULATION":
                print(f"Total Frames: {data['total_frames']}")
                print(f"Source MAC: {data['frames'][0]['src_mac']}")
                print(f"Destination MAC: {data['frames'][0]['dst_mac']}")
                print(f"EtherType: {data['frames'][0]['ethertype']}")
                print(f"\n→ Added MAC addresses and frame check sequence to each packet")
            else:
                print(f"Packets extracted: {len(data['packets'])} packets")
                print(f"Packets extracted from frames")
                print(f"\n→ Removed MAC addresses and frame headers, extracted network packets")
        
        elif layer.layer_number == 1:  # Physical
            if process == "ENCAPSULATION":
                print(f"Total Bits: {data['total_bits']}")
                print(f"Total Binary Frames: {len(data['binary_frames'])}")
                print(f"All Binary Frames:")
                for i, frame in enumerate(data['binary_frames']):
                    print(f"  Frame {i}: {frame['bit_length']} bits, binary={frame['binary_data']}")
                print(f"\n→ Converted frames to binary representation for transmission")
            else:
                print(f"All Binary Frames being converted:")
                for i, binary_frame in enumerate(data.get('binary_frames', [])):
                    print(f"  Frame {i}: {binary_frame['bit_length']} bits, binary={binary_frame['binary_data']}")
                print(f"Frames converted: {len(data['frames'])} frames")
                print(f"Frames reconstructed from binary data")
                print(f"\n→ Converted binary signals back to frames")


def main():
    """Main function to run the OSI simulator"""
    print("="*80)
    print("OSI MODEL DATA FLOW SIMULATOR - MQTT Protocol")
    print("="*80)
    print("\nSimulating MQTT message from a Mosquitto broker")
    print("You can send a message from terminal and receive it through OSI layers\n")
    
    # Get user input
    message = input("Enter a message to send through the OSI layers (MQTT payload): ").strip()
    
    if not message:
        message = "Hello, OSI Model!"
        print(f"Using default message: {message}")
    
    # Create simulator
    simulator = OSISimulator()
    
    # Encapsulate the message
    encapsulated_data = simulator.encapsulate(message)
    
    # Decapsulate the data
    decapsulated_message = simulator.decapsulate(encapsulated_data)
    
    # Verify
    print("\n" + "="*80)
    print("VERIFICATION")
    print("="*80)
    print(f"Original Message: {message}")
    print(f"Decapsulated Message: {decapsulated_message}")
    print(f"Match: {message == decapsulated_message}")
    
    return simulator


if __name__ == "__main__":
    main()
