#!/bin/bash
# Setup script for Braille Displays with BRLTTY
# Supports: Focus 40 Blue, Brailliant BI 20X, and other BRLTTY-compatible devices

echo "=== Braille Display Setup Script ==="
echo ""

# Check if running as root for certain commands
if [ "$EUID" -eq 0 ]; then 
   SUDO=""
else 
   SUDO="sudo"
fi

echo "1. Checking BRLTTY installation..."
if command -v brltty &> /dev/null; then
    echo "   ✓ BRLTTY is installed: $(brltty -v 2>&1 | head -1)"
else
    echo "   ✗ BRLTTY is not installed"
    echo "   Install with: sudo apt install brltty python3-brlapi python3-louis"
    exit 1
fi

echo ""
echo "2. Checking BRLTTY service status..."
if systemctl is-active --quiet brltty; then
    echo "   ✓ BRLTTY service is running"
else
    echo "   ✗ BRLTTY service is not running"
fi

echo ""
echo "   Checking if BRLTTY is enabled to start on boot..."
if systemctl is-enabled --quiet brltty 2>/dev/null; then
    echo "   ✓ BRLTTY is enabled (will start automatically on boot)"
else
    echo "   ⚠ BRLTTY is NOT enabled to start on boot"
    echo ""
    echo "   IMPORTANT: To enable automatic startup on boot, run:"
    echo "   sudo systemctl enable brltty"
    echo ""
    echo "   Then start the service:"
    echo "   sudo systemctl start brltty"
fi

echo ""
echo "3. Checking for braille display devices..."
echo "   USB devices:"
USB_DEVICES=$(lsusb | grep -i "freedom\|focus\|humanware\|brailliant")
if [ -n "$USB_DEVICES" ]; then
    echo "   ✓ Found braille display devices:"
    echo "$USB_DEVICES" | sed 's/^/      /'
else
    echo "      No known braille display devices found in USB list"
    echo "      (This is normal if device is not connected or using Bluetooth)"
fi

echo ""
echo "   Serial devices:"
ls /dev/ttyUSB* 2>/dev/null && echo "      Found USB serial devices" || echo "      No USB serial devices found"
ls /dev/ttyACM* 2>/dev/null && echo "      Found ACM devices" || echo "      No ACM devices found"

echo ""
echo "4. Checking user groups..."
if groups | grep -q "brltty\|brlapi\|dialout"; then
    echo "   ✓ User is in braille-related groups"
    groups | grep -E "brltty|brlapi|dialout"
else
    echo "   ⚠ User may need to be added to groups"
    echo "   Run: sudo usermod -a -G brltty,dialout $USER"
    echo "   Then log out and back in"
fi

echo ""
echo "5. BRLTTY Configuration (/etc/brltty.conf):"
if [ -f /etc/brltty.conf ]; then
    echo "   Configuration file exists"
    DRIVER_FOUND=false
    if grep -q "braille-driver.*fs" /etc/brltty.conf 2>/dev/null; then
        echo "   ✓ Focus driver (fs) configured"
        grep "braille-driver.*fs" /etc/brltty.conf | sed 's/^/      /'
        DRIVER_FOUND=true
    fi
    if grep -q "braille-driver.*hw" /etc/brltty.conf 2>/dev/null; then
        echo "   ✓ HumanWare driver (hw) configured"
        grep "braille-driver.*hw" /etc/brltty.conf | sed 's/^/      /'
        DRIVER_FOUND=true
    fi
    if [ "$DRIVER_FOUND" = false ]; then
        echo "   ⚠ No driver explicitly set (auto-detection will be used)"
        echo "   ✓ BRLTTY will automatically detect your device"
    fi
else
    echo "   Configuration file does not exist (using defaults)"
    echo "   ✓ BRLTTY will automatically detect your device"
fi

echo ""
echo "=== Next Steps ==="
echo ""
echo "To ensure BRLTTY starts automatically on boot (IMPORTANT for automatic operation):"
echo "  sudo systemctl enable brltty"
echo "  sudo systemctl start brltty"
echo ""
echo "If the service is not running:"
echo "  sudo systemctl start brltty"
echo ""
echo "If the device is not detected, try:"
echo "  1. Unplug and replug your braille display"
echo "  2. Check if it appears in: lsusb"
echo "  3. Start BRLTTY service: sudo systemctl start brltty"
echo "  4. Check service logs: sudo journalctl -u brltty -f"
echo ""
echo "Supported devices (auto-detected by BRLTTY):"
echo "  - Focus 40 Blue (Freedom Scientific) - driver: fs"
echo "  - Brailliant BI 20X (HumanWare) - driver: hw"
echo "  - Most other BRLTTY-compatible displays"
echo ""

