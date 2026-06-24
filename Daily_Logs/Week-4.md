# Internship Weekly Log: Week 4

**Developer:** Anurag Debnath & Abhilash Ghosh \
**Date:** June 24, 2026  

---

## Day 1: June 24, 2026

### Part 1: Intelligent Robotics — RPLIDAR C1 Obstacle Detection & Navigation System
**Hardware:** SLAMTEC RPLIDAR C1, MacBook Air
**Environment:** macOS, Python 3.11 venv, pyserial · numpy · matplotlib · scipy

#### ✅ What I Did
1. **Library Research & BreezySLAM Attempt:** Attempted to use the `breezyslam` Python library for SLAM. After studying the author's GitHub repository, confirmed that BreezySLAM uses C extensions that require compilation from source and has documented compatibility issues with SLAMTEC RPLIDAR A1/C1 series — even the author states he cannot provide support for this combination. `pip install breezyslam` confirmed: no prebuilt wheel available for Python 3.11 on macOS.

2. **Custom Protocol Implementation:** Since no compatible library exists for the C1, implemented raw serial communication from scratch using `pyserial`. Decoded the RPLIDAR binary protocol manually:
   - Start scan command: `0xA5 0x20`
   - Stop command: `0xA5 0x25`
   - Each data packet = 5 bytes → `quality (b0)`, `angle_low (b1)`, `angle_high (b2)`, `dist_low (b3)`, `dist_high (b4)`
   - Baud rate: 460800 (specific to C1, different from older A1/A2 models)

3. **2D Live Visualizer (built in Week 3, refined today):** Extended the Week 3 static polar visualizer with:
   - 3600-slot buffer (0.1° angular resolution)
   - 6-frame median filter per slot to eliminate noise spikes
   - cKDTree-based neighbor filter (removes isolated points with fewer than 2 neighbors within 150mm)
   - Quality threshold filter (quality > 12 out of max 63)

4. **Obstacle Alert System (`obstacle_alert.py`):** Built a split-panel system with:
   - Live polar map with color-coded points by distance zone
   - Right panel showing zone bar charts (point counts per zone) and directional alerts (FRONT / LEFT / BACK-RIGHT etc.)

5. **Navigation System with Safe Path (`obstacle_nav.py` → `lidar_final.py`):** Implemented a **sector-based safe direction finder**:
   - Divides 360° into 15° sectors
   - Computes minimum clearance per sector
   - Selects the sector with the **maximum minimum clearance** as the safest direction
   - Renders a **green GO arrow** and **40° cone** pointing toward the safe path
   - Bottom label shows: `▲ Safest direction: FRONT-LEFT (2.3m clearance)`

6. **Final Polished System (`lidar_final.py`):** Combined map + info panel into one professional layout:
   - Left: live map with zone rings, GO arrow, safe cone, danger arrow, compass
   - Right: zone statistics bars, closest obstacle readout, active directional alerts, safe path summary

#### 📸 Visual Evidence
<table>
  <tr>
    <td align="center"><b>LiDAR Obstacle Navigation Interface</b></td>
  </tr>
  <tr>
    <td align="center">
      <img src="assets/week4_lidar_obstacle_navigation.png" width="500" alt="Real-time LiDAR obstacle navigation interface displaying zone statistics and proximity alerts">
    </td>
  </tr>
</table>

#### 📊 Results
| Metric | Value |
|--------|-------|
| **Scan Resolution** | 0.1° (3600 angular slots) |
| **Smoothing** | 6-frame median filter per slot |
| **Noise Filter** | cKDTree — min 2 neighbours within 150mm |
| **Quality Threshold** | > 12 (out of 63 max) |
| **Zone Thresholds** | 500mm / 1000mm / 1500mm |
| **Safe Sector Size** | 15° per sector, 24 sectors total |
| **Render Rate** | ~10 FPS |
| **Max Detection Range** | 6000mm (6m) |
| **Points per Frame** | ~3500–3600 clean points |
| **Output Save** | `lidar_obstacle_navigation.py` @200 DPI |

#### 🧠 Key Learnings
- **BreezySLAM Incompatibility:** Python SLAM libraries targeting older RPLIDAR models (A1/A2) use C extensions that won't build on modern macOS + Python 3.11. Always verify library compatibility against both the sensor model and the Python version before investing time in installation.
- **Raw Serial Protocol:** The RPLIDAR C1 speaks a simple binary protocol over UART. Once the packet structure is understood (5 bytes per point), no third-party library is needed — raw `pyserial` is sufficient and more reliable.
- **Median > Mean for LiDAR noise:** A single bad reflection (glass, shiny surface) can spike a distance reading by 3–4m. Median filtering across 6 frames per slot eliminates such spikes completely while preserving real geometry.
- **Safe Path = Max of Minimums:** The safest direction to move is not the direction with the most points or the average distance — it is the sector whose *worst* point is still the farthest away. This guarantees clearance across the entire cone, not just at one angle.
- **cKDTree for Point Cloud Filtering:** Scipy's `cKDTree` performs spatial neighbour queries in O(log n) time — far faster than brute-force loops over thousands of points per frame.
- **Matplotlib artists outside loops:** Colorbars, figure objects, and axis objects must be created once outside the animation loop. Creating them inside causes unbounded stacking and UI breakage.

