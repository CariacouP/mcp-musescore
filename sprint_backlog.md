# 🏃‍♂️ Agile Sprint Backlog - MCP MuseScore

Document de suivi des Sprints et de l'historique Agile du projet `mcp-musescore`.
Conformément aux règles du projet, l'historique des Sprints validés et clôturés est immuable.

---

## 🎯 Sprint 1 : Nettoyage et Standardisation du Dépôt

- **Statut :** Terminé (Done)
- **Objectif du Sprint :** Aligner la base de code sur les standards stricts définis dans `AGENTS.md` (typage statique complet, déduplication, robustesse sans exception), créer une structure de tests automatisés unifiée et assainir la racine du dépôt.

### User Stories

| ID | Titre | Priorité | Estimation | Statut |
|---|---|---|---|---|
| **US-1.1** | Standardisation du Typage Statique (PEP 484) | Haute | 3 pts | **Done** |
| **US-1.2** | Déduplication du parsing de hauteur LilyPond | Moyenne | 1 pt | **Done** |
| **US-1.3** | Support polyphonique dans les types d'actions (`action_types.py`) | Haute | 1 pt | **Done** |
| **US-1.4** | Organisation des tests & couverture hors-ligne (`tests/`) | Haute | 3 pts | **Done** |
| **US-1.5** | Hygiène du dépôt, organisation des scripts et README | Moyenne | 2 pts | **Done** |

---

### Détail des User Stories

#### US-1.1 : Standardisation du Typage Statique
- **En tant que :** Développeur / Agent IA
- **Je veux :** Des Type Hints systématiques sur tous les paramètres et retours de fonctions dans `src/`
- **Afin de :** Garantir la robustesse de l'autocomplétion, la détection précoce d'erreurs et respecter la règle d'`AGENTS.md`.
- **Critères d'acceptation :**
  - [x] Les fonctions d'initialisation `setup_*_tools` typent le paramètre `mcp` (`FastMCP`) et le retour (`None`).
  - [x] Chaque outil `@mcp.tool()` dispose d'un type de retour explicite (`str` ou `Union[str, Dict[str, Any]]`).
  - [x] `run_and_format_response` dans `response_formatter.py` est typé pour ses entrées et sorties.
  - [x] 0 fonction ou méthode sans retour typé dans `src/`.

#### US-1.2 : Déduplication du parsing de hauteur LilyPond
- **En tant que :** Développeur
- **Je veux :** Réutiliser la fonction canonique `parse_lilypond_pitch` dans `analysis.py`
- **Afin d' :** Éviter la duplication de logique et les divergences potentielles d'octave ou de TPC.
- **Critères d'acceptation :**
  - [x] La fonction locale `_lilypond_to_midi_pitch` dans `src/tools/analysis.py` est remplacée par `parse_lilypond_pitch` de `src.utils.lilypond_writer`.
  - [x] La simulation d'harmonie (`simulate_harmony_changes`) fonctionne à l'identique.

#### US-1.3 : Support polyphonique dans les types d'actions
- **En tant que :** Développeur / Utilisateur de l'API MCP
- **Je veux :** Que `addNoteParams` et `addRestParams` reflètent l'ensemble des champs polyphoniques
- **Afin d' :** Assurer la cohérence des structures de données manipulées par `processSequence` et le writer LilyPond.
- **Critères d'acceptation :**
  - [x] `addNoteParams` intègre `startTick`, `addToChord`, `staff_idx`.
  - [x] `addRestParams` intègre `measure`, `startTick`, `voice`, `staffIdx`, `staff_idx` (ou `total=False`).

#### US-1.4 : Organisation des tests & couverture hors-ligne
- **En tant que :** Mainteneur du projet
- **Je veux :** Un dossier `tests/` standardisé et un test unitaire hors-ligne pour la conversion LilyPond
- **Afin de :** Pouvoir exécuter `python -m unittest discover` ou `pytest` sans dépendance externe à MuseScore.
- **Critères d'acceptation :**
  - [x] Répertoire `tests/` et `tests/fixtures/` créés.
  - [x] `test_lilypond_writer.py` déplacé dans `tests/test_lilypond_writer.py`.
  - [x] Création de `tests/test_lilypond_converter.py` testant `json_to_lilypond` avec un extrait représentatif de `score_dump.json`.
  - [x] Tous les tests s'exécutent avec succès en local et hors-ligne.

#### US-1.5 : Hygiène du dépôt, organisation des scripts et README
- **En tant que :** Utilisateur ou contributeur du dépôt
- **Je veux :** Une racine propre, des scripts utilitaires bien rangés et un README exact
- **Afin d' :** Avoir un dépôt lisible, professionnel et facile à prendre en main.
- **Critères d'acceptation :**
  - [x] `score_dump.json` déplacé dans `tests/fixtures/`.
  - [x] Les scripts `dump_score.py` et `syntax_check.js` sont déplacés dans `scripts/`.
  - [x] Les scripts WebSocket manuels (`test_ws.py`, `test_ws_raw.py`, `test_harmony.py`) sont déplacés dans `scripts/integration/`.
  - [x] Le `README.md` est nettoyé du placeholder ligne 76 et la section tests est actualisée.

---

### Définition de Terminé (Definition of Done - DoD)
- [x] Tous les tests unitaires dans `tests/` passent avec succès (14/14 tests validés).
- [x] Aucun fichier temporaire ou de dump orphelin à la racine.
- [x] Aucune régression sur les fonctionnalités existantes.
- [x] Le code compile sans erreur ni avertissement de syntaxe.
