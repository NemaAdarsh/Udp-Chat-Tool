# Computer Networks UDP Chat Tool

![image](https://github.com/user-attachments/assets/9188722f-3504-43e0-ae0d-42088360a22e)


## Overview
Computer Networks UDP Chat Tool is a simple, executable UDP-based chat application designed for students to explore socket programming and UDP communication without needing to set up Python or dependencies. This tool allows users to establish a connection over a local network and exchange messages in real-time.

## Features
- **User-friendly GUI**: No need to run Python scripts manually; just launch the executable.
- **Real-time chat**: Send and receive messages instantly using UDP sockets.
- **Network statistics**: Monitor sent/received messages, bytes transferred, and session details.
- **Educational insights**: Provides a built-in reference on UDP, socket programming, and IP addressing.

## Prerequisites
To use this tool, ensure the following requirements are met:
- Two computers connected to the same local network (Wi-Fi or Ethernet).
- Windows OS (for best compatibility with the provided `.exe` file).
- **Wireshark** (optional, for network packet analysis).

## Setup and Execution
1. **Download and Extract**
   - Download the `Computer_Networks_Lab_3.exe` from this repository.
   - Extract it to a preferred location.

2. **Find Your IP Address**
   - Open **Command Prompt** (`cmd`) on both computers.
   - Run the command: `ipconfig`
   - Note the **IPv4 Address** (e.g., `192.168.x.x`).

3. **Allow UDP Traffic Through Firewall** (if needed)
   - Open Command Prompt as Administrator.
   - Run the following command:
     ```sh
     netsh advfirewall firewall add rule name="Allow UDP 12345" protocol=UDP dir=in localport=12345 action=allow
     ```

4. **Run the Application**
   - Open `Computer_Networks_Lab_3.exe` on both computers.
   - Enter your partner’s IP in the **Connection Settings** and click **Connect**.
   - Start chatting!

5. **Monitor Packets with Wireshark** (Optional)
   - Open **Wireshark** and start capturing packets.
   - Use the filter: `udp.port == 12345` to view only chat-related UDP packets.

## Theory Behind the Tool
### **What is UDP?**
User Datagram Protocol (UDP) is a connectionless, lightweight transport layer protocol that allows data to be sent without establishing a dedicated connection.
#### **Key Characteristics:**
- No connection setup required.
- Faster than TCP but less reliable.
- No guaranteed delivery or order of packets.
- Commonly used in real-time applications like VoIP and gaming.

### **Socket Programming**
Sockets enable communication between devices over a network. This tool uses Python's `socket` module to send and receive messages over UDP.

### **IPv4 Addressing**
- Format: `xxx.xxx.xxx.xxx`
- Each number ranges from `0-255`.
- Identifies devices uniquely on a network.

## Cleanup (Optional)
To remove the firewall rule added earlier, run:
```sh
netsh advfirewall firewall delete rule name="Allow UDP 12345"
```

## Conclusion
This tool provides a hands-on approach to learning about UDP and socket programming while eliminating the complexity of setting up Python manually. It serves as an educational resource for students exploring computer networks.

---
If you found this tool helpful, consider giving this repo a ⭐ and contributing to improve it! 🚀
