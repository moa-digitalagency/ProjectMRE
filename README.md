# Site Vitrine Project

Structure du projet en Python Flask avec support pour base de données PostgreSQL.

## Structure des dossiers

- `algorithms/`: Algorithmes métier.
- `config/`: Configuration de l'application.
- `docs/`: Documentation.
- `lang/`: Fichiers de traduction.
- `models/`: Modèles de base de données (SQLAlchemy).
- `routes/`: Routes et contrôleurs Flask.
- `scripts/`: Scripts utilitaires.
- `security/`: Gestion de la sécurité.
- `services/`: Logique métier.
- `statics/`: Fichiers statiques (CSS, JS, images, uploads).
- `templates/`: Templates HTML (Jinja2).
- `utils/`: Fonctions utilitaires.

## Installation

1. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurer la base de données :
   - Le fichier `.env` contient la configuration. Modifiez `DATABASE_URL` pour utiliser PostgreSQL.
   - Exemple pour PostgreSQL : `DATABASE_URL=postgresql://user:password@localhost/dbname`
   - Par défaut, SQLite est utilisé (`app.db`) pour le développement si `DATABASE_URL` n'est pas défini pour Postgres.

4. Initialiser la base de données :
   ```bash
   python init_db.py
   ```
   Cela créera les tables nécessaires et un utilisateur administrateur par défaut.

5. Lancer l'application :
   ```bash
   python app.py
   ```
   Accéder à `http://127.0.0.1:5000`.

## Technologies

- Backend: Python Flask
- Base de données: PostgreSQL (via SQLAlchemy)
- Frontend: HTML, CSS (Tailwind via CDN), JS
