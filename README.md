# MST2-ZR NAR CarPlay Maps

Beta port of CarPlay's second-screen navigation view to the VW Active Info Display / Virtual Cockpit on one North American TechniSat/Preh MIB2 Standard firmware.

## Supported target

| Item | Required value |
|---|---|
| Firmware | `MST2_US_VW_ZR_P0367T` |
| MU | `0367` |
| Part number | `3G0919360CG` |
| HMI | `H28.28.197` |
| Unit | TechniSat/Preh MST2 navigation unit (`T` suffix), not Delphi |

The installer checks the HMI version plus the size and POSIX checksum of five stock files. If any value differs, installation stops before changing the unit. Do not force this package onto another firmware.

## What this beta does

- Adds a 1024×384 CarPlay cluster display while normal CarPlay remains on the radio screen.
- Sends the phone's H.264 stream through the stock FPK, J5 and MOST path.
- Supports Apple Maps, Google Maps and Waze when they provide the CarPlay secondary display.
- Feeds supported CarPlay maneuvers and lane guidance into the cluster's native widgets.
- Uses a one-boot trial first, keeps stock backups, includes an emergency kill switch and can be uninstalled.

This is the first NAR port and has not yet been tested in a vehicle. The source, HMI overlay and native ABI profile were validated against the supplied P0367T firmware, but QNX emulation cannot reproduce the vehicle's J5/MOST controller, cluster timing or a real iPhone session.

Android Auto map video is not included. Android Auto does not expose the same CarPlay second-screen stream on this platform; metadata/arrows are a separate project.

## Before you start

You need:

- The exact supported firmware shown above.
- A working installation of [MIB STD2 Toolbox](https://github.com/olli991/mib-std2-pq-zr-toolbox) with its Green Engineering Menu.
- The beta ZIP from this repository's Releases page.
- A known-good SD card and a saved copy of your unit's original files.
- Stable vehicle power. Do not install or test while driving.

If your unit is Delphi, has a different train, lacks factory navigation, or reports a different HMI version, stop.

## Install the beta

1. Download `mst2-zr-nar-carplay-maps-p0367t.zip` from the latest release.
2. Extract the ZIP. Open its `sd` folder.
3. Merge the `custom` folder into the root of your existing MIB STD2 Toolbox SD card. Keep the Toolbox files already on the card.
4. Insert the card into the head unit and open the Green Engineering Menu.
5. Open **Customization → Cluster navigation**.
6. Choose **Install**. Read the result on screen. A mismatch must end with `Aborted`; do not try to bypass it.
7. When installation reports success, reboot the unit. This next boot is a temporary trial.
8. Connect an iPhone, start CarPlay navigation, and select the cluster's Navigation view.
9. If the radio, cluster and controls remain stable, return to the same menu and choose **Enable permanently**.

The installer writes stock copies to both `/tsd/var/mst2-cluster-nav/backup` and `mst2-cluster-nav-backup` on the SD card. Keep the SD-card backup.

## Emergency disable and uninstall

For an emergency disable, create an empty file named `mst2-cluster-nav-disable` in the root of the Toolbox SD card, insert it, then boot the unit. The hooks remain inactive.

To remove the beta normally:

1. Open **Customization → Cluster navigation**.
2. Choose **Uninstall**.
3. Wait for the success message, then reboot.

## Tester report

Please include:

- Software train, MU, part number and HMI version.
- Vehicle, model year and cluster part number.
- iPhone model, iOS version and navigation app.
- Whether the main CarPlay screen, cluster map, native arrows and lane guidance worked.
- The contents of `/tsd/var/mst2-cluster-nav/log` after reproducing the issue.
- Whether reboot, emergency disable and uninstall worked.

Do not upload firmware or other proprietary binaries.

## Build from source

On Linux with Python 3, Clang, LLD and `zip`:

```sh
python3 -m unittest discover -s tests -v
./native/check.sh
CLANG=clang LLD=ld.lld ./package.sh
```

The release uses the included HMI overlay, which contains only this project's compiled classes. To rebuild it, set `MIBHMI` to a JAR converted from your own P0367T `MIBHMI.jxe` and use JDK 8.

## Credits and license

This is an adaptation of [perkthefox/mst2-cluster-nav](https://github.com/perkthefox/mst2-cluster-nav), with protocol and implementation work also informed by [1mikew/mst2-altscreen-carplay](https://github.com/1mikew/mst2-altscreen-carplay) and [MrGame11/mib-std2-AAtoKombi](https://github.com/MrGame11/mib-std2-AAtoKombi).

Copyright © 2026 Anton Perk. Licensed under CC BY-NC-SA 4.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). This NAR adaptation changes the supported firmware profile, native ABI bindings, HMI compatibility, safety preflight and packaging. Commercial use is not permitted by the upstream license.
