from pathlib import Path
import csv
import os
import sys



TVA_TAUX = 0.20
FICHIER_IN = "ventes.csv"
FICHIER_OUT = "resultats_final.csv"


FICHIER_IN = Path("ventes.csv")
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


def generer_fichier_csv(chemin: Path, donnees: list) -> None:
    """Génère le fichier CSV source à partir des données initiales."""
    with chemin.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Prix", "Quantite", "Remise"])
        writer.writerows(donnees)
    print(f"'{chemin}' généré ({len(donnees)} produits).")

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
                print(f"Ligne {numero_ligne} ignorée — {e}")

    print (f"{len(resultats)} ligne(s) calculée(s) avec succès.")
    return resultats
def afficher_ca_total(resultats):
    total = sum(r["CA_TTC"] for r in resultats)
    print(f"\n{'='*45}")
    print(f" CA Total (TTC) de l'entreprise : {total:.2f} DT")
    print(f"{'='*45}")
    return total

def identifier_top_produit(resultats):
    top = max(resultats, key=lambda r: r["CA_Net"])
    print(f"\n[TOP] Produit avec le plus gros bénéfice : ")
    print(f" ID={top['ID']} | CA Net={top['CA_Net']:.2f} DT | CA TTC={top['CA_TTC']:.2f} DT")
    return top

def exporter_resultats(resultats, chemin=FICHIER_OUT):
    colonnes = ["ID", "Prix", "Quantite", "Remise", "CA_Brut", "CA_Net", "TVA", "CA_TTC"]
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(resultats)
    print(f"[OK] Résultats exportés dans '{chemin}'.")

def afficher_graphiques(resultats):
    import matplotlib.pyplot as plt

    ids   = [r["ID"] for r in resultats]
    bruts = [r["CA_Brut"] for r in resultats]
    nets  = [r["CA_Net"] for r in resultats]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    x = range(len(ids))
    ax1.bar([i - 0.2 for i in x], bruts, 0.4, label="CA Brut", color="#378ADD")
    ax1.bar([i + 0.2 for i in x], nets,  0.4, label="CA Net",  color="#1D9E75")
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(ids)
    ax1.set_title("CA Brut vs CA Net par produit")
    ax1.set_xlabel("ID Produit")
    ax1.set_ylabel("Montant (DT)")
    ax1.legend()
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    ranked      = sorted(resultats, key=lambda r: r["CA_Net"])
    ranked_ids  = [r["ID"] for r in ranked]
    ranked_nets = [r["CA_Net"] for r in ranked]
    ax2.barh(ranked_ids, ranked_nets, color="#E07B3F")
    ax2.set_title("Classement CA Net par produit")
    ax2.set_xlabel("CA Net (DT)")
    ax2.grid(axis="x", linestyle="--", alpha=0.4)

    plt.tight_layout()
    plt.savefig("graphiques_ventes.png", dpi=150)
    plt.show()
    print("[OK] Graphiques sauvegardés → graphiques_ventes.png")

def main():
    generer_fichier_csv(FICHIER_IN, DONNEES_INITIALES)
    resultats = calculer_resultats(FICHIER_IN)
    afficher_ca_total(resultats)
    identifier_top_produit(resultats)
    exporter_resultats(resultats)
    afficher_graphiques(resultats)

if __name__ == "__main__":
    main()
