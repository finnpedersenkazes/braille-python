#!/bin/bash
# Fix BRLTTY installation based on Installation.md findings
# This script addresses the issues documented in Installation.md

echo "=== Fixing BRLTTY Installation ==="
echo ""
echo "Based on Installation.md, the following issues need to be fixed:"
echo "1. BRLTTY service is not running (see line 264)"
echo "2. BRLTTY service is not enabled (see line 267)"
echo "3. /etc/brlapi.key permissions need to be 0644 (see lines 220-254)"
echo "4. User may need to be in brlapi group (see lines 745-754)"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "This script needs to be run with sudo:"
   echo "  sudo ./fix_brltty_installation.sh"
   exit 1
fi

echo "1. Checking /etc/brlapi.key permissions..."
CURRENT_PERMS=$(stat -c "%a" /etc/brlapi.key 2>/dev/null)
echo "   Current permissions: $CURRENT_PERMS"

if [ "$CURRENT_PERMS" != "644" ]; then
    echo "   Fixing permissions to 0644 (as documented in Installation.md line 224)..."
    chmod 0644 /etc/brlapi.key
    echo "   ✓ Permissions changed to 0644"
    ls -l /etc/brlapi.key
else
    echo "   ✓ Permissions are already correct (0644)"
fi

echo ""
echo "2. Starting BRLTTY service (as documented in Installation.md line 264)..."
systemctl start brltty.service
if systemctl is-active --quiet brltty; then
    echo "   ✓ BRLTTY service started successfully"
else
    echo "   ✗ Failed to start BRLTTY service"
    echo "   Check logs with: journalctl -u brltty.service"
fi

echo ""
echo "3. Enabling BRLTTY service for automatic startup on boot (as documented in Installation.md line 267)..."
systemctl enable brltty.service
if systemctl is-enabled --quiet brltty; then
    echo "   ✓ BRLTTY service enabled (will start automatically on boot/reboot)"
else
    echo "   ✗ Failed to enable BRLTTY service"
fi

echo ""
echo "4. Checking service status (as documented in Installation.md line 258)..."
systemctl status brltty.service --no-pager -l | head -15

echo ""
echo "=== Summary ==="
echo ""
echo "The following fixes were applied based on Installation.md:"
echo "  - Changed /etc/brlapi.key permissions to 0644 (line 224)"
echo "  - Started brltty.service (line 264)"
echo "  - Enabled brltty.service for automatic startup on boot (line 267)"
echo ""
echo "Next steps:"
echo "  1. Check if your Focus 40 Blue is connected (USB or Bluetooth)"
echo "  2. Check service logs: journalctl -u brltty.service -f"
echo "  3. Try running your Python script again"
echo ""
echo "If issues persist, check:"
echo "  - Service logs: journalctl -u brltty.service"
echo "  - Device detection: lsusb (for USB) or bluetoothctl (for Bluetooth)"
echo "  - Configuration: /etc/brltty.conf"
echo ""

