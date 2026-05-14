"""
build.py — przygotowuje demo do uruchomienia.

Kopiuje wybrane zdjęcia z folderu Kosciol/content/galeria/.../assets/
do demo-parafia-v2/public/img/ pod prostymi, łatwymi do podmiany nazwami.

Uruchomienie:
    python build.py
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_BASE = ROOT / "Kosciol" / "content" / "galeria"
DST = Path(__file__).resolve().parent / "public" / "img"

# Mapowanie: nazwa-docelowa.jpg  ->  ścieżka źródłowa (relatywna od SRC_BASE)
MAPPING: dict[str, str] = {
    # hero slider — 100 lat parafii (2025)
    "hero-1.jpg": "100-lat-parafii-01-08-2025-r.html/assets/mini25-08-30-14-45-25-photo-2025-08-02-14-18-38.jpg",
    "hero-2.jpg": "100-lat-parafii-01-08-2025-r.html/assets/mini25-08-30-14-45-48-photo-2025-08-02-14-20-42.jpg",
    "hero-3.jpg": "100-lat-parafii-01-08-2025-r.html/assets/mini25-08-30-14-46-04-photo-2025-08-02-14-20-43.jpg",

    # wizytacja 2025
    "event-wizytacja-1.jpg": "wizytacja-kanoniczna-2025-r.html/assets/mini25-05-09-16-20-24-5d4a3635.jpg",
    "event-wizytacja-2.jpg": "wizytacja-kanoniczna-2025-r.html/assets/mini25-05-09-16-20-25-5d4a3638.jpg",
    "event-wizytacja-3.jpg": "wizytacja-kanoniczna-2025-r.html/assets/mini25-05-09-16-20-26-5d4a3645.jpg",
    "event-wizytacja-4.jpg": "wizytacja-kanoniczna-2025-r.html/assets/mini25-05-09-16-20-27-5d4a3665.jpg",

    # budowa nowego kościoła
    "budowa-1.jpg": "nowy-kosciol-i-podziemia-stan-05-03-2025.html/assets/mini25-03-07-13-49-16-img_3218.jpg",
    "budowa-2.jpg": "nowy-kosciol-i-podziemia-stan-05-03-2025.html/assets/mini25-03-07-13-49-17-img_3219.jpg",
    "budowa-3.jpg": "nowy-kosciol-i-podziemia-stan-05-03-2025.html/assets/mini25-03-07-13-49-18-img_3228.jpg",
    "budowa-4.jpg": "nowy-kosciol-i-podziemia-stan-05-03-2025.html/assets/mini25-03-07-13-49-18-img_3229.jpg",

    # pożegnanie księdza Antoniego
    "event-pozegnanie-1.jpg": "zegnamy-ksiedza-antoniego.html/assets/mini23-09-06-18-13-11-photo-2023-09-05-11-36-58_1.jpg",
    "event-pozegnanie-2.jpg": "zegnamy-ksiedza-antoniego.html/assets/mini23-09-06-18-13-12-photo-2023-09-05-11-36-58.jpg",

    # historia / noclegownia
    "noclegownia.jpg": "noclegownia-budynek-starego-kosciola.html/assets/mini23-06-22-12-18-13-noclegownia.jpg",

    # suma odpustowa
    "event-odpust-1.jpg": "suma-odpustowa-09-06-2024r.html/assets/mini24-06-13-19-13-46-katarzyna-gudzik-85.jpg",
    "event-odpust-2.jpg": "suma-odpustowa-09-06-2024r.html/assets/mini24-06-13-19-13-50-katarzyna-gudzik-87.jpg",
    "event-odpust-3.jpg": "suma-odpustowa-09-06-2024r.html/assets/mini24-06-13-19-13-53-katarzyna-gudzik-90.jpg",
    "event-odpust-4.jpg": "suma-odpustowa-09-06-2024r.html/assets/mini24-06-13-19-13-55-katarzyna-gudzik-93.jpg",
}


def main() -> None:
    if not SRC_BASE.exists():
        sys.exit(f"Brak folderu źródłowego: {SRC_BASE}")
    DST.mkdir(parents=True, exist_ok=True)

    print(f"Kopiuję zdjęcia do: {DST}")
    print("-" * 70)
    ok = 0
    missing = []
    for dst_name, src_rel in MAPPING.items():
        src = SRC_BASE / src_rel
        dst = DST / dst_name
        if not src.exists():
            print(f"  BRAK   {dst_name:<28} <- {src_rel}")
            missing.append((dst_name, src_rel))
            continue
        shutil.copy2(src, dst)
        size_kb = dst.stat().st_size // 1024
        print(f"  OK     {dst_name:<28} <- {src_rel} ({size_kb} KB)")
        ok += 1

    print("-" * 70)
    print(f"Skopiowane: {ok}/{len(MAPPING)}")
    if missing:
        print(f"\nUWAGA — {len(missing)} plików nie istnieje. Demo będzie miało puste obrazki w tych miejscach:")
        for name, rel in missing:
            print(f"  - {name}")


if __name__ == "__main__":
    main()
