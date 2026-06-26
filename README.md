# Météo-France Observation

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Syxxxx/meteofrance-observation)
![GitHub last commit](https://img.shields.io/github/last-commit/Syxxxx/meteofrance-observation)

Cette intégration pour Home Assistant permet de récupérer les données d'observation en temps quasi-réel (toutes les 6 minutes) des stations de Météo-France via l'API publique officielle.

## Fonctionnalités

* Connexion à l'API Publique d'Observation de Météo-France.
* Configuration simple via l'interface utilisateur de Home Assistant.
* Création d'un appareil (Device) par station météo pour regrouper toutes les entités.
* Création de capteurs (sensors) pour chaque donnée météorologique disponible.
* Mise à jour automatique des données toutes les 6 minutes.

## Prérequis

* Home Assistant (version 2023.9 ou plus récente).
* [HACS](https://hacs.xyz/) installé et fonctionnel.
* Une clé d'API valide obtenue depuis le [portail API de Météo-France](https://portail-api.meteofrance.fr/).
* Avoir souscrit à l'API [Données d’observation Version: v2 (gratuit)](https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesObservation).

## ⬇️ Installation via HACS

Pour l'instant, cette intégration n'est pas dans le dépôt par défaut de HACS. Vous devez l'ajouter comme **dépôt personnalisé**.

1.  Allez dans votre interface Home Assistant.
2.  Naviguez vers **HACS** > **Intégrations**.
3.  Cliquez sur les trois points en haut à droite et sélectionnez **Dépôts personnalisés**.
4.  Dans le champ "Dépôt", collez l'URL de ce projet :
    ```
    [https://github.com/Syxxxx/meteofrance-observation](https://github.com/Syxxxx/meteofrance-observation)
    ```
5.  Dans le champ "Catégorie", sélectionnez **Intégration**.
6.  Cliquez sur **Ajouter**.
7.  L'intégration apparaît maintenant dans la liste. Cliquez sur **Installer** et suivez les instructions.

## ⚙️ Configuration

Une fois l'installation terminée, vous devez configurer l'intégration :

1.  Redémarrez Home Assistant pour vous assurer que l'intégration est bien chargée.
2.  Allez dans **Paramètres** > **Appareils et services**.
3.  Cliquez sur le bouton **+ Ajouter une intégration** en bas à droite.
4.  Cherchez "**Météo-France Observation**" et sélectionnez-la.
5.  Une boîte de dialogue s'ouvrira :
    * **ID de la station** : Entrez l'identifiant de la station Météo-France que vous souhaitez suivre (ex: `59343001` pour Lille-Lesquin).
    * **Clé d'API** : Entrez la clé d'API que vous avez obtenue.
6.  Cliquez sur **Valider**. L'appareil et ses entités seront automatiquement ajoutés.

## 📊 Entités créées

L'intégration créera les capteurs suivants :

* Température
* Température du sol (10cm)
* Humidité
* Pression
* Vitesse du vent
* Direction du vent
* Vitesse des rafales
* Précipitations (6 min)
* Rayonnement Solaire
* Durée d'ensoleillement (1h)
* Visibilité

---

*Cette intégration n'est pas officiellement affiliée ou supportée par Météo-France.*
