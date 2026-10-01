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
```

`build_catalogue.py` lit `simulations/_titres.json`, ne retient que les
fichiers canoniques (`simulation_*.html` et `enhanced_simulation_*.html`,
hors `.bak`), et écrit :

- `sims/<niveau>/<leçon>/<fichier>.html` — une copie de chaque simulation ;
- `data.js` — le manifeste que lit `index.html` (id, niveau, leçon, type,
  titre, chemin).

**Rien ne se corrige dans `sims/` ni dans `data.js`** : ils sont régénérés
en entier à chaque exécution du script.

## Structure

```
index.html     le catalogue (HTML/CSS/JS autonome, pas de dépendance externe)
data.js        le manifeste des 173 simulations
sims/          les fichiers, par niveau puis par leçon
```

Aucune étape de build côté serveur : GitHub Pages sert ces fichiers tels quels.
