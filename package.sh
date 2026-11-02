#!/bin/sh
# Build the mod and lay out the toolbox SD card: build/sd/custom/ goes to the root of the card
# next to the MIB STD2 toolbox's own custom/ directory, then GEM -> Customization -> Cluster
# navigation -> Install.
#   MIBHMI=<MIBHMI.jar converted from your unit's MIBHMI.jxe> JAVAC=<JDK 8 javac> ./package.sh
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
if [ -n "${MIBHMI:-}" ]; then
    "$HERE/hmi/build.sh"
elif [ -f "$HERE/prebuilt/mst2-zr-nar-carplay-maps.jar" ]; then
    mkdir -p "$HERE/hmi/build"
    cp "$HERE/prebuilt/mst2-zr-nar-carplay-maps.jar" "$HERE/hmi/build/mst2-zr-nar-carplay-maps.jar"
else
    echo "No HMI build available. Set MIBHMI to a P0367T MIBHMI.jar." >&2
    exit 1
fi
"$HERE/native/build.sh"
SD="$HERE/build/sd"
rm -rf "$SD"
mkdir -p "$SD"
cp -R "$HERE/toolbox/custom" "$SD/custom"
cp "$HERE/hmi/build/mst2-zr-nar-carplay-maps.jar" "$SD/custom/mst2-cluster-nav/mst2-cluster-nav.jar"
for lib in $(awk '!/^#/ && NF == 2 { print $2 }' "$HERE/toolbox/custom/mst2-cluster-nav/preload.list"); do
    cp "$HERE/native/build/$lib" "$SD/custom/mst2-cluster-nav/"
done
(cd "$HERE/build" && rm -f mst2-zr-nar-carplay-maps-p0367t.zip && zip -qr mst2-zr-nar-carplay-maps-p0367t.zip sd)
echo "$HERE/build/mst2-zr-nar-carplay-maps-p0367t.zip"
