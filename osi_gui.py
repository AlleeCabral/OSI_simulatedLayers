#!/usr/bin/env python3
"""
OSI Model Data Flow Simulator - GUI Version
Graphical visualization of OSI layer encapsulation and decapsulation
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import time
from osi_simulator import OSISimulator


class OSISimulatorGUI:
    """GUI for OSI Model Simulator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("OSI Model Data Flow Simulator")
        self.root.geometry("1200x800")
        
        # Create simulator instance
        self.simulator = OSISimulator()
        
        # Setup GUI
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI layout"""
        # Title
        title_label = tk.Label(
            self.root,
            text="OSI Model Data Flow Simulator",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Input frame
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill=tk.X, padx=10)
        
        tk.Label(input_frame, text="Enter Message:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        self.message_entry = tk.Entry(input_frame, font=("Arial", 12), width=50)
        self.message_entry.pack(side=tk.LEFT, padx=5)
        self.message_entry.insert(0, "Hello, OSI Model!")
        
        self.simulate_btn = tk.Button(
            input_frame,
            text="Simulate",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            command=self.run_simulation
        )
        self.simulate_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            input_frame,
            text="Clear",
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            command=self.clear_output
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Encapsulation tab
        self.encap_frame = tk.Frame(self.notebook)
        self.notebook.add(self.encap_frame, text="Encapsulation Flow")
        
        self.encap_text = scrolledtext.ScrolledText(
            self.encap_frame,
            font=("Courier", 10),
            wrap=tk.WORD,
            bg="#ecf0f1"
        )
        self.encap_text.pack(fill=tk.BOTH, expand=True)
        
        # Decapsulation tab
        self.decap_frame = tk.Frame(self.notebook)
        self.notebook.add(self.decap_frame, text="Decapsulation Flow")
        
        self.decap_text = scrolledtext.ScrolledText(
            self.decap_frame,
            font=("Courier", 10),
            wrap=tk.WORD,
            bg="#ecf0f1"
        )
        self.decap_text.pack(fill=tk.BOTH, expand=True)
        
        # Visualization tab
        self.viz_frame = tk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Layer Visualization")
        
        # Canvas for visualization
        self.viz_canvas = tk.Canvas(self.viz_frame, bg="white")
        self.viz_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            font=("Arial", 10),
            bg="#34495e",
            fg="white",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def run_simulation(self):
        """Run the OSI simulation"""
        message = self.message_entry.get().strip()
        
        if not message:
            messagebox.showwarning("Input Required", "Please enter a message to simulate!")
            return
        
        # Disable button during simulation
        self.simulate_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Simulating...")
        
        # Run simulation in thread to keep GUI responsive
        thread = threading.Thread(target=self._simulate, args=(message,))
        thread.start()
    
    def _simulate(self, message):
        """Internal simulation method"""
        try:
            # Clear previous output
            self.encap_text.delete(1.0, tk.END)
            self.decap_text.delete(1.0, tk.END)
            
            # Encapsulation
            self.encap_text.insert(tk.END, "="*80 + "\n")
            self.encap_text.insert(tk.END, "ENCAPSULATION PROCESS (Application → Physical)\n")
            self.encap_text.insert(tk.END, "="*80 + "\n\n")
            
            encapsulated_data = self._encapsulate_with_display(message)
            
            # Small delay for visualization
            time.sleep(0.5)
            
            # Decapsulation
            self.decap_text.insert(tk.END, "="*80 + "\n")
            self.decap_text.insert(tk.END, "DECAPSULATION PROCESS (Physical → Application)\n")
            self.decap_text.insert(tk.END, "="*80 + "\n\n")
            
            decapsulated_message = self._decapsulate_with_display(encapsulated_data)
            
            # Verification
            self.encap_text.insert(tk.END, "\n" + "="*80 + "\n")
            self.encap_text.insert(tk.END, "VERIFICATION\n")
            self.encap_text.insert(tk.END, "="*80 + "\n")
            self.encap_text.insert(tk.END, f"Original Message: {message}\n")
            self.encap_text.insert(tk.END, f"Decapsulated Message: {decapsulated_message}\n")
            self.encap_text.insert(tk.END, f"Match: {message == decapsulated_message}\n")
            
            # Draw visualization
            self.draw_visualization()
            
            self.status_label.config(text="Simulation complete!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Simulation error: {str(e)}")
            self.status_label.config(text="Error occurred!")
        
        finally:
            self.simulate_btn.config(state=tk.NORMAL)
    
    def _encapsulate_with_display(self, message):
        """Encapsulate and display each layer"""
        data = message
        
        for layer in self.simulator.layers:
            data = layer.encapsulate(data)
            self._display_layer_encapsulation(layer, data)
        
        return data
    
    def _decapsulate_with_display(self, data):
        """Decapsulate and display each layer"""
        for layer in reversed(self.simulator.layers):
            data = layer.decapsulate(data)
            self._display_layer_decapsulation(layer, data)
        
        return data
    
    def _display_layer_encapsulation(self, layer, data):
        """Display layer information during encapsulation"""
        self.encap_text.insert(tk.END, f"Layer {layer.layer_number}: {layer.layer_name}\n")
        self.encap_text.insert(tk.END, "-" * 80 + "\n")
        
        if layer.layer_number == 7:  # Application
            self.encap_text.insert(tk.END, f"HTTP Header: {data['header'][:50]}...\n")
            self.encap_text.insert(tk.END, f"Message: {data['data']}\n")
        
        elif layer.layer_number == 6:  # Presentation
            self.encap_text.insert(tk.END, f"Encoding: {data['encoding']}\n")
            self.encap_text.insert(tk.END, f"Encryption: {data['encryption']}\n")
            self.encap_text.insert(tk.END, f"Encrypted data length: {len(data['encrypted_data'])} bytes\n")
            self.encap_text.insert(tk.END, f"First 20 bytes (hex): {data['encrypted_data'][:20].hex()}\n")
        
        elif layer.layer_number == 5:  # Session
            self.encap_text.insert(tk.END, f"Session ID: {data['session_id']}\n")
        
        elif layer.layer_number == 4:  # Transport
            self.encap_text.insert(tk.END, f"Total Segments: {data['total_segments']}\n")
            self.encap_text.insert(tk.END, f"Segment Size: 10 bytes\n")
            self.encap_text.insert(tk.END, f"Source Port: {data['segments'][0]['src_port']}\n")
            self.encap_text.insert(tk.END, f"Destination Port: {data['segments'][0]['dst_port']}\n")
            if data['segments']:
                self.encap_text.insert(tk.END, f"First Segment Checksum: {data['segments'][0]['checksum']}\n")
        
        elif layer.layer_number == 3:  # Network
            self.encap_text.insert(tk.END, f"Total Packets: {data['total_packets']}\n")
            self.encap_text.insert(tk.END, f"Source IP: {data['packets'][0]['src_ip']}\n")
            self.encap_text.insert(tk.END, f"Destination IP: {data['packets'][0]['dst_ip']}\n")
            self.encap_text.insert(tk.END, f"TTL: {data['packets'][0]['ttl']}\n")
            self.encap_text.insert(tk.END, f"Protocol: {data['packets'][0]['protocol']}\n")
        
        elif layer.layer_number == 2:  # Data Link
            self.encap_text.insert(tk.END, f"Total Frames: {data['total_frames']}\n")
            self.encap_text.insert(tk.END, f"Source MAC: {data['frames'][0]['src_mac']}\n")
            self.encap_text.insert(tk.END, f"Destination MAC: {data['frames'][0]['dst_mac']}\n")
            self.encap_text.insert(tk.END, f"EtherType: {data['frames'][0]['ethertype']}\n")
        
        elif layer.layer_number == 1:  # Physical
            self.encap_text.insert(tk.END, f"Total Bits: {data['total_bits']}\n")
            self.encap_text.insert(tk.END, f"Total Binary Frames: {len(data['binary_frames'])}\n")
            if data['binary_frames']:
                self.encap_text.insert(tk.END, f"First Frame Binary (first 50 bits): {data['binary_frames'][0]['binary_data'][:50]}...\n")
        
        self.encap_text.insert(tk.END, "\n")
        self.encap_text.see(tk.END)
        self.root.update()
    
    def _display_layer_decapsulation(self, layer, data):
        """Display layer information during decapsulation"""
        self.decap_text.insert(tk.END, f"Layer {layer.layer_number}: {layer.layer_name}\n")
        self.decap_text.insert(tk.END, "-" * 80 + "\n")
        
        if layer.layer_number == 7:  # Application
            self.decap_text.insert(tk.END, f"Original Message: {data}\n")
        elif layer.layer_number == 6:  # Presentation
            self.decap_text.insert(tk.END, "Data decrypted and decoded\n")
        elif layer.layer_number == 5:  # Session
            self.decap_text.insert(tk.END, "Session validated\n")
        elif layer.layer_number == 4:  # Transport
            self.decap_text.insert(tk.END, "Segments reassembled\n")
        elif layer.layer_number == 3:  # Network
            self.decap_text.insert(tk.END, "Packets extracted\n")
        elif layer.layer_number == 2:  # Data Link
            self.decap_text.insert(tk.END, "Frames extracted\n")
        elif layer.layer_number == 1:  # Physical
            self.decap_text.insert(tk.END, "Binary data converted\n")
        
        self.decap_text.insert(tk.END, "\n")
        self.decap_text.see(tk.END)
        self.root.update()
    
    def draw_visualization(self):
        """Draw OSI layer visualization"""
        self.viz_canvas.delete("all")
        
        # Layer colors
        colors = [
            "#e74c3c",  # Application - Red
            "#e67e22",  # Presentation - Orange
            "#f39c12",  # Session - Yellow
            "#27ae60",  # Transport - Green
            "#3498db",  # Network - Blue
            "#9b59b6",  # Data Link - Purple
            "#34495e"   # Physical - Dark Gray
        ]
        
        layer_names = [
            "Layer 7: Application",
            "Layer 6: Presentation",
            "Layer 5: Session",
            "Layer 4: Transport",
            "Layer 3: Network",
            "Layer 2: Data Link",
            "Layer 1: Physical"
        ]
        
        # Canvas dimensions
        canvas_width = self.viz_canvas.winfo_width()
        canvas_height = self.viz_canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 1000
        if canvas_height <= 1:
            canvas_height = 600
        
        # Draw layers
        layer_height = 60
        start_y = 50
        layer_width = 300
        
        # Encapsulation side (left)
        encap_x = 100
        self.viz_canvas.create_text(
            encap_x + layer_width // 2,
            20,
            text="ENCAPSULATION ↓",
            font=("Arial", 14, "bold"),
            fill="#2c3e50"
        )
        
        for i, (name, color) in enumerate(zip(layer_names, colors)):
            y = start_y + i * (layer_height + 10)
            
            # Draw rectangle
            self.viz_canvas.create_rectangle(
                encap_x,
                y,
                encap_x + layer_width,
                y + layer_height,
                fill=color,
                outline="#2c3e50",
                width=2
            )
            
            # Draw text
            self.viz_canvas.create_text(
                encap_x + layer_width // 2,
                y + layer_height // 2,
                text=name,
                font=("Arial", 12, "bold"),
                fill="white"
            )
            
            # Draw arrow
            if i < 6:
                arrow_y = y + layer_height + 5
                self.viz_canvas.create_line(
                    encap_x + layer_width // 2,
                    arrow_y,
                    encap_x + layer_width // 2,
                    arrow_y + 10,
                    arrow=tk.LAST,
                    width=3,
                    fill="#2c3e50"
                )
        
        # Decapsulation side (right)
        decap_x = canvas_width - 400
        self.viz_canvas.create_text(
            decap_x + layer_width // 2,
            20,
            text="DECAPSULATION ↑",
            font=("Arial", 14, "bold"),
            fill="#2c3e50"
        )
        
        for i, (name, color) in enumerate(reversed(list(zip(layer_names, colors)))):
            y = start_y + i * (layer_height + 10)
            
            # Draw rectangle
            self.viz_canvas.create_rectangle(
                decap_x,
                y,
                decap_x + layer_width,
                y + layer_height,
                fill=color,
                outline="#2c3e50",
                width=2
            )
            
            # Draw text
            self.viz_canvas.create_text(
                decap_x + layer_width // 2,
                y + layer_height // 2,
                text=name,
                font=("Arial", 12, "bold"),
                fill="white"
            )
            
            # Draw arrow (upward)
            if i < 6:
                arrow_y = y
                self.viz_canvas.create_line(
                    decap_x + layer_width // 2,
                    arrow_y - 10,
                    decap_x + layer_width // 2,
                    arrow_y - 5,
                    arrow=tk.LAST,
                    width=3,
                    fill="#2c3e50"
                )
        
        # Draw transmission arrow in the middle
        mid_x = (encap_x + layer_width + decap_x) // 2
        bottom_y = start_y + 6 * (layer_height + 10) + layer_height
        
        self.viz_canvas.create_line(
            encap_x + layer_width + 20,
            bottom_y,
            decap_x - 20,
            bottom_y,
            arrow=tk.LAST,
            width=4,
            fill="#e74c3c"
        )
        
        self.viz_canvas.create_text(
            mid_x,
            bottom_y - 15,
            text="TRANSMISSION",
            font=("Arial", 12, "bold"),
            fill="#e74c3c"
        )
    
    def clear_output(self):
        """Clear all output"""
        self.encap_text.delete(1.0, tk.END)
        self.decap_text.delete(1.0, tk.END)
        self.viz_canvas.delete("all")
        self.status_label.config(text="Ready")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = OSISimulatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
