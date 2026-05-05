import csv
import os
import sys

TVA_TAUX = 0.20
FICHIER_IN = "ventes.csv"
FICHIER_OUT = "resultats_final.csv"
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
    generer_fichier_csv()
    resultats = calculer_resultats(FICHIER_IN)
    afficher_ca_total(resultats)
    identifier_top_produit(resultats)
    exporter_resultats(resultats)
    afficher_graphiques(resultats)

if __name__ == "__main__":
    main()
