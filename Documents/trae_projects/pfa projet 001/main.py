# ================================================================
#   PROJET DE FIN D'ANNÉE — Automatisation des Ventes
#   Matière : Logiciels
#   Description : Analyse automatique d'un fichier CSV de ventes
# ================================================================

import csv
import sys
from pathlib import Path

# ── Configuration globale ────────────────────────────────────────
TVA_TAUX    = 0.20
FICHIER_IN  = Path("ventes.csv")
FICHIER_OUT = Path("resultats_final.csv")

DONNEES_INITIALES = [
    [101, 15.0, 3, 10],
    [102, 25.0, 2,  5],
    [103, 10.0, 5,  0],
    [104, 30.0, 1, 15],
    [105, 18.0, 4,  8],
    [106, 45.0, 2, 20],
    [107, 12.5, 6,  0],
]

# ── Utilitaires d'affichage ──────────────────────────────────────
SEPARATEUR = "=" * 52

def titre(texte):
    print(f"\n{SEPARATEUR}")
    print(f"  {texte}")
    print(SEPARATEUR)

def ok(message):
    print(f"  [OK]  {message}")

def info(message):
    print(f"  [>>]  {message}")

def alerte(message):
    print(f"  [!!]  {message}", file=sys.stderr)



# ÉTAPE 1 — Génération du fichier ventes.csv


def generer_fichier_csv(chemin: Path, donnees: list) -> None:
    """Génère le fichier CSV source à partir des données initiales."""
    with chemin.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Prix", "Quantite", "Remise"])
        writer.writerows(donnees)
    ok(f"'{chemin}' généré ({len(donnees)} produits).")



# ÉTAPES 2–4 — Lecture + Calculs (CA Brut, CA Net, TVA)


def calculer_resultats(chemin: Path) -> list[dict]:
    
    resultats = []

    with chemin.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for numero_ligne, ligne in enumerate(reader, start=2):
            try:
                id_produit = ligne["ID"]
                prix       = float(ligne["Prix"])
                quantite   = int(ligne["Quantite"])
                remise     = float(ligne["Remise"])

                # Validation des valeurs
                if prix < 0 or quantite < 0:
                    raise ValueError("Prix ou quantité négatif.")
                if not (0 <= remise <= 100):
                    raise ValueError(f"Remise invalide ({remise}%).")

                # Calculs
                ca_brut = prix * quantite
                ca_net  = ca_brut * (1 - remise / 100)
                tva     = ca_net * TVA_TAUX
                ca_ttc  = ca_net + tva

                resultats.append({
                    "ID":       id_produit,
                    "Prix":     prix,
                    "Quantite": quantite,
                    "Remise":   remise,
                    "CA_Brut":  round(ca_brut, 2),
                    "CA_Net":   round(ca_net,  2),
                    "TVA":      round(tva,     2),
                    "CA_TTC":   round(ca_ttc,  2),
                })

            except (ValueError, KeyError) as e:
                alerte(f"Ligne {numero_ligne} ignorée — {e}")

    ok(f"{len(resultats)} ligne(s) calculée(s) avec succès.")
    return resultats



# ÉTAPE 5 — Affichage du CA Total


def afficher_totaux(resultats: list[dict]) -> None:
    
    total_brut = round(sum(r["CA_Brut"] for r in resultats), 2)
    total_net  = round(sum(r["CA_Net"]  for r in resultats), 2)
    total_tva  = round(sum(r["TVA"]     for r in resultats), 2)
    total_ttc  = round(sum(r["CA_TTC"]  for r in resultats), 2)

    print(f"\n  {'Indicateur':<22} {'Montant':>12}")
    print(f"  {'-'*36}")
    print(f"  {'CA Brut Total':<22} {total_brut:>11.2f} DT")
    print(f"  {'CA Net Total':<22} {total_net:>11.2f} DT")
    print(f"  {'TVA Totale':<22} {total_tva:>11.2f} DT")
    print(f"  {'CA TTC Total':<22} {total_ttc:>11.2f} DT")


def afficher_ca_total(resultats: list[dict]) -> float:
    """Affiche le Chiffre d'Affaires total TTC."""
    total = sum(r["CA_TTC"] for r in resultats)
    print(f"\n{'='*45}")
    print(f"  CA Total (TTC) de l'entreprise : {total:.2f} €")
    print(f"{'='*45}")
    return total



# ÉTAPE 6 — Produit avec le plus gros bénéfice


