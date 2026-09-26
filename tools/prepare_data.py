from __future__ import annotations

import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_REPO = PROJECT_ROOT / "ResearchDocuments" / "01_IMPACT" / "code" / "IMPACT"
DOWNLOADER = OFFICIAL_REPO / "tools" / "download_impact.py"
VERIFY = OFFICIAL_REPO / "tools" / "verify_release.py"


def extract_safely(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(archive_path) as archive:
        for item in archive.infolist():
            target = (destination / item.filename).resolve()
            if target != root and root not in target.parents:
                raise ValueError(f"Archive member escapes extraction root: {item.filename}")
        archive.extractall(destination)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch, verify and extract the official IMPACT v1.1 quick-start sample.")
    parser.add_argument("--archive", type=Path, default=None, help="Use an already downloaded sample archive")
    parser.add_argument("--skip-extract", action="store_true")
    args = parser.parse_args()
    raw_root = PROJECT_ROOT / "data" / "raw" / "impact"
    if args.archive:
        archive_path = args.archive.resolve()
    else:
        subprocess.run([sys.executable, str(DOWNLOADER), "--include", "sample", "--output", str(raw_root)], check=True)
        archive_path = raw_root / "v1.1" / "sample" / "IMPACT-v1.1-sample.zip"
    if not archive_path.is_file():
        raise FileNotFoundError(archive_path)
    if args.archive:
        checksums = raw_root / "v1.1" / "SHA256SUMS"
        if checksums.is_file():
            subprocess.run([sys.executable, str(VERIFY), str(archive_path), "--checksums", str(checksums)], check=True)
        else:
            with zipfile.ZipFile(archive_path) as archive:
                if archive.testzip():
                    raise ValueError("Sample archive has a CRC failure")
    print(f"[ok] verified official archive: {archive_path}")
    if not args.skip_extract:
        destination = PROJECT_ROOT / "data" / "processed" / "impact" / "v1.1"
        extracted = destination / "IMPACT-v1.1" / "sample" / "videos" / "front"
        if extracted.is_dir() and any(extracted.glob("*.mp4")):
            print(f"[ok] extracted sample already present: {extracted}")
        else:
            extract_safely(archive_path, destination)
            print(f"[ok] extracted sample: {destination}")


if __name__ == "__main__":
    main()
