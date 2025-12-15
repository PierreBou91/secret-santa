#!/usr/bin/env python3
"""
🎅 Générateur de Secret Santa
Crée les assignations aléatoires et génère le fichier JSON pour le site web.
"""

import json
import random
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ Le module PyYAML est requis. Installez-le avec: pip install pyyaml")
    exit(1)


def load_config() -> dict:
    """Charge la configuration depuis config.yaml."""
    config_path = Path(__file__).parent.parent / "config.yaml"
    
    if not config_path.exists():
        print(f"❌ Fichier de configuration introuvable: {config_path}")
        print("   Créez un fichier config.yaml à la racine du projet.")
        exit(1)
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_codename(config: dict) -> str:
    """Génère un nom de code avec accord grammatical français."""
    prefixes = config["codenames"]["prefixes"]
    suffixes = config["codenames"]["suffixes"]
    
    # Choisir un préfixe aléatoire: [mot, genre]
    prefix_word, gender = random.choice(prefixes)
    
    # Choisir un suffixe et accorder selon le genre: [masculin, féminin]
    suffix_forms = random.choice(suffixes)
    suffix_word = suffix_forms[0] if gender == "m" else suffix_forms[1]
    
    number = random.randint(10, 99)
    return f"{prefix_word}{suffix_word}{number}"


def generate_password(config: dict) -> str:
    """Génère un mot de passe thématique."""
    passwords = config.get("passwords", ["secret"])
    return random.choice(passwords) + str(random.randint(1, 99))


def assign_secret_santas(participants: list[str], exceptions: list[list[str]]) -> dict[str, str]:
    """
    Assigne aléatoirement un Secret Santa à chaque participant.
    Garantit que:
    - Personne ne s'offre à soi-même
    - Les paires d'exceptions ne sont pas assignées l'une à l'autre
    """
    # Convertir les exceptions en set de tuples pour recherche rapide
    forbidden_pairs = set()
    for exc in exceptions:
        if len(exc) == 2:
            forbidden_pairs.add((exc[0], exc[1]))
            forbidden_pairs.add((exc[1], exc[0]))
    
    max_attempts = 1000
    for attempt in range(max_attempts):
        shuffled = participants.copy()
        random.shuffle(shuffled)
        
        # Décalage simple : chaque personne offre à la suivante
        assignments = {}
        valid = True
        
        for i, giver in enumerate(shuffled):
            receiver = shuffled[(i + 1) % len(shuffled)]
            
            # Vérifier les contraintes
            if giver == receiver:
                valid = False
                break
            if (giver, receiver) in forbidden_pairs:
                valid = False
                break
            
            assignments[giver] = receiver
        
        if valid:
            return assignments
    
    # Si on n'a pas trouvé de solution après max_attempts, 
    # utiliser un algorithme plus sophistiqué
    print("⚠️  Algorithme simple échoué, tentative avec backtracking...")
    return assign_with_backtracking(participants, forbidden_pairs)


def assign_with_backtracking(participants: list[str], forbidden_pairs: set) -> dict[str, str]:
    """
    Algorithme de backtracking pour les cas difficiles avec beaucoup d'exceptions.
    """
    n = len(participants)
    assignments = {}
    available_receivers = set(participants)
    
    def backtrack(index: int) -> bool:
        if index == n:
            # Vérifier que le dernier peut donner au premier (cycle complet)
            return True
        
        giver = participants[index]
        candidates = list(available_receivers)
        random.shuffle(candidates)
        
        for receiver in candidates:
            if receiver == giver:
                continue
            if (giver, receiver) in forbidden_pairs:
                continue
            
            assignments[giver] = receiver
            available_receivers.remove(receiver)
            
            if backtrack(index + 1):
                return True
            
            # Backtrack
            del assignments[giver]
            available_receivers.add(receiver)
        
        return False
    
    random.shuffle(participants)
    if backtrack(0):
        return assignments
    else:
        print("❌ Impossible de trouver une assignation valide avec les exceptions données.")
        print("   Vérifiez que les exceptions ne rendent pas l'assignation impossible.")
        exit(1)


