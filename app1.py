import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import threading
import time
import json
from datetime import datetime
import psutil
import platform
import subprocess

class NetworkChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Chat Tool")
        self.root.geometry("1200x800")
        
        # Initialize network variables
        self.sock = None
        self.connected = False
        self.bytes_sent = 0
        self.bytes_received = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.start_time = time.time()
        self.friend_ip = None
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (Chat Area)
        self.left_panel = ttk.Frame(self.main_container)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connection Frame
        self.connection_frame = ttk.LabelFrame(self.left_panel, text="UDP Settings")
        self.connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # IP Entry
        ttk.Label(self.connection_frame, text="Friend's IP:").pack(side=tk.LEFT, padx=5)
        self.ip_entry = ttk.Entry(self.connection_frame)
        self.ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.ip_entry.insert(0, "192.168.1.1")
        
        # Port Entry
        ttk.Label(self.connection_frame, text="Port:").pack(side=tk.LEFT, padx=5)
        self.port_entry = ttk.Entry(self.connection_frame, width=6)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.insert(0, "12345")
        
        # Start Button
        self.start_btn = ttk.Button(self.connection_frame, text="Start Chat", command=self.initialize_udp)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
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
        self.message_entry.config(state='disabled')
        
        self.send_btn = ttk.Button(self.message_frame, text="Send", command=lambda: self.send_message(None))
        self.send_btn.pack(side=tk.LEFT, padx=5)
        self.send_btn.config(state='disabled')
        
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

Enter the destination IP and port, then click 'Start Chat'!""")
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
    
    def configure_firewall(self, port):
        try:
            # On Windows, add firewall rule for the specified port
            if platform.system() == "Windows":
                cmd = f'netsh advfirewall firewall add rule name="Allow UDP {port}" protocol=UDP dir=in localport={port} action=allow'
                subprocess.run(cmd, shell=True, check=True)
                return True
            return True  # For non-Windows systems, assume it's ok
        except Exception as e:
            messagebox.showerror("Firewall Error", f"Failed to configure firewall: {str(e)}")
            return False
    
    def initialize_udp(self):
        # Get port and validate
        try:
            port = int(self.port_entry.get())
            if port < 1024 or port > 65535:
                messagebox.showerror("Error", "Port must be between 1024 and 65535")
                return
        except ValueError:
            messagebox.showerror("Error", "Port must be a number")
            return
        
        # Get friend's IP
        self.friend_ip = self.ip_entry.get()
        if not self.friend_ip:
            messagebox.showerror("Error", "Please enter friend's IP address")
            return
        
        # Configure firewall (Windows)
        if not self.configure_firewall(port):
            return
        
        try:
            # Initialize socket with dynamic port
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("0.0.0.0", port))
            self.connected = True
            
            # Update UI
            self.message_display.insert(tk.END, f"UDP Chat initialized on port {port}. You can start sending messages now.\n")
            self.message_display.insert(tk.END, f"No connection required - UDP is connectionless!\n")
            self.message_display.see(tk.END)
            
            # Disable settings, enable chat
            self.ip_entry.config(state='disabled')
            self.port_entry.config(state='disabled')
            self.start_btn.config(state='disabled')
            self.message_entry.config(state='normal')
            self.send_btn.config(state='normal')
            
            # Reset statistics
            self.start_time = time.time()
            self.bytes_sent = 0
            self.bytes_received = 0
            self.messages_sent = 0
            self.messages_received = 0
            
            # Start receive thread
            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize UDP: {str(e)}")
    
    def send_message(self, event):
        if not self.connected or not self.sock:
            self.message_display.insert(tk.END, "Please start the chat first!\n")
            return
            
        message = self.message_entry.get()
        if message:
            try:
                self.sock.sendto(message.encode(), (self.friend_ip, int(self.port_entry.get())))
                self.bytes_sent += len(message.encode())
                self.messages_sent += 1
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.message_display.insert(tk.END, f"[{timestamp}] You: {message}\n")
                self.message_display.see(tk.END)
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.message_display.insert(tk.END, f"Error sending message: {str(e)}\n")
    
    def receive_messages(self):
        while self.connected and self.sock:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = data.decode()
                self.bytes_received += len(data)
                self.messages_received += 1
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                sender_ip = addr[0]
                self.message_display.insert(tk.END, f"[{timestamp}] {sender_ip}: {message}\n")
                self.message_display.see(tk.END)
            except:
                if not self.connected:
                    break
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
                port_str = self.port_entry.get() if not self.connected else self.port_entry.get()
                stats = {
                    "Status": "Chatting (UDP)" if self.connected else "Waiting to start",
                    "Local IP": local_ip,
                    "Port": port_str,
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