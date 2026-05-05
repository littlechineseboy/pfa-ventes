


DONNEES_INITIALES = [
    [101, 15.0, 3, 10],
    [102, 25.0, 2,  5],
    [103, 10.0, 5,  0],
    [104, 30.0, 1, 15],
    [105, 18.0, 4,  8],
    [106, 45.0, 2, 20],
    [107, 12.5, 6,  0],
]



# ÉTAPE 1 — Génération du fichier ventes.csv


def generer_fichier_csv(chemin: Path, donnees: list) -> None:
    """Génère le fichier CSV source à partir des données initiales."""
    with chemin.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Prix", "Quantite", "Remise"])
        writer.writerows(donnees)
    print(f"'{chemin}' généré ({len(donnees)} produits).")



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

    print(f"{len(resultats)} ligne(s) calculée(s) avec succès.")
    return resultats
