def normaliser_email(email: str | None) -> str:
    # Les adresses sont enregistrees et recherchees en minuscules : la casse ne
    # doit jamais distinguer deux comptes. La RFC 5321 rend la partie locale
    # sensible a la casse, mais aucun fournisseur reel ne l'applique.
    return (email or "").strip().lower()
