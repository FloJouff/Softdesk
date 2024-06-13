# SoftDesk support

![Python](https://img.shields.io/badge/python-3.12.x-green.svg)
![Django](https://img.shields.io/badge/django-5.0.4.x-green.svg)
![DjangoRESTFramework](https://img.shields.io/badge/djangoRESTframework-3.15.x-green.svg)

[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Flake8](https://img.shields.io/badge/flake8-checked-blueviolet)](https://flake8.pycqa.org/en/latest/)


## Description du projet:
  Le but de ce projet est de développer une API RESTful pour SoftDesk support à l'aide de Django REST, permettant le suivi du support technique de clients.

## Fonctionnalités de l'application:

### Gestion des utilisateurs

Un utilisateur peut s'authentifier à l'application grace à un username et un mot de passe. L'authentification retourne un Json Web Token qui permet de sécuriser la connexion et les données de l'utilisateurs.
Les choix de confidentialités de chaque utilisateurs sont pris en compte lors de leur inscription, conformément aux normes RGPD en implémentant deux attributs:
  partage des données et peut être contacté.
Une restriction d'inscription relative à l'âge de l'utilisateur est également mise en place conformément aux normes RGPD(Un utilisateur ne peut s'inscrire s'il a moins de 15 ans)

### Gestion des Projets

Tous les utilisateurs connectés peuvent consulter les projets existants.
Un utilisateur peut créer un projet. Il en devient l'auteur et le contributeur.
Lors de la création, il peut désigner d'autre utilisateurs inscrits comme contributeurs à ce projet.
Seuls les contributeurs peuvent avoir accès aux ressources qui référencent un projet (*issues* et *comments*) et accéder au détail de ce projet.

### Création des tâches et des problèmes (issues)

Un contributeur qui travaille sur un projet doit pouvoir créer des *Issues*.
Ces *Issues* permettent de planifier des fonctionnalités à mettre en oeuvre ou des bugs à régler dans un projet donné.
Les de la création de l'issu, le contributeur la nomme et donne une description. il peut l'assigner à un autre contributeur qu'il désigne comme *assignee*.
Cependant, seul un autre contributeur au projet peut être désigné comme tel.

### Création des commentaires (comments)

Afin de mieux cerner les problèmes et faciliter la communication, les contributeurs d'un projet peuvent commenter les *issues*

### Informations complémentaires

Seul l'auteur d'une ressource peut la modifier ou la supprimer.
Seuls les utilisateurs autorisés(*contributor*) peuvent consulter une ressource.

un système de pagination a été mis en place pour gérer le listage des ressources et éviter les charges excessives.

Les points de terminaisons de l'API peuvent être testées à l'aide d'outils comme Postman.

## Installation et lancement

#### Installer Python

L’installation de Python est très simple ! Rendez-vous sur [python.org](https://www.python.org/downloads/), choisissez votre système d’exploitation (Mac/Windows, etc.) et cliquez sur le bouton de téléchargement pour installer Python sur votre ordinateur.

Si vous utilisez Windows, pensez à bien cocher la case "Add to path" pour ajouter Python aux variables d'environnement.

#### Faire une copie du repository.

A partir du lien GitHub: https://github.com/FloJouff/Softdesk, créer un clone du projet en local sur votre ordinateur

#### Gestion des dépendances

Afin de limiter les failles et vulnérabilités des dépendances, l'utilisation de Pipenv permettra de les garder à jour:

    $ pip install pipenv
    $ pipenv install

    $ pipenv shell

    $ pipenv install -r requirements.txt

#### Base de données

Placez vous à la racine du projet puis effectuer les migrations:

    $ python manage.py makemigrations

puis, en l'absence de message d'erreur:

    $ python manage.py migrate

#### Lancement

- Exécuter le programme en tapant "python manage.py" dans la console ou à l'aide d'un éditeur de code.
   - Dans le terminal, tapez: 
      
        $ python manage.py runserver 

      pour lancer le serveur local.
   - Dans votre navigateur, rendez vous à l' adresse:" http://127.0.0.1:8000/api/users/" pour acceder au site.
---

## Administration du site:
   - Créer un profil "superuser" dans le terminal:
      $ python manage.py createsuperuser
   
   - Suivez les instructions de l'invite pour créer votre superuser. 
   Vous n'avez pas besoin de remplir une adresse électronique, mais n'oubliez pas votre mot de passe.

   - Ensuite, exécutez le serveur de développement, et dans votre navigateur, allez sur http://127.0.0.1:8000/admin/ 
   - À partir de là, vous pourrez gérer les différents modèles enregistrés sur le site d'administration.

---
## Liste des points de terminaison de l'API:
   
|# | *Methode HTTP* | *URL (base: http://127.0.0.1:800)*                                | *Endpoint de l'API*                     |
|--|----------------|-------------------------------------------------------------------|-----------------------------------------|
|1 |POST            |/api/users/                                                        |Inscription d'un utilisateur             |
|2 |POST            |/api/token/                                                        |Connexion d'un utilisateur               |
|3 |POST            |/api/token/refresh/                                                |Refresh token d'un utilisateur           |
|4 |GET             |/api/users/                                                        |Liste des utilisateurs                   |
|5 |GET             |/api/users/{user_id}/                                              |Détail de l'utilisateur connecté         |
|6 |PATCH           |/api/users/{user_id}/                                              |Modifications de l'utilisateur connecté  |
|7 |DELETE          |/api/users/{user_id}/                                              |Suppression de l'utilisateur connecté    |
|8 |POST            |/api/projects/                                                     |Création d'un projet                     |
|9 |GET             |/api/projects/                                                     |Liste des projects                       |
|10|GET             |/api/projects/{project_id}/                                        |Détails d'un projet                      |
|11|PATCH           |/api/projects/{project_id}/                                        |Modification d'un projet                 |
|12|DELETE          |/api/projects/{project_id}/                                        |Suppression d'un projet                  |
|13|POST            |/api/projects/{project_id}/issues/                                 |Création d'une issue                     |
|14|GET             |/api/projects/{project_id}/issues/                                 |Liste des issues d'un projet             |
|15|GET             |/api/projects/{project_id}/issues/{issue_id}/                      |Détails d'une issue                      |
|16|PATCH           |/api/projects/{project_id}/issues/{issue_id}/                      |Modification d'une issue (par son auteur)|
|17|DELETE          |/api/projects/{project_id}/issues/{issue_id}/                      |Suppression d'un projet (par son auteur) |
|18|POST            |/api/projects/{project_id}/issues/{issue_id}/comments/             |Création d'un comment                    |
|19|POST            |/api/projects/{project_id}/issues/{issue_id}/comments/             |Liste des comments d'une issue           |
|20|POST            |/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/|Détails d'un comment                     |
|21|POST            |/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/|Modification d'un comment(par son auteur)|
|22|POST            |/api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/|Suppression d'un comment(par son auteur) |
|23|GET             |/api/projects/{project_id}/contributors/                           |Liste des contributeurs d'un projet      |

