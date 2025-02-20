import tkinter as tk
from tkinter import ttk, scrolledtext

class AppStyles:
    @staticmethod
    def configure_styles():
        # Configure style for a modern look
        style = ttk.Style()
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", background="#f0f0f0")
        style.configure("TButton", padding=5)
    
    @staticmethod
    def configure_chat_display(message_display):
        # Configure chat display colors
        message_display.configure(
            background="#ffffff",
            foreground="#000000",
            selectbackground="#0078d7",
            selectforeground="#ffffff",
            font=("Segoe UI", 10)
        )
    
    @staticmethod
    def configure_edu_panel(edu_text):
        # Configure educational panel
        edu_text.configure(
            background="#f8f8f8",
            foreground="#333333",
            font=("Segoe UI", 10)
        )
    
    @staticmethod
    def create_educational_content():
        return """🔹 UDP (User Datagram Protocol):
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

Enter the destination IP and port, then click 'Start Chat'!"""

    @staticmethod
    def build_ui_components(root):
        # Create main container
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel (Chat Area)
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Connection Frame
        connection_frame = ttk.LabelFrame(left_panel, text="UDP Settings")
        connection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # IP Entry
        ttk.Label(connection_frame, text="Friend's IP:").pack(side=tk.LEFT, padx=5)
        ip_entry = ttk.Entry(connection_frame)
        ip_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ip_entry.insert(0, "192.168.1.1")
        
        # Port Entry
        ttk.Label(connection_frame, text="Port:").pack(side=tk.LEFT, padx=5)
        port_entry = ttk.Entry(connection_frame, width=6)
        port_entry.pack(side=tk.LEFT, padx=5)
        port_entry.insert(0, "12345")
        
        # Start Button placeholder (will be configured in main)
        start_btn = ttk.Button(connection_frame, text="Start Chat")
        start_btn.pack(side=tk.LEFT, padx=5)
        
        # Chat Area
        chat_frame = ttk.LabelFrame(left_panel, text="Chat")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message Display
        message_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, height=20)
        message_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Message Entry
        message_frame = ttk.Frame(chat_frame)
        message_frame.pack(fill=tk.X, padx=5, pady=5)
        
        message_entry = ttk.Entry(message_frame)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        message_entry.config(state='disabled')
        
        send_btn = ttk.Button(message_frame, text="Send")
        send_btn.pack(side=tk.LEFT, padx=5)
        send_btn.config(state='disabled')
        
        # Create right panel (Network Statistics)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # Network Statistics
        stats_frame = ttk.LabelFrame(right_panel, text="Network Statistics")
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Statistics Labels
        stats_labels = {}
        stats = [
            "Status", "Local IP", "Port",
            "Messages Sent", "Messages Received",
            "Bytes Sent", "Bytes Received",
            "Network Interface", "Session Duration"
        ]
        
        for stat in stats:
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            ttk.Label(frame, text=f"{stat}:").pack(side=tk.LEFT)
            stats_labels[stat] = ttk.Label(frame, text="---")
            stats_labels[stat].pack(side=tk.RIGHT)
        
        # Educational Panel
        edu_frame = ttk.LabelFrame(right_panel, text="Network Concepts")
        edu_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        edu_text = scrolledtext.ScrolledText(edu_frame, wrap=tk.WORD, height=10)
        edu_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        edu_text.insert(tk.END, AppStyles.create_educational_content())
        edu_text.config(state='disabled')
        
        # Apply styles
        AppStyles.configure_chat_display(message_display)
        AppStyles.configure_edu_panel(edu_text)
        
        # Return all UI components as a dictionary
        return {
            'main_container': main_container,
            'left_panel': left_panel,
            'right_panel': right_panel,
            'connection_frame': connection_frame,
            'ip_entry': ip_entry,
            'port_entry': port_entry,
            'start_btn': start_btn,
            'chat_frame': chat_frame,
            'message_display': message_display,
            'message_entry': message_entry,
            'send_btn': send_btn,
            'stats_frame': stats_frame,
            'stats_labels': stats_labels,
            'edu_frame': edu_frame,
            'edu_text': edu_text
        }