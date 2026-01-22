---
marp: true
theme: default
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
---

<!-- _class: lead -->

# Mauvaise IA Dans Une Boîte (**BAIIAB**)

*Faire que l'IA « Touche l'Herbe »*
Tommy Falgout - Architecte Solutions Partenaires @ Microsoft
Yui Mikuriya - Architecte Solutions Partenaires @ Microsoft

<!--
Ma journée a commencé à leur 2h du matin
Avec Amanda + Tam
Partenariat avec Ignite
MAUVAISE != maléfique. Essayer de bouleverser les attentes
-->

---

<!-- _class: lead -->

# Mauvaise IA Dans Une Boîte (**BAIIAB**)

*Faire que l'IA « Touche l'Herbe »*
Requin de Pelouse

![bg right:50% w:600](img/lawn-shark.png)

<!--
Je ne veux pas que vous vous sentiez appâtés
Mon Requin de Pelouse
-->

---

# Moi

- Grand passionné de bricolage
  - [DFW Trebuchet](https://www.dfwtrebuchet.com/)
  - [LEGO Robo-Clippy](https://github.com/lastcoolnameleft/robo-clippy)
  - [Bad AI In A Box](https://github.com/lastcoolnameleft/baiiab)
  - [LED Lanyard](https://ledlanyard.com)
  - [NTX Makers](https://www.ntxmakers.com/)
- Architecte Solutions Partenaires @ Microsoft (ex-Yahoo!, ex-Nortel)
- [Expert en trébuchet pour Dude Perfect](https://www.imdb.com/name/nm9305352/) (S2.E6)

![bg right:50% w:600](img/halloween.png)

<!--
_footer: Source: moi
-->

---

# POURQUOI ?!?!

**Rendre l'IA Intrigante et Amusante, Pas Effrayante**

- Inspiré par le projet "[Fortune Witch](https://www.olisny.com/fortune-witch/)" d'amis
- Basé sur un [projet Adafruit](https://learn.adafruit.com/pi-thermal-printer)
- Je voulais créer quelque chose de **tangible** et **amusant**
- L'IA peut sembler intimidante et complexe
- L'interaction physique la rend plus accessible

> *« Et si interagir avec l'IA pouvait être aussi simple que de tourner un bouton ? »*

![bg right:45% w:600](img/yt.jpg)

<!--
MAUVAISE != maléfique. Essayer de bouleverser les attentes
-->

---

# Évolution du Projet

Ça a commencé comme un exercice d'apprentissage...

1. **Objectif Initial** : Apprendre ce nouveau truc ChatGPT
2. **Première Itération** : [Bad Advice As A Service (BaaaS)](https://advice.lastcoolnameleft.com/)
3. **Interface Physique** : Ajout Raspberry Pi + LCD + Bouton
4. **Mode Hors Ligne** : Si le WiFi / Partage de connexion échoue
5. **Observabilité** : Ajout d'OpenTelemetry
6. **Intégration Cloud** : Connexion à la plateforme d'observabilité Elastic

![bg right:40% w:500](img/baaas.png)

<!--
Inspiré par un "Stand de mauvais conseils" auquel j'ai assisté
-->

---

# Le Grand Moment

### Microsoft Build 2025 - Keynote du Jour 3

**Présenté avec :**
- **Mark Russinovich** - CTO Azure
- **Scott Hanselman** - Légende du Developer Advocacy

[Démonstration en direct sur scène](https://youtu.be/KIFDVOXMNDc?t=3233) :
- Plus de 1000 personnes dans l'audience
- 10k vues sur YouTube

![bg right:35% w:400](img/build-keynote.png)

<!--
Ça peut ne pas sembler important, mais j'ai ça comme photo de profil Teams et je reçois encore des commentaires

-->

---


# Flux d'Expérience Utilisateur

```
                                                ┌─────────────────────┐
                                                │   ÉCRAN D'ACCUEIL   │ Écran LCD 4x20
                                                │   IA Dans Une Boîte │
                                                └─────────────────────┘
                                                        ↓ (tourner pour parcourir)
                                                ┌─────────────────────┐
                                                │   > Blague          │
                                                │     Conseil         │
                                                │     Recette         │
                                                │     Insulte         │
                                                └─────────────────────┘
                                                        ↓ (appuyer pour sélectionner)
                                                ┌─────────────────────┐
                                                │   > Blague de Papa  │
                                                │     Drôle           │
                                                │     Absurde         │
                                                └─────────────────────┘
                                                        ↓ (appuyer pour générer)
                                                ┌─────────────────────┐
                                                │   GÉNÉRATION...     │
                                                │   Azure OpenAI GPT-4│
                                                └─────────────────────┘
                                                        ↓ (imprimer)
                                                ┌─────────────────────┐
                                                │       [Logo]        │ 
                                                │      [BAIIAB]       │
                                                │                     │ Papier de caisse
                                                │   [Réponse IA]      │
                                                │   [Avertissement]   │
                                                │   [bit.ly/baiiab]   │
                                                └─────────────────────┘
```

<!--
Montrer la boîte
-->
---

# Architecture Technique
![w:800](img/architecture.png)

---

<!-- _class: lead -->

# TEMPS DE DÉMO !

<!--
Démo simulateur + montrer le code
-->
---

# Liste des Composants (BOM)

## Composants Matériels

| Composant | Fonction |
|-----------|---------|
| **Raspberry Pi Zero 2 W** | 4 cœurs, basé sur Debian |
| **Écran LCD 20x4** | Afficher les menus de navigation |
| **Encodeur Rotatif** | Navigation (tourner + appuyer) |
| **Imprimante Thermique** | Sortie sur papier de caisse |
| **Boîtier** | Boîtier personnalisé imprimé en 3D |

**Coût Total** : ~150-200 €

---

# La Boîte

![bg right:50% w:600](img/the-internet.jpg)

- Conçue avec OpenSCAD + Tinkercad
- Inspirée de "L'Internet"
- Imprimée en 3D (PLA)
- Trous pour imprimante thermique, boutons, écran

<!--
Design inspiré de L'Internet de IT Crowd
-->

---

# OpenSCAD

- Modeleur 3D pour programmeurs
- Permet une conception paramétrique facile
- Personnalisation des boutons

![bg right:60% w:700](img/openscad.png)

---

# L'Interface

Inspirée de l'interface de mon imprimante Prusa i3 MK3

- Utilise un écran LCD de 20x4 caractères
- Interface réécrite en Python


![bg right:50% w:600](img/prusa.webp)

---

# Encodeur Rotatif

1. **Tourner dans le Sens Horaire** ↻
   - Naviguer vers le bas dans les options du menu
   
2. **Tourner dans le Sens Anti-horaire** ↺
   - Naviguer vers le haut dans les options du menu
   
3. **Appuyer sur le Bouton** 
   - Sélectionner l'option actuelle
   - Générer la réponse IA

**Callbacks gérés en Python**

**C'est tout !** Pas de clavier, pas de souris, pas d'écran tactile.

![bg right:50% w:600](img/rotary-encoder.png)

---

# Imprimante Thermique

![bg right:50% w:600](img/thermal-printer.jpg)

- À l'origine de chez [Adafruit](https://www.adafruit.com/product/597)
        - [Bibliothèque Python](https://github.com/adafruit/Adafruit-Thermal-Printer-Library)
        - Discontinuée !
- Jeu de Caractères : ASCII
- Protocole : Série TTL, 19200 baud
---

# Capacité de la Batterie

- mAh = durée de fonctionnement d'un appareil
- Pensez au mAh comme la taille d'un réservoir de carburant :
  - Une batterie de 2000 mAh peut alimenter un appareil de 100 mA pendant 20 heures
  - Plus de mAh = plus longue autonomie
![bg right:40% w:500](img/battery-test.png)

---

# Comment mesurer ça ?!

![bg right:40% w:500](img/usb-multimeter.png)
- Les [multimètres USB](https://amzn.to/45PBLf5) sont vos amis !
- Le projet nécessite 2 connexions USB
  - RPi + Imprimante Thermique


---


# Catégories de Contenu

Stockées dans un fichier de configuration : **Sujet -> Sous-sujet -> Prompt**

- Conseil - Mauvais, Idiot, Cryptique, Bon
- Faux Faits - Darth Vader, Satya Nadella
- Cocktail - Délicieux, Dégoûtant
- Conspiration - Drôle, Folle, Sombre
- Insulte - Monty Python, Shakespeare, Français, Allemand, Espagnol

*Tout alimenté par Azure OpenAI (GPT-4)*




---

# Décisions d'Architecture

## Pourquoi Ces Choix ?

| Décision | Raison |
|----------|--------|
| **Raspberry Pi** | Abordable, puissant, support GPIO, __faible consommation__ (0.17A)|
| **Python** | Prototypage rapide, bibliothèques riches |
| **LCD 20x4** | Taille parfaite, bon marché, fiable |
| **Impression 3D** | Reproductible, design personnalisé |
| **Encodeur Rotatif** | Intuitif, retour tactile |
| **OpenTelemetry** | Neutre vis-à-vis des fournisseurs, pérenne |
| **Azure OpenAI** | Accès GPT-4, avantage entreprise |

---

# Les Chiffres

## Statistiques du Projet

- **Lignes de Code** : ~2 500
- **Sujets** : 5 principaux
- **Sous-sujets** : 2-5+ par sujet
- **Coût par requête** : ~0,02 € (GPT-4)
- **Temps de réponse** : 1-3 secondes en moyenne
- **Démos en conférence** : 100+ interactions

---

# Ajout de l'Observabilité

## Intégration OpenTelemetry

**Pourquoi ?** Pour comprendre :
- Comment les utilisateurs interagissent avec l'appareil
- Les performances de l'API
- Les requêtes les plus populaires
- Combien ça coûte à Microsoft...

**Connecté à la Plateforme d'Observabilité Elastic**
- Traces en temps réel
- Métriques et tableaux de bord

![bg right:40% w:600](img/OpenTelemetry.png)

---

# Intégration Elastic Observability

## Pourquoi Elastic ?

**Plateforme Unifiée :**
- Logs, métriques, traces au même endroit
- APM pour la performance applicative
- Tableaux de bord et alertes personnalisés

**Support OTLP :**
- Ingestion native OpenTelemetry
- Migration facile

![bg right:50% w:400](img/elastic.png)

---

# Métriques Suivies

- **Appels API** : Nombre, durée, modèle, statut
- **Interactions Utilisateur** : Sélections de catégories, navigation
- **Temps de Réponse** : Durée des appels API
- **Taux d'Erreur** : Appels échoués, timeouts
- **Contenu Populaire** : Catégories les plus demandées

*Tout visualisé dans les tableaux de bord Elastic*

![bg right:50% w:600](img/kibana.png)

---

<!-- _class: lead -->

# TEMPS DE DÉMO ! (Prise 2)

<!--
Démo simulateur + montrer le code
-->

---

![bg 95%](img/elastic-in-azure-1.png)

---

![bg 95%](img/elastic-in-azure-2.png)


---

# Au-delà de la Nouveauté

**Interfaces IA physiques :**
- Combler le fossé numérique-physique
- Rendre l'IA accessible aux non-techniciens
- Créer des expériences mémorables

**Observabilité :**
- Comprendre le comportement des utilisateurs
- Déboguer les problèmes de production

**Open Source :**
- Partager les difficultés d'apprentissage
- « Avec suffisamment de regards, tous les bugs sont superficiels... »


---

# Défis Surmontés

**Matériel :**
- Le faire tenir → câbles personnalisés + boîte
- Périphériques → Beaucoup d'échecs en prod
- Anti-rebond de l'encodeur → ajout de sleep(?)

**Logiciel :**
- Gestion des timeouts API → logique de retry + mode hors ligne
- RPi + gRPC = GALÈRE → Migration vers HTTP (pas de compilation)
- Logique de navigation dans les menus → pattern machine d'état

---

## Mode Hors Ligne

### Résilience Intégrée

**Réponses de secours** quand le réseau échoue :
- Réponses pré-générées
- Stockées en JSON

**Avantages :**
- Fonctionne en conférence (WiFi instable)
- Fiabilité des démos

![bg right:50% w:600](img/offline-dino.png)

---

# Et Après ?

- Feedback Utilisateur (Pouce haut/bas)
- ~~Audio~~ - Pas adapté pour les conférences
- ~~LLM Local~~ - CPU 1 cœur
- Mobile ? IoT ? Caméra ?
- Afficher le coût ?
- Corriger les problèmes avec certains Unicode (ex : "¾ oz Bourbon")

---

# FAQ

**Q : Pourquoi Raspberry Pi ?**
R : Abordable, puissant, excellent support GPIO, grande communauté

**Q : Puis-je utiliser d'autres modèles IA ?**
R : Oui ! Fonctionne avec toute API compatible OpenAI

**Q : Ça fonctionne hors ligne ?**
R : Oui ! Mode de secours avec contenu pré-généré

**Q : Pourquoi OpenTelemetry ?**
R : Neutre vis-à-vis des fournisseurs, pérenne, écosystème riche

**Q : Puis-je ajouter des catégories personnalisées ?**
R : Absolument ! Éditez conf/menu.json

---

# Points Clés à Retenir

## Ce Qui Rend Ce Projet Spécial

1. **IA Tangible** - le physique surpasse le numérique pour l'engagement
1. **Interface Simple** - 3 interactions = accessibilité maximale
1. **Observable** - comprendre l'utilisation
1. **Résilient** - fonctionne en ligne et hors ligne
1. **Open Source** - apprendre, partager, améliorer
1. **Abordable** - ~150-200 € de composants

---

# Ressources

## En Savoir Plus

**Code & Documentation :**
- GitHub : [github.com/lastcoolnameleft/baiiab](https://github.com/lastcoolnameleft/baiiab)
- Issues & PRs bienvenues !

**Technologies :**
- OpenTelemetry : [opentelemetry.io](https://opentelemetry.io)
- Elastic Observability : [elastic.co/observability](https://elastic.co/observability)
- Azure OpenAI : [azure.microsoft.com/openai](https://azure.microsoft.com/openai)
- Raspberry Pi : [raspberrypi.org](https://raspberrypi.org)


---

<!-- _class: lead -->

# **BAIIAB - Mauvaise IA Dans Une Boîte**

# Diapositives disponibles sur : [https://lastcoolnameleft.github.io/baiiab/](https://lastcoolnameleft.github.io/baiiab/)

![bg right:47% w:500](img/qrcode.png)

<!--
_footer:  Diapositives écrites en [MARP](https://marp.app/)

-->
---

*Construit avec ❤️ et OpenTelemetry*

GitHub : lastcoolnameleft/baiiab
Site web : lastcoolnameleft.com
Email : tommy lastcoolnameleft com

