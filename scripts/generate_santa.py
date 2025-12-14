#!/usr/bin/env python3
"""
🎅 Générateur de Secret Santa
Crée les assignations aléatoires et génère le fichier JSON pour le site web.
"""

import json
import random
import os
from pathlib import Path

# ============================================
# 🎄 CONFIGURATION - MODIFIER ICI 🎄
# ============================================

# Liste des participants (remplacez par les vrais noms!)
PARTICIPANTS = [
    "Pierre",
    "Gautier",
    "Olivia",
    "Fanny",
    "Anna",
    "Elzéar",
    "Margaux",
    "Ulysse",
]

# Budget à afficher
BUDGET = "10 à 20€"

# Préfixes et suffixes rigolos pour les noms de code
PREFIXES = [
    "Agent", "Lutin", "Renne", "Bonhomme", "Flocon", 
    "Guirlande", "Boule", "Étoile", "Traineau", "Cheminée"
]

SUFFIXES = [
    "Mystère", "Ninja", "Secret", "Festif", "Givré",
    "Enchanté", "Magique", "Doré", "Scintillant", "Joyeux"
]

# Mots de passe rigolos (thème Noël)
PASSWORDS = [
    "hohoho", "renne", "sapin", "guirlande", "chocolat",
    "buche", "cadeau", "neige", "etoile", "reveillon",
    "bonbon", "lutin", "traineau", "chaussette", "houx"
]

# Messages fun pour la révélation
FUN_MESSAGES = [
    "🎁 Mission top secrète : trouver le cadeau parfait pour",
    "🎄 Le destin a parlé ! Tu dois gâter",
    "🦌 Rudolf te confie une mission : faire plaisir à",
    "⭐ Les étoiles se sont alignées ! Tu offres à",
    "🎅 Ho ho ho ! Le Père Noël compte sur toi pour",
    "❄️ Sous le sceau du secret, tu dois choyer",
    "🔔 Ding dong ! C'est l'heure de trouver un cadeau pour",
]


def generate_codename() -> str:
    """Génère un nom de code rigolo."""
    prefix = random.choice(PREFIXES)
    suffix = random.choice(SUFFIXES)
    number = random.randint(10, 99)
    return f"{prefix}{suffix}{number}"


def generate_password() -> str:
    """Génère un mot de passe thématique."""
    return random.choice(PASSWORDS) + str(random.randint(1, 99))


def assign_secret_santas(participants: list[str]) -> dict[str, str]:
    """
    Assigne aléatoirement un Secret Santa à chaque participant.
    Garantit que personne ne s'offre à soi-même.
    """
    while True:
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Décalage simple : chaque personne offre à la suivante
        assignments = {}
        for i, giver in enumerate(shuffled):
            receiver = shuffled[(i + 1) % len(shuffled)]
            assignments[giver] = receiver
        
        # Vérifie que personne ne s'offre à soi-même (ne devrait jamais arriver avec le décalage)
        if all(giver != receiver for giver, receiver in assignments.items()):
            return assignments


def generate_json():
    """Génère le fichier JSON avec toutes les assignations."""
    
    print("🎅 Génération des assignations Secret Santa...")
    print(f"   Participants : {', '.join(PARTICIPANTS)}")
    
    # Assigner les Secret Santas
    assignments = assign_secret_santas(PARTICIPANTS)
    
    # Créer les données pour chaque participant
    participants_data = []
    used_codenames = set()
    used_passwords = set()
    
    for name, giftee in assignments.items():
        # Générer un nom de code unique
        codename = generate_codename()
        while codename in used_codenames:
            codename = generate_codename()
        used_codenames.add(codename)
        
        # Générer un mot de passe unique
        password = generate_password()
        while password in used_passwords:
            password = generate_password()
        used_passwords.add(password)
        
        participants_data.append({
            "codename": codename,
            "password": password,
            "realName": name,
            "giftee": giftee,
            "funMessage": random.choice(FUN_MESSAGES)
        })
    
    # Structure finale
    data = {
        "event": {
            "name": "Secret Santa des Cousins 🎄",
            "budget": BUDGET
        },
        "participants": participants_data
    }
    
    # Créer le dossier data s'il n'existe pas
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "assignments.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fichier généré : {output_file}")
    print("\n📋 Résumé des assignations :")
    print("-" * 40)
    
    for p in participants_data:
        print(f"   {p['realName']:12} → offre à → {p['giftee']}")
        print(f"      Nom de code : {p['codename']}")
        print(f"      Mot de passe : {p['password']}")
        print()
    
    print("🎁 Joyeuses fêtes !")
    
    return data


if __name__ == "__main__":
    generate_json()
