# PCC Valise — Catalogue des simulations

Catalogue public, triable et filtrable, des simulations et paillasses
virtuelles de Physique-Chimie du cycle collégial (1APIC, 2APIC, 3APIC),
extraites de **PCC Valise**.

**173 pages interactives** — 79 simulations, 94 paillasses virtuelles —
chacune un fichier HTML autonome, ouvert directement dans le navigateur.

## Régénérer le catalogue

Le contenu vient de `College valise/simulations/` (projet source, non inclus
ici). Après ajout ou modification de simulations :

```
cd "College valise/app-demo" && node tools/titres.js   # réindexe les titres
python build_catalogue.py                              # copie + data.js
python build_thumbnails.py                              # vignette PNG par simulation
```

`build_catalogue.py` lit `simulations/_titres.json`, ne retient que les
fichiers canoniques (`simulation_*.html` et `enhanced_simulation_*.html`,
hors `.bak`), et écrit :

- `sims/<niveau>/<leçon>/<fichier>.html` — une copie de chaque simulation ;
- `data.js` — le manifeste que lit `index.html` (id, niveau, leçon, type,
  titre, chemin).

**Rien ne se corrige dans `sims/` ni dans `data.js`** : ils sont régénérés
en entier à chaque exécution du script.

`build_thumbnails.py` capture ensuite une vignette par simulation — Chrome
headless, `--screenshot`, 900×620 — dans `thumbs/<niveau>/<id>-<type>.png`,
et ajoute le champ `vignette` à chaque entrée de `data.js`. **Une vignette
déjà présente n'est pas régénérée** : supprimer `thumbs/` force une capture
complète. Prévoir quelques minutes pour les ~170 captures au premier passage.

## Structure

```
index.html          le catalogue (HTML/CSS/JS autonome, pas de dépendance externe)
data.js              le manifeste des 173 simulations (titres + vignettes)
sims/                les fichiers, par niveau puis par leçon
thumbs/              une vignette PNG par simulation
build_catalogue.py   copie les simulations et écrit data.js
build_thumbnails.py  capture les vignettes
```

Aucune étape de build côté serveur : GitHub Pages sert ces fichiers tels quels.
