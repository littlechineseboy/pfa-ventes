# Automatisation des Ventes

Projet de Fin d'Année — Matière : Logiciels  
Faculté des Sciences de Tunis — LMASD 2025/2026

## Description

Script Python d'automatisation de l'analyse des ventes pour une entreprise de e-commerce.  
Le script génère un fichier CSV de ventes, effectue les calculs financiers, affiche les résultats et exporte un rapport final.

## Fonctionnalités

- Génération automatique de `ventes.csv`
- Calcul du Chiffre d'Affaires Brut, Net et TTC
- Application des remises et de la TVA (20%)
- Affichage du CA Total de l'entreprise
- Identification du produit le plus rentable
- Export de `resultats_final.csv`
- Visualisation avec deux graphiques Matplotlib

## Structure du projet

| Fichier | Description |
|---|---|
| `main.py` | Script principal |
| `ventes.csv` | Données de ventes générées |
| `resultats_final.csv` | Résultats calculés exportés |
| `graphiques_ventes.png` | Graphiques générés |

##  Installation & Configuration

### 1. Prérequis

- Python **3.10+** installé sur votre machine
- Git installé

### 2. Cloner le dépôt

```bash
git clone https://github.com/littlechineseboy/pfa-ventes
```

### 3. Créer et activer l'environnement virtuel

**Windows (PowerShell) :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

>  Votre terminal affichera `(venv)` devant le prompt une fois activé.

##  Installer les dépendances

```bash
pip install matplotlib
pip install -r requirements.txt
```

## Utilisation

```bash
python main.py
```

## Formules utilisées

| Indicateur | Formule |
|---|---|
| CA Brut | Prix × Quantité |
| CA Net | CA Brut × (1 - Remise / 100) |
| TVA | CA Net × 0.20 |
| CA TTC | CA Net + TVA |

## Équipe

- **Mazen** — Export, graphiques, main()
- **Firas** — Calculs, affichage CA Total, top produit
- **Zyra** — Génération CSV, lecture dynamique
