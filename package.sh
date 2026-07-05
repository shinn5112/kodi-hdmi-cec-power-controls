#!/usr/bin/env bash
set -euo pipefail

ADDON_DIR="script.hdmi.cec.power"
ADDON_XML="${ADDON_DIR}/addon.xml"
DIST_DIR="dist"

# Extract version from addon.xml
VERSION=$(python3 -c "import xml.etree.ElementTree as ET; print(ET.parse('${ADDON_XML}').getroot().get('version'))")
ZIP_NAME="${ADDON_DIR}-${VERSION}.zip"

mkdir -p "${DIST_DIR}"
rm -f "${DIST_DIR}/${ZIP_NAME}"

zip -r "${DIST_DIR}/${ZIP_NAME}" "${ADDON_DIR}/" \
    --exclude "*/__pycache__/*" \
    --exclude "*/*.pyc" \
    --exclude "*/*.pyo" \
    --exclude "*/.DS_Store"

echo "Built: ${DIST_DIR}/${ZIP_NAME}"
