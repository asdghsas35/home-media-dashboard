# Helper script to drive the Windows build via Wine
set -e

# 1. Install Python (silent)
# Only install if python.exe doesn't exist to save time
if [ ! -f "$HOME/.wine/drive_c/Python311/python.exe" ]; then
    echo "Installing Python into Wine..."
    wine .tmp/python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=C:\\Python311
else
    echo "Python already installed in Wine."
fi

# 2. Install PyInstaller and dependencies in Wine
echo "Installing dependencies in Wine..."
wine C:\\Python311\\python.exe -m pip install --upgrade pip
wine C:\\Python311\\python.exe -m pip install pyinstaller flask requests python-dotenv

# 3. Build the Windows Executable
echo "Building Windows Executable..."
# We need to map the workspace execution path to Z: drive (default Wine mapping for /)
# Workspace is at /home/greg/Desktop/Home Media Dashboard Workspace
# So path is Z:\home\greg\Desktop\Home Media Dashboard Workspace\execution\app.py

WORK_DIR="Z:$(pwd)/execution"
DIST_DIR="Z:$(pwd)/dist"

wine C:\\Python311\\python.exe -m PyInstaller --noconfirm --onefile --windowed --name media-dashboard-win --add-data "$WORK_DIR/templates;templates" --add-data "$WORK_DIR/static;static" "$WORK_DIR/app.py"

echo "Build complete. Check dist/media-dashboard-win.exe"
