#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construit le dépôt du catalogue de simulations : copie les fichiers
canoniques (simulation_*.html / enhanced_simulation_*.html, hors .bak),
génère data.js, et laisse index.html/README déjà écrits à côté.

Lit  : simulations/_titres.json (déjà généré par `node tools/titres.js`)
Écrit: <SORTIE>/sims/<niveau>/<lecon>/<fichier>.html
       <SORTIE>/data.js
"""
import json
import os
import re
import shutil

SOURCE = r"C:\Users\uytr\Desktop\CRMEF\الملف التراكمي\College valise\simulations"
SORTIE = r"C:\Users\uytr\AppData\Local\Temp\claude\C--Users-uytr-Desktop--coles-pionni-res\559f65a1-9b3d-4743-969c-f7b945302221\scratchpad\pcc-simulations"

PATTERN = re.compile(
    r"^(?P<niveau>[123]AC)/(?P<lecon>L\d+)/"
    r"(?P<type>enhanced_simulation|simulation)_(?P<id>E[123]AC-\d+)\.html$",
    re.IGNORECASE,
)

NOMS_NIVEAU = {"1AC": "1APIC", "2AC": "2APIC", "3AC": "3APIC"}


def titre_court(titre, type_):
    """« Paillasse virtuelle — E1AC-01 · le test de… » -> « le test de… »
    « Simulation — Test de reconnaissance de l'eau » -> « Test de… »
    Le préfixe est déjà porté par le badge de type dans l'interface ;
    le répéter dans chaque titre de carte serait redondant partout."""
    t = titre
    t = re.sub(r"^Paillasse virtuelle\s*—\s*E[123]AC-\d+\s*·\s*", "", t)
    t = re.sub(r"^Simulation\s*—\s*", "", t)
    t = t.strip() or titre
    return t[:1].upper() + t[1:] if t else t


def main():
    with open(os.path.join(SOURCE, "_titres.json"), encoding="utf-8") as f:
        titres = json.load(f)

    os.makedirs(os.path.join(SORTIE, "sims"), exist_ok=True)
    entrees = []
    doublons_id = {}

    for chemin, titre in sorted(titres.items()):
        chemin_norm = chemin.replace("\\", "/")
        m = PATTERN.match(chemin_norm)
        if not m:
            continue

        niveau, lecon, type_, sim_id = m.group("niveau"), m.group("lecon"), m.group("type"), m.group("id")
        type_norm = "paillasse" if type_.lower() == "enhanced_simulation" else "simulation"

        src = os.path.join(SOURCE, chemin_norm.replace("/", os.sep))
        dst_rel = "sims/%s/%s/%s" % (niveau, lecon, os.path.basename(chemin_norm))
        dst = os.path.join(SORTIE, dst_rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

        cle = (niveau, sim_id, type_norm)
        doublons_id[cle] = doublons_id.get(cle, 0) + 1

        entrees.append({
            "id": sim_id,
            "niveau": niveau,
            "niveau_libelle": NOMS_NIVEAU[niveau],
            "lecon": lecon,
            "lecon_num": int(lecon[1:]),
            "type": type_norm,
            "titre": titre_court(titre, type_norm),
            "titre_complet": titre,
            "fichier": dst_rel,
        })

    dup = {k: v for k, v in doublons_id.items() if v > 1}
    if dup:
        print("  ! doublons détectés (même niveau+id+type) :", dup)

    entrees.sort(key=lambda e: (e["niveau"], e["lecon_num"], e["id"], e["type"]))

    with open(os.path.join(SORTIE, "data.js"), "w", encoding="utf-8") as f:
        f.write("// Généré par build_catalogue.py — ne pas éditer à la main.\n")
        f.write("const SIMULATIONS = ")
        json.dump(entrees, f, ensure_ascii=False, indent=1)
        f.write(";\n")

    par_niveau = {}
    par_type = {}
    for e in entrees:
        par_niveau[e["niveau"]] = par_niveau.get(e["niveau"], 0) + 1
        par_type[e["type"]] = par_type.get(e["type"], 0) + 1

    print("  %d entrées copiées" % len(entrees))
    print("  par niveau :", par_niveau)
    print("  par type   :", par_type)
    taille = sum(os.path.getsize(os.path.join(dp, f))
                 for dp, _, fs in os.walk(os.path.join(SORTIE, "sims")) for f in fs)
    print("  taille sims/ : %.1f Mo" % (taille / 1_000_000))


if __name__ == "__main__":
    main()
