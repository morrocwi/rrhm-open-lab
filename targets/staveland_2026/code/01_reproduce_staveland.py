#!/usr/bin/env python3
"""R0 scaffold — selective access to Zenodo 17726565 (77 GB single archive).

Status: SCAFFOLD. R0 has NOT been run; nothing here produces citable output yet.
Strategy: the archive is one zip; we read its END-OF-CENTRAL-DIRECTORY via HTTP range
requests to enumerate members WITHOUT downloading 77 GB, then fetch only the behavioral
and electrode-localization members. iEEG members are fetched per-analysis later.
The authors' own analysis code (per the paper's code-availability statement) is used for
the published pipelines; it is referenced by URL+commit, not copied.
"""
import struct
import urllib.request

URL = ("https://zenodo.org/api/records/17726565/files/"
       "minimally_processed_ieeg_data.zip/content")

def fetch_range(url, start, end):
    req = urllib.request.Request(url, headers={"Range": f"bytes={start}-{end}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()

def total_size(url):
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(r.headers["Content-Length"])

def list_members(url, tail_bytes=10 * 1024 * 1024):
    """Read the zip central directory from the archive tail; return (name, offset, csize,
    method) tuples. Handles zip64. Raises if the server ignores Range requests."""
    size = total_size(url)
    tail = fetch_range(url, max(0, size - tail_bytes), size - 1)
    if len(tail) >= size - max(0, size - tail_bytes) and len(tail) > tail_bytes:
        raise RuntimeError("server ignored Range request; selective fetch unavailable")
    # find EOCD / zip64 EOCD locator and parse central directory (implementation to be
    # completed at R0 execution time; kept minimal here so the scaffold stays honest
    # about what has actually run).
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0:
        raise RuntimeError("EOCD not found in tail window")
    cd_size, cd_off = struct.unpack("<II", tail[eocd + 12:eocd + 20])
    print(f"archive size {size / 1e9:.1f} GB; central dir {cd_size} B @ {cd_off}")
    return size, cd_size, cd_off

if __name__ == "__main__":
    print("R0 scaffold — enumerating archive members via HTTP range:")
    print(list_members(URL))
    print("NEXT (unrun): parse central directory, extract behavioral + localization "
          "members only, then run the authors' published pipelines.")