def afficher_meilleur_produit(resultats: list[dict]) -> None:
    
    if not resultats:
        alerte("Aucune donnée disponible.")
        return

    meilleur = max(resultats, key=lambda r: r["CA_Net"])

    info("En l'absence du coût d'achat, le bénéfice est assimilé au CA Net.")
    print(f"\n  ID Produit   : {meilleur['ID']}")
    print(f"  Prix unitaire: {meilleur['Prix']:.2f} DT")
    print(f"  Quantité     : {meilleur['Quantite']}")
    print(f"  Remise       : {meilleur['Remise']:.0f}%")
    print(f"  CA Net       : {meilleur['CA_Net']:.2f} DT")
    print(f"  CA TTC       : {meilleur['CA_TTC']:.2f} DT")



# ÉTAPE 7 — Export de resultats_final.csv


def exporter_resultats(resultats: list[dict], chemin: Path) -> None:
    
    champs = ["ID", "Prix", "Quantite", "Remise",
              "CA_Brut", "CA_Net", "TVA", "CA_TTC"]

    with chemin.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=champs)
        writer.writeheader()
        writer.writerows(resultats)

    ok(f"'{chemin}' exporté ({len(resultats)} ligne(s)).")



#  — Graphiques Matplotlib


def afficher_graphiques(resultats: list[dict]) -> None:
    try:
        import matplotlib.pyplot as plt

        ids   = [r["ID"]      for r in resultats]
        bruts = [r["CA_Brut"] for r in resultats]
        nets  = [r["CA_Net"]  for r in resultats]
        tvas  = [r["TVA"]     for r in resultats]

        x = range(len(ids))
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
        fig.suptitle("Analyse des Ventes — Chiffre d'Affaires",
                     fontsize=13, fontweight="bold")

        # Graphique 1 : CA Brut vs CA Net
        ax1.bar([i - 0.2 for i in x], bruts, 0.38,
                label="CA Brut", color="#378ADD", alpha=0.9)
        ax1.bar([i + 0.2 for i in x], nets,  0.38,
                label="CA Net",  color="#1D9E75", alpha=0.9)
        ax1.set_xticks(list(x))
        ax1.set_xticklabels(ids)
        ax1.set_title("CA Brut vs CA Net")
        ax1.set_xlabel("ID Produit")
        ax1.set_ylabel("Montant (DT)")
        ax1.legend()
        ax1.grid(axis="y", linestyle="--", alpha=0.4)
        ax1.spines[["top", "right"]].set_visible(False)

        # Graphique 2 : CA Net + TVA empilés
        ax2.bar(ids, nets, label="CA Net",    color="#1D9E75", alpha=0.9)
        ax2.bar(ids, tvas, bottom=nets,
                label="TVA (20%)", color="#D85A30", alpha=0.85)
        ax2.set_title("Décomposition CA Net + TVA")
        ax2.set_xlabel("ID Produit")
        ax2.set_ylabel("Montant (DT)")
        ax2.legend()
        ax2.grid(axis="y", linestyle="--", alpha=0.4)
        ax2.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        plt.savefig("graphiques_ventes.png", dpi=150, bbox_inches="tight")
        plt.show()
        ok("Graphiques enregistrés → graphiques_ventes.png")

    except ImportError:
        alerte("matplotlib non installé. Exécutez : pip install matplotlib")



# — Lecture dynamique (n'importe quelle taille de CSV)


def analyser_csv(chemin: Path) -> list[dict]:
    
    if not chemin.exists():
        alerte(f"Fichier introuvable : {chemin}")
        return []
    return calculer_resultats(chemin)



# PROGRAMME PRINCIPAL


def main():
    titre("ÉTAPE 1 — Génération de ventes.csv")
    generer_fichier_csv(FICHIER_IN, DONNEES_INITIALES)

    titre("ÉTAPES 2–4 — Calculs (CA Brut, CA Net, TVA)")
    resultats = calculer_resultats(FICHIER_IN)

    if not resultats:
        alerte("Aucune donnée valide. Arrêt du programme.")
        sys.exit(1)

    titre("ÉTAPE 5 — CA Total de l'entreprise")
    afficher_ca_total(resultats)

    titre("ÉTAPE 6 — Produit le plus rentable")
    afficher_meilleur_produit(resultats)

    titre("ÉTAPE 7 — Export resultats_final.csv")
    exporter_resultats(resultats, FICHIER_OUT)

    titre("BONUS — Graphiques Matplotlib")
    afficher_graphiques(resultats)

    titre("BONUS — Lecture dynamique")
    donnees_dyn = analyser_csv(FICHIER_IN)
    info(f"{len(donnees_dyn)} ligne(s) relues dynamiquement depuis '{FICHIER_IN}'.")

    titre("TRAITEMENT TERMINÉ")
    ok("Tous les fichiers ont été générés avec succès.")
    info(f"  Fichiers créés : {FICHIER_IN}, {FICHIER_OUT}, graphiques_ventes.png")


if __name__ == "__main__":
    main()
