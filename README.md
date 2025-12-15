# 🎅 QG Secret Santa

Un site web festif et hilarant pour organiser votre Secret Santa en famille !

## ✨ Fonctionnalités

- 🕵️ Thème "agent secret de Noël"
- ❄️ Animation de flocons de neige (cliquez dessus !)
- 🎊 Explosion de confettis à la révélation
- 🔐 Système de "login" avec noms de code rigolos
- 📱 Design responsive

## 🚀 Installation

### 1. Configurer les participants

Éditez le fichier `config.yaml` à la racine du projet :

```yaml
participants:
  - Prénom1
  - Prénom2
  # etc.

# Paires interdites (optionnel) - aucun des deux ne peut offrir à l'autre
exceptions:
  - [Prénom1, Prénom2]  # exemple: couple ou fratrie
```

### 2. Générer les assignations

```bash
pip install pyyaml  # si pas déjà installé
python scripts/generate_santa.py
```

Options :
- `--secret` ou `-s` : Mode secret (l'organisateur ne voit pas les assignations)

### 2. Récupérer les identifiants

Le script affiche les noms de code et mots de passe de chaque participant.
Envoyez à chacun ses identifiants en privé !

### 3. Déployer sur GitHub Pages

1. Créez un repo GitHub
2. Activez Pages dans les paramètres (source: GitHub Actions)
3. Poussez le code :

```bash
git init
git add .
git commit -m "🎄 Ho ho ho!"
git branch -M main
git remote add origin https://github.com/VOTRE_USER/secret-santa.git
git push -u origin main
```

## 🥚 Easter Eggs

- **Code Konami** : ↑↑↓↓←→←→BA
- **Clic sur flocons** : Fait un son !
- **5 échecs de login** : Message spécial
- **Mode admin** : Login `admin` / `perenoel2024`

## 💰 Budget

10 à 20€ (modifiable dans `scripts/generate_santa.py`)

---

Fait avec ❤️ et beaucoup de chocolat chaud 🍫
