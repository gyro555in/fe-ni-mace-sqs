#!/usr/bin/env python3
"""Download and verify the Fe-Ni MACE-sqs files from Zenodo (doi:10.5281/zenodo.23484911).

Standard library only. Files go to ./data, are checked against checksums.md5,
and zip archives are extracted into ./data/<archive-name>/.
"""
import argparse
import hashlib
import sys
import urllib.request
import zipfile
from pathlib import Path

RECORD_ID = "23484911"
BASE_URL = f"https://zenodo.org/records/{RECORD_ID}/files"
ROOT = Path(__file__).resolve().parent
MODEL = "MACE-sqs.model"


def load_checksums():
    sums = {}
    for line in (ROOT / "checksums.md5").read_text().splitlines():
        if line.strip():
            md5, name = line.split()
            sums[name] = md5
    return sums


def md5sum(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def download(name, dest):
    url = f"{BASE_URL}/{name}?download=1"
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(url) as r, open(tmp, "wb") as f:
        total = int(r.headers.get("Content-Length", 0))
        done = 0
        while True:
            block = r.read(1 << 20)
            if not block:
                break
            f.write(block)
            done += len(block)
            if total:
                print(f"\r  {name}: {done / total:6.1%} of {total / 1e6:,.1f} MB", end="", flush=True)
    print()
    tmp.rename(dest)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--skip-model", action="store_true", help=f"do not download {MODEL} (1.5 GB)")
    p.add_argument("--no-extract", action="store_true", help="keep zip archives packed")
    p.add_argument("--outdir", default=str(ROOT / "data"))
    args = p.parse_args()

    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    failed = []

    for name, expected in load_checksums().items():
        if args.skip_model and name == MODEL:
            print(f"skipping {name}")
            continue
        dest = out / name
        if dest.exists() and md5sum(dest) == expected:
            print(f"ok (cached) {name}")
        else:
            print(f"downloading {name}")
            download(name, dest)
            if md5sum(dest) != expected:
                print(f"  MD5 MISMATCH for {name}", file=sys.stderr)
                failed.append(name)
                continue
            print(f"  verified {name}")
        if name.endswith(".zip") and not args.no_extract:
            with zipfile.ZipFile(dest) as z:
                z.extractall(out / name[:-4])

    if failed:
        sys.exit(f"checksum failures: {', '.join(failed)}")
    print(f"done, files in {out}")


if __name__ == "__main__":
    main()
