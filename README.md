# Freeplayer XA - Custom Component for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/hacs/integration)

Basé sur une bibliothèque pure-python, ce composant personnalisé permet de contrôler à distance plusieurs appareils Freebox Player.

Ce composant est testé sur Freebox Delta, mais devrait fonctionner sur Freebox Revolution et Crystal (feedback apprécié). Il ne fonctionne pas sur Freebox Mini 4K, car elle n'a pas de code de télécommande.

## Installation

### Installation via HACS
1. Recherchez `Freeplayer XA` sous `Integrations` dans l'onglet Store de HACS.
2. **Redémarrez Home Assistant après l'installation pour que le composant fonctionne.**
3. Configurez l'intégration (voir section Configuration).

## Fonctionnalités
* Supporte On / Off
* Supporte le changement de chaînes
* Supporte les changements de volume
* Supporte les contrôles de navigation
* Support pour plusieurs players (TVs) configurables indépendamment
* Plus à venir

## Encore en développement
Ce composant utilise l'ancienne API de télécommande, mais Free développe une nouvelle API non liée à la télécommande (contrôler le player pour ouvrir des URLs, etc.).

## Configuration
Une fois installé, le composant Freeplayer XA doit être configuré pour fonctionner.

Éditez le fichier `configuration.yaml` et ajoutez ce qui suit :

```yaml
# Exemple d'entrée dans configuration.yaml
freeplayerxa:
  players:
    - name: TV Salon
      host: 192.168.0.10
      remote_code: 12345678
    - name: TV Chambre
      host: 192.168.0.11
      remote_code: 87654321
