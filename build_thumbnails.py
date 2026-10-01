#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Génère une vignette PNG par simulation, via Chrome headless — même
incantation que `topdf.py` du projet Écoles pionnières, en mode
`--screenshot` au lieu de `--print-to-pdf`.

    python build_thumbnails.py

Lit `data.js`, écrit `thumbs/<niveau>/<id>-<type>.png` pour chaque entrée,
et complète chaque entrée de `data.js` avec son chemin de vignette.

Une vignette déjà présente n'est PAS régénérée : seules les simulations
nouvelles ou dont la vignette manque sont capturées. Supprimer `thumbs/`
force une régénération complète.
"""
import json
import os
import re
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
TAILLE = "900,620"


def charger_data():
    with open(os.path.join(ICI, "data.js"), encoding="utf-8") as f:
        s = f.read()
    m = re.search(r"const SIMULATIONS = (\[.*\]);", s, re.S)
    return json.loads(m.group(1))


def ecrire_data(entrees):
    with open(os.path.join(ICI, "data.js"), "w", encoding="utf-8") as f:
        f.write("// Généré par build_catalogue.py puis build_thumbnails.py — ne pas éditer à la main.\n")
        f.write("const SIMULATIONS = ")
        json.dump(entrees, f, ensure_ascii=False, indent=1)
        f.write(";\n")


def capturer(html_abs, png_abs):
    url = "file:///" + html_abs.replace("\\", "/")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         "--window-size=" + TAILLE, "--screenshot=" + png_abs.replace("\\", "/"), url],
        check=True, capture_output=True, timeout=25,
    )


def main():
    entrees = charger_data()
    os.makedirs(os.path.join(ICI, "thumbs"), exist_ok=True)

    total = len(entrees)
    faites, manquees = 0, []
    t0 = time.time()

    for i, e in enumerate(entrees, 1):
        rel = "thumbs/%s/%s-%s.png" % (e["niveau"], e["id"], e["type"])
        dst = os.path.join(ICI, rel.replace("/", os.sep))
        e["vignette"] = rel

        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            continue

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        src = os.path.join(ICI, e["fichier"].replace("/", os.sep))
        try:
            capturer(src, dst)
            faites += 1
        except Exception as ex:
            manquees.append((e["id"], e["type"], str(ex)[:120]))
            e["vignette"] = None

        if i % 20 == 0 or i == total:
            print("  %3d / %d  (%.0f s écoulées)" % (i, total, time.time() - t0))

    ecrire_data(entrees)

    print("\n  %d vignette(s) capturée(s), %d déjà présente(s)."
          % (faites, total - faites - len(manquees)))
    if manquees:
        print("  %d échec(s) :" % len(manquees))
        for id_, type_, err in manquees:
            print("    - %s (%s) : %s" % (id_, type_, err))


if __name__ == "__main__":
    main()
