#!/bin/bash
set -e

# Configuration
DIST_DIR="dist"
ARCH_DIR="packaging/arch"
PROJECT_ROOT=$(pwd)

# Ensure we are in the project root
if [ ! -f "media-dashboard.spec" ]; then
    echo "Error: Please run this script from the project root directory."
    exit 1
fi

# Ensure existing binary is up to date? 
# Creating the deb package builds it, but Arch PKGBUILD expects it in dist/media-dashboard.
# We should probably run pyinstaller here too if not exists or forced?
# For now, let's assume dist/media-dashboard exists or run pyinstaller.

# Always rebuild binary to ensure latest code changes are included
echo "Building binary..."
rm -f "dist/media-dashboard"
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
pyinstaller media-dashboard.spec

echo "Building Arch package..."
cd "$ARCH_DIR"

# Clean previous builds in arch dir
rm -f *.pkg.tar.zst

# Run makepkg
# -f: Overwrite existing package
# -s: Install missing dependencies (if sudo available/needed)
# --noconfirm: Do not ask for confirmation
makepkg -f --noconfirm

# Move package to dist
echo "Moving package to dist/..."
mv *.pkg.tar.zst "$PROJECT_ROOT/$DIST_DIR/"

echo "Package moved to $DIST_DIR/"
ls -l "$PROJECT_ROOT/$DIST_DIR/"*.pkg.tar.zst
