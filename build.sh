#!/bin/bash
# Builds Quizlet2CSV.app from source. Run this (via Terminal) after
# downloading/unzipping the project, and again any time you edit the
# .applescript/.py source or swap the icon.
set -euo pipefail
cd "$(dirname "$0")"

APP_NAME="Quizlet2CSV.app"
ICON_SRC="icon.png"

rm -rf "$APP_NAME"
osacompile -o "$APP_NAME" Quizlet2CSV.applescript
mkdir -p "$APP_NAME/Contents/Resources"
cp quizlet_html_to_csv.py "$APP_NAME/Contents/Resources/"

# osacompile sets CFBundleIconName, which makes macOS render the icon from
# the compiled Assets.car catalog instead of the loose .icns file below.
# Strip it so CFBundleIconFile (droplet.icns) is authoritative.
/usr/libexec/PlistBuddy -c "Delete :CFBundleIconName" "$APP_NAME/Contents/Info.plist" 2>/dev/null || true

if [ -f "$ICON_SRC" ]; then
	echo "Applying custom icon from $ICON_SRC..."
	WORKDIR=$(mktemp -d)
	ICONSET_DIR="$WORKDIR/icon.iconset"
	mkdir -p "$ICONSET_DIR"
	for size in 16 32 128 256 512; do
		double=$((size * 2))
		sips -z "$size" "$size" "$ICON_SRC" --out "$ICONSET_DIR/icon_${size}x${size}.png" >/dev/null
		sips -z "$double" "$double" "$ICON_SRC" --out "$ICONSET_DIR/icon_${size}x${size}@2x.png" >/dev/null
	done
	iconutil -c icns "$ICONSET_DIR" -o "$WORKDIR/icon.icns"
	cp "$WORKDIR/icon.icns" "$APP_NAME/Contents/Resources/droplet.icns"
	touch "$APP_NAME"
	rm -rf "$WORKDIR"
else
	echo "No icon.png found — using the default AppleScript icon."
	echo "Drop a square 1024x1024 icon.png in this folder and rebuild to customize it."
fi

echo "Built $APP_NAME"
echo "Drag it into /Applications, or just leave it here and drag HTML files onto it."
