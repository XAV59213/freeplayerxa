# Free Player XA (Home Assistant custom component)

Contrôlez plusieurs Freebox Player comme des entités `media_player`. Chaque TV est ajoutée via l'UI avec **Nom**, **IP**, **Code télécommande**.

> ⚠️ Freebox mini 4K non compatible (pas de code télécommande HTTP).

## Installation via HACS
1. HACS → Intégrations → menu ⋮ → **Custom repositories** → ajoutez ce dépôt en type *Integration*.
2. Installez **Free Player XA** puis redémarrez Home Assistant.

## Installation manuelle
Copiez `custom_components/freeplayerxa` dans `config/custom_components/` puis redémarrez.

## Configuration (UI)
1. Paramètres → Appareils & services → **Ajouter une intégration** → *Free Player XA*.
2. Renseignez : **Nom de la TV**, **IP**, **Code télécommande** (Freebox OS → Télécommande).
3. Options : mappage des chaînes (une par ligne), ex. :
   ```
   1: TF1
   2: France 2
   3: France 3
   BFM=15
   ```

## Notes techniques
- API HTTP : `http://<ip>/pub/remote_control?code=<CODE>&key=<KEY>` (ajoutez `&long=true` si nécessaire).
- `unique_id` = `host-code` pour autoriser plusieurs TV.
- L'état ON/OFF est approximatif (API stateless).

## Licence
MIT
