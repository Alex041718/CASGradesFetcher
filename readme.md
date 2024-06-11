# Bonjour !

## C'est quoi ce repot ?

Les université et IUTs de france utilises un logiciel appelé Scodoc pour enregistrer les notes des étudiants.

@SebL68 à conçu avec d'autres contributeurs une interface / passerelle (qui peut être déployer par les université) pour récupérer les notes de Scodoc et les afficher sur un site web, à destination des étudiants.


`https://notes9.iutlan.univ-rennes1.fr` est l'adresse de cette interface pour l'IUT de Lannion.

Ce repot contient des outils pour récupéré les notes de Scodoc à partir de cette interface.

Le script `main.py` gère notamment l'autentification du serveur CAS de l'université permettant par la suite de récupérer les notes de l'utilisateur.

Mon objectif est de réccupérer et stocker mes notes périoquement à fin de visualiser une sorte d'historique.