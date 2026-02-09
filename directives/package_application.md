# Package Application Directive

## Goal
Create installable packages for Debian/Ubuntu (`.deb`) and Arch Linux (`.pkg.tar.zst`) distributions.
All generated packages MUST be placed in the `dist/` directory.

## Inputs
- **Source Code**: `execution/`
- **Packaging Config**: `packaging/debian/` and `packaging/arch/`
- **Build Scripts**: `packaging/deb_build.sh` and `packaging/arch_build.sh`

## Tools
- `packaging/deb_build.sh`: Builds the Debian package.
- `packaging/arch_build.sh`: Builds the Arch Linux package.

## Instructions

### 1. Build Debian Package
Run the following script to create a `.deb` package.
```bash
./packaging/deb_build.sh
```
**Output**: `dist/media-dashboard_x.x.x_amd64.deb`

### 2. Build Arch Linux Package
Run the following script to create a `.pkg.tar.zst` package.
```bash
./packaging/arch_build.sh
```
**Output**: `dist/media-dashboard-x.x.x-x-x86_64.pkg.tar.zst`

## Configuration
- **Output Directory**: The build scripts are configured to move the final artifacts to the `dist/` folder.
- **Formats**:
    -   Debian: `.deb`
    -   Arch: `.pkg.tar.zst`
