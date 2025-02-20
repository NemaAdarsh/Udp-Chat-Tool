import socket
import threading
import time
import platform
import subprocess
import psutil
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

class UDPNetworkManager:
    def __init__(self, ui_components):
        # Store UI references
        self.message_display = ui_components['message_display']
        self.message_entry = ui_components['message_entry']
        self.send_btn = ui_components['send_btn']
        self.ip_entry = ui_components['ip_entry']
        self.port_entry = ui_components['port_entry']
        self.start_btn = ui_components['start_btn']
        self.stats_labels = ui_components['stats_labels']
        
        # Initialize network variables
        self.sock = None
        self.connected = False
        self.bytes_sent = 0
        self.bytes_received = 0
        self.messages_sent = 0
        self.messages_received = 0
        self.start_time = time.time()
        self.friend_ip = None
        
        # Set up event handlers
        self.message_entry.bind("<Return>", self.send_message)
        self.send_btn.config(command=lambda: self.send_message(None))
        self.start_btn.config(command=self.initialize_udp)
        
        # Start statistics update thread
        self.update_thread = threading.Thread(target=self.update_statistics, daemon=True)
        self.update_thread.start()
    
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