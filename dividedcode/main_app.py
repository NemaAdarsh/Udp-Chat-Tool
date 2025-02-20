import tkinter as tk
from ui_styles import AppStyles
from udp_network import UDPNetworkManager

class NetworkChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UDP Chat Tool")
        self.root.geometry("1200x800")
        
        # Configure UI styles
        AppStyles.configure_styles()
        
        # Build UI components
        self.ui_components = AppStyles.build_ui_components(root)
        
        # Initialize network manager with UI components
        self.network_manager = UDPNetworkManager(self.ui_components)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkChatApp(root)
    root.mainloop()