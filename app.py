import tkinter as tk
from tkinter import ttk, scrolledtext
import socket
import threading
import time
import json
from datetime import datetime
import psutil
import platform

class NetworkChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Computer Networks Lab 3 Tool")
        self.root.geometry("1200x800")
        
        # Initialize network variables
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 12345
        self.sock.bind(("0.0.0.0", self.port))
        self.connected = False
        self.bytes_sent = 0
        self.bytes_received = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.start_time = time.time()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (Chat Area)
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connection Frame
        self.connection_frame = ttk.LabelFrame(self.left_panel, text="Connection Settings")
        self.connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # IP Entry
        ttk.Label(self.connection_frame, text="Friend's IP:").pack(side=tk.LEFT, padx=5)
        self.ip_entry = ttk.Entry(self.connection_frame)
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.ip_entry.insert(0, "192.168.1.1")
        
        # Connect Button
        self.connect_btn = ttk.Button(self.connection_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        # Chat Area
        self.chat_frame = ttk.LabelFrame(self.left_panel, text="Chat")
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message Display
        self.message_display = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, height=20)
        self.message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message Entry
        self.message_frame = ttk.Frame(self.chat_frame)
        self.message_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.message_entry = ttk.Entry(self.message_frame)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_btn = ttk.Button(self.message_frame, text="Send", command=lambda: self.send_message(None))
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        # Create right panel (Network Statistics)
        self.right_panel = ttk.Frame(self.main_container)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Network Statistics
        self.stats_frame = ttk.LabelFrame(self.right_panel, text="Network Statistics")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statistics Labels
        self.stats_labels = {}
        stats = [
            "Status", "Local IP", "Port",
            "Messages Sent", "Messages Received",
            "Bytes Sent", "Bytes Received",
            "Network Interface", "Session Duration"
        ]
        
        for stat in stats:
            frame = ttk.Frame(self.stats_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=f"{stat}:").pack(side=tk.LEFT)
            self.stats_labels[stat] = ttk.Label(frame, text="---")
            self.stats_labels[stat].pack(side=tk.RIGHT)
        
        # Educational Panel
        self.edu_frame = ttk.LabelFrame(self.right_panel, text="Network Concepts")
        self.edu_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.edu_text = scrolledtext.ScrolledText(self.edu_frame, wrap=tk.WORD, height=10)
        self.edu_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.edu_text.insert(tk.END, """🔹 UDP (User Datagram Protocol):
- A connectionless protocol
- Faster than TCP but less reliable
- No guaranteed delivery or order
- Perfect for real-time applications

🔹 Socket Programming:
- Enables network communication
- Uses IP addresses and ports
- Allows data exchange between computers

🔹 IPv4 Addressing:
- Format: xxx.xxx.xxx.xxx
- Each number: 0-255
- Used to identify devices on network

Press 'Connect' to start chatting!""")
        self.edu_text.config(state='disabled')
        
        # Start statistics update thread
        self.update_thread = threading.Thread(target=self.update_statistics, daemon=True)
        self.update_thread.start()
        
        # Style configuration
        self.style_ui()
        
    def style_ui(self):
        # Configure style for a modern look
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0")
        style.configure("TButton", padding=5)
        
        # Configure chat display colors
        self.message_display.configure(
            background="#ffffff",
            foreground="#000000",
            selectbackground="#0078d7",
            selectforeground="#ffffff",
            font=("Segoe UI", 10)
        )
        
        # Configure educational panel
        self.edu_text.configure(
            background="#f8f8f8",
            foreground="#333333",
            font=("Segoe UI", 10)
        )
    
    def toggle_connection(self):
        if not self.connected:
            self.friend_ip = self.ip_entry.get()
            self.connected = True
            self.connect_btn.config(text="Disconnect")
            self.ip_entry.config(state='disabled')
            self.start_time = time.time()
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            
            self.message_display.insert(tk.END, "Connected to chat!\n")
        else:
            self.connected = False
            self.connect_btn.config(text="Connect")
            self.ip_entry.config(state='normal')
            self.message_display.insert(tk.END, "Disconnected from chat.\n")
    
    def send_message(self, event):
        if not self.connected:
            self.message_display.insert(tk.END, "Please connect first!\n")
            return
            
        message = self.message_entry.get()
        if message:
            try:
                self.sock.sendto(message.encode(), (self.friend_ip, self.port))
                self.bytes_sent += len(message.encode())
                self.messages_sent += 1
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.message_display.insert(tk.END, f"[{timestamp}] You: {message}\n")
                self.message_display.see(tk.END)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.message_display.insert(tk.END, f"Error sending message: {str(e)}\n")
    
    def receive_messages(self):
        while self.connected:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode()
                self.bytes_received += len(data)
                self.messages_received += 1
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.message_display.insert(tk.END, f"[{timestamp}] Friend: {message}\n")
                self.message_display.see(tk.END)
            except:
                continue
    
    def update_statistics(self):
        while True:
            if hasattr(self, 'stats_labels'):
                # Get local IP
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                # Get network interface info
                net_if = ""
                for interface, addrs in psutil.net_if_addrs().items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET and addr.address == local_ip:
                            net_if = interface
                            break
                
                # Update statistics
                stats = {
                    "Status": "Connected" if self.connected else "Disconnected",
                    "Local IP": local_ip,
                    "Port": str(self.port),
                    "Messages Sent": str(self.messages_sent),
                    "Messages Received": str(self.messages_received),
                    "Bytes Sent": f"{self.bytes_sent:,} bytes",
                    "Bytes Received": f"{self.bytes_received:,} bytes",
                    "Network Interface": net_if,
                    "Session Duration": f"{int(time.time() - self.start_time)} seconds"
                }
                
                for key, value in stats.items():
                    if key in self.stats_labels:
                        self.stats_labels[key].config(text=value)
            
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkChatApp(root)
    root.mainloop()