def generate_json(config: dict, secret_mode: bool = False):
    """Génère le fichier JSON avec toutes les assignations."""
    
    participants = config["participants"]
    exceptions = config.get("exceptions", [])
    event = config.get("event", {"name": "Secret Santa 🎄", "budget": "20€"})
    fun_messages = config.get("fun_messages", ["🎁 Tu offres à"])
    
    print("🎅 Génération des assignations Secret Santa...")
    print(f"   Participants : {', '.join(participants)}")
    
    if exceptions:
        print(f"   Exceptions : {len(exceptions)} paire(s) interdite(s)")
    
    if secret_mode:
        print("\n🤫 MODE SECRET ACTIVÉ - Les assignations ne seront PAS affichées !")
    
    # Assigner les Secret Santas
    assignments = assign_secret_santas(participants, exceptions)
    
    # Créer les données pour chaque participant
    participants_data = []
    used_codenames = set()
    used_passwords = set()
    
    for name, giftee in assignments.items():
        # Générer un nom de code unique
        codename = generate_codename(config)
        while codename in used_codenames:
            codename = generate_codename(config)
        used_codenames.add(codename)
        
        # Générer un mot de passe unique
        password = generate_password(config)
        while password in used_passwords:
            password = generate_password(config)
        used_passwords.add(password)
        
        participants_data.append({
            "codename": codename,
            "password": password,
            "realName": name,
            "giftee": giftee,
            "funMessage": random.choice(fun_messages)
        })
    
    # Structure finale
    data = {
        "event": event,
        "participants": participants_data
    }
    
    # Créer le dossier data s'il n'existe pas
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "assignments.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Fichier généré : {output_file}")
    
    # Générer le fichier des identifiants (sans révéler les assignations)
    credentials_file = output_dir / "credentials.txt"
    with open(credentials_file, "w", encoding="utf-8") as f:
        f.write("🎅 IDENTIFIANTS SECRET SANTA 🎅\n")
        f.write("=" * 40 + "\n\n")
        f.write("Envoie à chaque personne ses identifiants en privé !\n\n")
        for p in participants_data:
            f.write(f"👤 {p['realName']}\n")
            f.write(f"   Nom de code : {p['codename']}\n")
            f.write(f"   Mot de passe : {p['password']}\n")
            f.write("\n")
    
    print(f"📝 Fichier identifiants : {credentials_file}")
    
    if secret_mode:
        # Mode secret : afficher seulement les identifiants, pas les assignations
        print("\n📋 Identifiants à distribuer (assignations cachées) :")
        print("-" * 40)
        for p in participants_data:
            print(f"   👤 {p['realName']}")
            print(f"      Nom de code : {p['codename']}")
            print(f"      Mot de passe : {p['password']}")
            print()
        print("🎁 Les assignations restent secrètes, même pour toi !")
        print("   Consulte le site avec tes propres identifiants pour découvrir qui tu gâtes 🎄")
    else:
        # Mode normal : tout afficher
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
    import sys
    
    secret_mode = "--secret" in sys.argv or "-s" in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("🎅 Générateur de Secret Santa")
        print()
        print("Usage: python generate_santa.py [OPTIONS]")
        print()
        print("Options:")
        print("  --secret, -s    Mode secret : génère sans révéler les assignations")
        print("                  (pour que l'organisateur puisse aussi participer)")
        print("  --help, -h      Affiche cette aide")
        print()
        print("Configuration:")
        print("  Éditez le fichier config.yaml à la racine du projet pour:")
        print("  - Modifier la liste des participants")
        print("  - Ajouter des exceptions (paires interdites)")
        print("  - Personnaliser les noms de code et mots de passe")
        print()
        print("Exemple:")
        print("  python generate_santa.py --secret")
    else:
        config = load_config()
        generate_json(config, secret_mode=secret_mode)
