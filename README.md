DirtySales Analytics

Mini application full-stack data analytics construite pour démontrer :
- la manipulation de données “sales” (valeurs manquantes / invalides),
- une API Python moderne avec FastAPI,
- un frontend React + TypeScript construit manuellement (Webpack),
- l’affichage de données via tables analytiques et graphiques.

Le projet met l’accent sur la qualité des données, la séparation des responsabilités et les bonnes pratiques d’architecture.

Stack technique
- Backend
    - Python
    - FastAPI
    - Polars / Pandas (cleaning & transformation)
    - DuckDB (analytics SQL in-memory)
    - Pydantic (DTO / contrats API)

- Frontend
    - React 19
    - TypeScript
    - Webpack 5 (setup manuel)
    - Ant Design (tables & UI data-heavy)
    - Ant Design Charts (graphiques)
    - Tailwind CSS (layout & design utilitaire)
    - React Router

Fonctionnalités
- Backend
    - Chargement d’un CSV volontairement sale
    - Normalisation et validation des données
    - Génération de flags de qualité (is_invalid, issues)
    - Endpoints :
        /rows : lignes avec filtres
        /kpis : métriques globales
        /timeseries : revenus dans le temps
        /data-quality : qualité par colonne
    - Documentation automatique via Swagger (/docs)

- Frontend
    - Page Table :
        - table Ant Design
        - tri, pagination
        - mise en évidence des données invalides
    - Page Charts :
        - KPIs
        - graphique d’évolution du revenu
        - Navigation via routes dédiées

Lancer le projet
- Backend
    cd backend
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload

    API disponible sur : http://127.0.0.1:8000
    Swagger : http://127.0.0.1:8000/docs

- Frontend
    cd frontend
    npm install
    npm run dev

    Frontend disponible sur : http://localhost:5173