# supat-app
Une plateforme ideale pour la collecte et l'analyse descriptive des donnees des patients dans un hopital.
📌 README.md
# 🏥 SUPAT Hospital Pro

SUPAT Hospital Pro est une application web de gestion hospitalière intelligente développée avec **Flet (Python)** et **PostgreSQL**.  
Elle permet la gestion des patients, l’analyse des données médicales et un tableau de bord administrateur.

---

## 🚀 Fonctionnalités

### 👨‍⚕️ Côté patient
- Enregistrement des patients
- Saisie des informations médicales :
  - Nom
  - Âge
  - Sexe
  - Adresse
  - Email
  - Téléphone
  - Maladie
- Validation des données

### 📊 Analyse médicale
- Répartition des sexes (graphique camembert)
- Statistiques des maladies (diagramme en barres)
- Génération automatique avec **Matplotlib**

### 🧑‍💼 Admin
- Authentification admin
- Tableau de bord complet
- Visualisation de tous les patients
- Actualisation des données

---

## 🛠️ Technologies utilisées

- 🐍 Python 3
- ⚡ Flet (UI web)
- 🐘 PostgreSQL
- 📊 Pandas
- 📈 Matplotlib
- 🧠 SQL (gestion base de données)

---

## Installation locale

### 1. Cloner le projet
```bash
git clone https://github.com/ton-utilisateur/supat-hospital-pro.git
cd supat-hospital-pro
2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
3. Installer les dépendances
pip install -r requirements.txt
📌 Requirements.txt
flet
psycopg2-binary
pandas
matplotlib
🗄️ Configuration base de données
Option 1 : Local PostgreSQL

Créer une base :

CREATE DATABASE supat;
CREATE USER supat_user WITH PASSWORD 'supat123';
GRANT ALL PRIVILEGES ON DATABASE supat TO supat_user;
Option 2 : Cloud (Render / Supabase / Railway)

Ajouter la variable d’environnement :

DATABASE_URL=postgresql://user:password@host:port/dbname
▶️ Lancer l’application
python main.py

Puis ouvrir :

http://localhost:8080
🌐 Déploiement (Fly.io / Render)
1. Build
flyctl launch
2. Deploy
flyctl deploy
📁 Structure du projet
supat-hospital-pro/
│
├── main.py
├── requirements.txt
├── assets/
│   ├── sexe.png
│   ├── maladie.png
│
└── README.md
⚠️ Notes importantes
L’application nécessite PostgreSQL actif
Les graphiques sont générés automatiquement dans /assets

L’admin par défaut est :

username: admin
password: 1234
📸 Aperçu

Ajoute ici des screenshots de ton app (home, dashboard, analyse)

👨‍💻 Auteur

Développé par [Ton Nom]

📜 Licence

Ce projet est open-source et libre d’utilisation pour fins éducatives.


---

# 💡 Bonus (important pour GitHub)

Ajoute aussi ces fichiers :

### 📄 `.gitignore`
```txt
__pycache__/
venv/
.env
*.pyc
assets/*.png
📄 Procfile (si Render/Heroku-like)
web: python main.py
