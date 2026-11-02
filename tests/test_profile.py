import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).parents[1]


class ProfileTests(unittest.TestCase):
    def test_profile_is_locked_to_p0367t(self):
        profile = json.loads((ROOT / "profiles/MST2_US_VW_ZR_P0367T.json").read_text())
        self.assertEqual(profile["release"], "MST2_US_VW_ZR_P0367T")
        self.assertEqual(profile["part_number"], "3G0919360CG")
        self.assertEqual(profile["hmi_version"], "H28.28.197")
        self.assertEqual(len(profile["files"]), 5)
        for item in profile["files"].values():
            self.assertGreater(item["size"], 0)
            self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")
            self.assertGreater(item["cksum"], 0)

    def test_installer_contains_every_profile_cksum(self):
        profile = json.loads((ROOT / "profiles/MST2_US_VW_ZR_P0367T.json").read_text())
        common = (ROOT / "toolbox/custom/greenmenu/scripts/mcn_common.sh").read_text()
        for path, item in profile["files"].items():
            self.assertIn(path, common)
            self.assertIn(f'{item["cksum"]} {item["size"]}', common)

    def test_prebuilt_hmi_hash(self):
        jar = ROOT / "prebuilt/mst2-zr-nar-carplay-maps.jar"
        self.assertEqual(
            hashlib.sha256(jar.read_bytes()).hexdigest(),
            "1940075c6eb5cd8137731160eb38b47d8f695388a656b5024604d55e48115743",
        )

    def test_nar_native_offsets_are_present(self):
        stream = (ROOT / "native/src/sal/stream.c").read_text()
        dm = (ROOT / "native/src/dm/dm.c").read_text()
        for offset in ("0x1142c", "0x17550", "0x17ed0", "0x19480", "0x1a4a4", "0x1e4a0"):
            self.assertIn(offset, stream)
        for offset in ("0x88f4u", "0x8b54u", "0x8e04u", "0x1a3f8u", "0x1262d8u"):
            self.assertIn(offset, dm)


if __name__ == "__main__":
    unittest.main()

