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

echo "Preparing source files for Arch package..."
# Copy execution directory to packaging/arch to be included
rm -rf "$ARCH_DIR/execution"
cp -r execution "$ARCH_DIR/"

echo "Building Arch package..."
cd "$ARCH_DIR"

# Clean previous builds in arch dir
rm -f *.pkg.tar.zst

# Run makepkg
# -f: Overwrite existing package
# -s: Install missing dependencies (if sudo available/needed)
# --noconfirm: Do not ask for confirmation
# Note: verifying source integrity is skipped for local files usually, but we might need to update checksums or skip
makepkg -f --noconfirm --skipchecksums --nodeps

# Move package to dist
echo "Moving package to dist/..."
mv *.pkg.tar.zst "$PROJECT_ROOT/$DIST_DIR/"

# Cleanup
rm -rf execution src pkg media-dashboard

echo "Package moved to $DIST_DIR/"
ls -l "$PROJECT_ROOT/$DIST_DIR/"*.pkg.tar.zst
