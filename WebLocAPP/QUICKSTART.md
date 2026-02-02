# Démarrage Rapide WebLocAPP

## Installation et lancement en 3 étapes

### 1. Ouvrir le terminal dans le dossier WebLocAPP

```bash
cd /Users/alexandrebonard/Documents/LocApp/WebLocAPP
```

### 2. Lancer le script de démarrage

```bash
./start.sh
```

Le script va automatiquement :
- Créer l'environnement virtuel Python (si nécessaire)
- Installer les dépendances (Flask, etc.)
- Démarrer le serveur web

### 3. Accéder à l'interface

Ouvrez votre navigateur et allez sur :
- **http://localhost:5001**

## Identifiants de connexion

- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `locapp2024`

## Arrêter le serveur

Appuyez sur `CTRL+C` dans le terminal

## Problèmes courants

### Le port 5001 est déjà utilisé

Modifiez le port dans `app.py` (ligne 241) :
```python
app.run(debug=True, host='0.0.0.0', port=5002)  # Changez 5001 en 5002
```

### Erreur "module not found"

Assurez-vous d'être dans l'environnement virtuel :
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Permission refusée pour start.sh

Rendez le script exécutable :
```bash
chmod +x start.sh
```

## Fonctionnalités disponibles

Une fois connecté, vous pouvez administrer :

✅ **Informations générales** - Nom de la propriété, messages de bienvenue
✅ **WiFi** - SSID, mot de passe, description
✅ **Adresse** - Localisation complète
✅ **Parking** - Distance, conseils, tarifs
✅ **Accès** - Horaires check-in/out, codes
✅ **Contact** - Téléphone, email, WhatsApp, Airbnb
✅ **Activités** - Gestion complète des attractions (CRUD)
✅ **Services** - Commerces et services à proximité (CRUD)
✅ **Export JSON** - Pour l'intégration avec l'app iOS

## Export des données

Pour exporter toutes les données en JSON :

1. Allez sur la page d'accueil
2. Cliquez sur "Télécharger l'export JSON"
3. Entrez vos identifiants
4. Le fichier `locapp_data.json` sera téléchargé

Ce fichier peut être utilisé dans votre application iOS Swift.

## Architecture

```
WebLocAPP/
├── app.py              → Serveur Flask (API + Routes)
├── database.py         → Gestion base de données SQLite
├── locapp.db           → Base de données (créée automatiquement)
├── requirements.txt    → Dépendances Python
├── start.sh           → Script de démarrage
├── static/
│   ├── css/style.css  → Styles de l'interface
│   └── js/common.js   → Fonctions JavaScript
└── templates/         → Pages HTML
    ├── index.html
    ├── general.html
    ├── wifi.html
    ├── activities.html
    └── ... (autres pages)
```

## Support

Pour plus d'informations, consultez le fichier `README.md` complet.
