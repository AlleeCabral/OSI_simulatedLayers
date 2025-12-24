#!/usr/bin/env python3
"""
Example usage of the OSI Model Simulator
Demonstrates how to use the OSI simulator programmatically
Using MQTT protocol (Mosquitto broker simulation)
"""

from osi_simulator import OSISimulator


def example_basic_usage():
    """Basic usage example"""
    print("="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)
    
    # Create simulator
    simulator = OSISimulator()
    
    # Define message
    message = "Hello from the Application Layer!"
    
    # Encapsulate (sending)
    encapsulated = simulator.encapsulate(message)
    
    # Decapsulate (receiving)
    decapsulated = simulator.decapsulate(encapsulated)
    
    # Verify
    print("\n" + "="*80)
    print("RESULT")
    print("="*80)
    print(f"Original:      {message}")
    print(f"Decapsulated:  {decapsulated}")
    print(f"Success:       {message == decapsulated}")


def example_layer_details():
    """Example showing detailed layer information"""
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Accessing Layer Details")
    print("="*80)
    
    from osi_simulator import (
        ApplicationLayer, PresentationLayer, SessionLayer,
        TransportLayer, NetworkLayer, DataLinkLayer, PhysicalLayer
    )
    
    # Create individual layers
    app_layer = ApplicationLayer()
    pres_layer = PresentationLayer()
    session_layer = SessionLayer()
    trans_layer = TransportLayer()
    net_layer = NetworkLayer()
    link_layer = DataLinkLayer()
    phys_layer = PhysicalLayer()
    
    print("\nLayer Configuration:")
    print(f"  Application: MQTT PUBLISH (Mosquitto broker)")
    print(f"  Presentation: XOR Encryption (key={pres_layer.key}), UTF-8 Encoding")
    print(f"  Transport: Ports {trans_layer.src_port} → {trans_layer.dst_port}, Segment size: {trans_layer.segment_size} bytes")
    print(f"  Network: {net_layer.src_ip} → {net_layer.dst_ip}")
    print(f"  Data Link: {link_layer.src_mac} → {link_layer.dst_mac}")
    print(f"  Physical: Binary conversion")


def example_custom_message():
    """Example with custom messages"""
    print("\n\n" + "="*80)
    print("EXAMPLE 3: Multiple MQTT Messages")
    print("="*80)
    
    messages = [
        "Temperature: 23.5C",
        '{"sensor": "DHT22", "temp": 23.5, "humidity": 45}',
        "Alert",
        "Simulating a longer MQTT message that will be split into multiple segments during transport!"
    ]
    
    for i, message in enumerate(messages, 1):
        simulator = OSISimulator()
        
        print(f"\n--- Message {i}: '{message[:30]}{'...' if len(message) > 30 else ''}' ---")
        
        # Quick test without full output
        import sys
        import io
        
        # Suppress output temporarily
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        encapsulated = simulator.encapsulate(message)
        decapsulated = simulator.decapsulate(encapsulated)
        
        # Restore output
        sys.stdout = old_stdout
        
        # Calculate some statistics
        if 'binary_frames' in encapsulated:
            total_bits = encapsulated['total_bits']
            num_frames = len(encapsulated['binary_frames'])
            print(f"  Total bits transmitted: {total_bits}")
            print(f"  Number of frames: {num_frames}")
            print(f"  Successfully recovered: {message == decapsulated}")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "OSI MODEL SIMULATOR - MQTT PROTOCOL EXAMPLES" + " "*19 + "║")
    print("╚" + "="*78 + "╝")
    
    # Run examples
    example_basic_usage()
    example_layer_details()
    example_custom_message()
    
    print("\n\n" + "="*80)
    print("All examples completed successfully!")
    print("="*80)


if __name__ == "__main__":
    main()
