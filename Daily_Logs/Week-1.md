# Internship Weekly Log: Week 1

**Developer:** Anurag Debnath & Abhilash Ghosh
**Date:** June 5, 2026

---

## Day 1: June 5, 2026

### Focus Area: Web Technologies & Networking — Dual Server Configuration on Ubuntu  
**Environment:** Ubuntu 26.04 LTS (UTM VM) / macOS (M1)

#### ✅ What I Did
1. **Network Interface Identification:**
   - Used `ip link show` to identify the active wired network card, locating the interface `enp0s1`.
   - Used `nmcli con show` to find the exact NetworkManager connection name (`netplan-enp0s1`).
2. **Static IP Configuration:**
   - Replaced the dynamic DHCP assignment with a fixed, static IP address to ensure the server remains reachable at the same address.
   - Assigned the IPv4 address `192.168.1.1/24` using `sudo nmcli con mod "netplan-enp0s1" ipv4.addresses 192.168.1.1/24`.
   - Set the IPv4 method to manual and applied the connection changes.
3. **SSH Server Installation & Activation:**
   - Updated package repositories (`sudo apt update`) and installed the OpenSSH server (`sudo apt install openssh-server -y`).
   - Enabled and started the service securely using `sudo systemctl enable --now ssh`.
   - Verified the daemon was successfully running and listening on port 22 (`Active: active (running)`).
4. **Python HTTP Server Deployment:**
   - Navigated to the home directory (`cd ~`).
   - Launched a lightweight built-in Python web server using `python3 -m http.server 8080`.
5. **System Verification & Testing:**
   - Opened a secondary terminal to test the SSH connection and successfully logged into the server locally (`iamanuragdn`).
   - Opened Firefox and navigated to `http://192.168.1.1:8080`, successfully accessing the server's directory listing (showing `.bash_history`, `Desktop/`, `Downloads/`, etc.).

#### 📸 Visual Evidence

<table>
  <tr>
    <td align="center"><b>1. SSH Server Verification (Terminal)</b></td>
    <td align="center"><b>2. HTTP Server Directory Listing (Browser)</b></td>
  </tr>
  <tr>
    <td align="center"><img src="/Daily_Logs/assets/week1_ssh_terminal.png" width="400" alt="Terminal showing SSH systemctl status active"></td>
    <td align="center"><img src="/Daily_Logs/assets/week1_http_browser.png" width="400" alt="Firefox browser showing the directory listing on port 8080"></td>
  </tr>
</table>

#### 📊 Results
| Configuration Metric | Assigned Value |
|----------------------|----------------|
| **Network Interface** | `enp0s1` |
| **Static IPv4 Address**| `192.168.1.1/24` |
| **SSH Service** | Active / Port `22` |
| **HTTP Service** | Python SimpleHTTP / Port `8080` |

#### 🧠 Key Learnings
- **NetworkManager CLI (`nmcli`):** Learned how to manually override automatic IP assignments to create a stable, predictable server address on a Linux machine.
- **Service Management (`systemctl`):** Understood how to use `systemctl` to not only check the status of a daemon (like SSH) but also enable it to start automatically upon system boot.
- **Dual-Server Functionality:** Grasped the distinct roles of different servers running simultaneously on the same machine—SSH handling secure terminal remote control on Port 22, while Python handles outward-facing file hosting on Port 8080.

#### ❌ Issues Faced & Solutions
| Issue | Cause | Solution |
|-------|-------|----------|
| **Dynamic IP changing on reboot** | Default DHCP configuration automatically reassigns IPs, breaking server access. | Switched `ipv4.method` to `manual` and explicitly assigned `192.168.1.1/24` via `nmcli`. |
| **SSH connections refused** | Ubuntu does not come with an SSH server pre-installed/active by default. | Installed `openssh-server` and utilized `systemctl enable --now ssh` to activate the listener daemon. |

#### 📁 Project Summary for Supervisor
"Configured the Ubuntu VM as a dual SSH and HTTP server. Assigned a static IP (`192.168.1.1/24`) on interface `enp0s1`, installed `openssh-server`, enabled it as a systemd service on port 22, and verified the SSH login. Subsequently, initialized a Python HTTP server on port 8080 and successfully confirmed outward file serving via the Firefox browser."