#### ❌ Issues Faced & Solutions
| Issue | Cause | Solution |
|-------|-------|----------|
| `breezyslam` install failed | No prebuilt Python 3.11 wheel; requires C compilation; incompatible with RPLIDAR C1 | Replaced with custom raw serial implementation |
| `ModuleNotFoundError: serial` | VS Code terminal used system Python, not venv Python | Switched to `.venv/bin/python3 script.py` explicitly |
| Colorbar duplicating every frame | `fig.colorbar()` called inside the update loop | Moved colorbar creation outside loop using a dummy scatter |
| Scattered noise points across map | Low quality threshold + no spatial filtering | Raised quality threshold to > 12, added cKDTree neighbour filter (r=150mm, min 2 neighbours) |
| SLAM drift while walking | ICP scan matching without odometry accumulates rotation error | Noted as limitation — true mobile SLAM requires wheel encoders; static scanning used instead |
| Port not found on relaunch | LiDAR unplugged between sessions, port name changed | Added `ls /dev/cu.*` verification step before every run |

#### 📁 Files Created / Modified
- [lidar_obstacle_navigation.py](../LiDAR/lidar_obstacle_navigation.py) — Real-time LiDAR obstacle navigation interface displaying zone statistics, obstacle proximity alerts, and safe path calculation.

---
### Part 2: Intelligent Robotics — EMEET SmartCam S600 Integration & Object Detection  
**Hardware:** Raspberry Pi (Arm64), EMEET SmartCam S600 (4K UVC)  
**Environment:** Raspberry Pi OS (Debian Bookworm)

#### ✅ What I Did
1. **Hardware Connection:** Plugged the 4K EMEET SmartCam into the Raspberry Pi.
2. **Environment Setup:** Installed OpenCV (`python3-opencv`) via `apt` in the local `cubobots` environment.
3. **Camera Verification:** Verified the camera feed using a basic OpenCV capture script, initially testing the `/dev/video0` node and fixing index assignments.
4. **Model Integration:** Downloaded the pre-trained object detection zip file ("Object and Animal Recognition With Raspberry Pi and OpenCV") from Core Electronics.
5. **Code Modification:** Refactored the core object detection script (`object-ident.py`). Replaced the hardcoded legacy paths (`/home/pi/...`) with relative file paths so it could run under the current `cubobots` user profile.
6. **Deployment:** Successfully executed the script to perform live, real-time object detection using the SSD MobileNet model.

#### 📸 Visual Evidence
<table>
  <tr>
    <td align="center"><b>1. Hardware Setup</b></td>
    <td align="center"><b>2. Live Object Detection Output</b></td>
  </tr>
  <tr>
    <td align="center"> <img src="assets/week4_hardware-setup.jpeg" width="250" alt="Hardware setup showing Raspberry Pi and connected EMEET camera"></td>
    <td align="center"><img src="assets/week4_live-object-detection-output.jpeg" width="500" alt="Live OpenCV window showing bounding boxes and object detection confidence"></td>
  </tr>
</table>

#### 📊 Results
| Metric | Value |
|--------|-------|
| **Camera Feed** | Downscaled to 640x480 for real-time processing |
| **Object Model** | SSD MobileNet v3 Large (COCO 2020) |
| **Detection Status** | Successfully identifying objects and applying bounding boxes |
| **Pathing Status** | Refactored for universal portability via relative paths |

#### 🧠 Key Learnings
- **User Environment Dependency:** Scripts downloaded from third-party tutorials often hardcode specific usernames (like the default `pi` user). Using relative file paths is a much more robust coding practice that ensures the script won't break when moved to a different machine or user profile (like `cubobots`).
- **OpenCV Video Nodes:** A single plugged-in USB camera can generate dozens of virtual `/dev/video` nodes on Raspberry Pi OS. Verifying the correct node index is a crucial first step before deploying a computer vision model.

#### ❌ Issues Faced & Solutions
| Issue | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError` for `coco.names` | Code hardcoded to the default `pi` username, but current user is `cubobots` | Refactored script to use relative file paths |
| `Internal data stream error` | OpenCV defaulted to unstable GStreamer backend | Initialized capture with `cv2.VideoCapture(0, cv2.CAP_V4L2)` |

#### 📁 Files Created / Modified
- [final_object-ident.py](../Raspberry/Object%20Detection/final_object-ident.py) — Fully refactored MobileNet SSD object detection script with relative pathing and live camera capture.
