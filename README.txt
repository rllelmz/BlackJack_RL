Fichier SimpleBlackJack.py:
  - simple modélisation du Jeu de Nim avec 2 joueurs choisissant aléatoirement un chiffre entre 1 et 3 à envoyer au juge & ce dernier additionne les valeurs données par chaque joueur ainsi qu'annoncer le gagnant, c'est-à-dire le premier à atteindre la somme de 21. Les 2 joueurs ont la même chance d'être le joueur_2.
  - exécution: pade start-runtime --port 2000 SimpleBlackJack.py

Fichier BlackJackIntelligence.py:
  - même principe que le premier sauf que cette fois-ci, on donne une bonne stratégie (une intelligence) aux joueurs pour terminer le jeu le plus rapidement possible 
  - Fonctionnement: 
      - si la banque vaut 18 alors le joueur qui joue choisit 3 et gagne;
      - si la banque vaut 19 alors le joueur qui joue choisit 2 et gagne;
      - si la banque vaut 20 alors le joueur qui joue choisit 1 et gagne;
      - sinon chaque joueur joue 1.
  - exécution: pade start-runtime --port 2000 BlackJackIntelligence.py

Fichier Complex2j.py:
  - modélisation du Jeu de Nim entre 2 joueurs avec la suppression du juge: 
      - les 2 joueurs ont toujours la même chance d'être le joueur_2;
      - le joueur_2 tire aléatoirement un chiffre entre 1 et 3 et demande une proposition d'une valeur au joueur_1 qui lui propose un chiffre aléatoire entre 1 et 3;
      - chaque joueur a sa propre banque et additionne la banque reçue de l'autre joueur avec son chiffre aléatoire, uniquement si le joueur précédent n'est pas arrivé ou dépassé 21;
      - les joueurs s'informe de l'état actuel du jeu au lieu du juge précédemment:
           - "ARRET": le joueur précédent ou joueur actuel a dépassé 21;
           - "LOSE": le joueur précédent ou actuel n'a pas atteint le score de 21;
           - "WIN": le joueur précédent ou actuel a gagné.
  - exécution: pade start-runtime --port 2000 Complex2j.py

Fichier Complex3j.py:
  - même principe que le jeu de Nim entre 2 joueurs mais dans le cas de 3 joueurs, on utilise un anneau logique:
      - les 3 joueurs ont la même chance d'être le joueur_2;
      - chaque joueur est connecté à son prochain joueur et ne peut envoyer sa banque qu'à ce dernier: j1 → j2, j2 → j3, j3 → j1;
      - fin d'une partie: tous les joueurs sont au courant de qui a gagné, perdu ou bien si le score est supérieur à 21.
  - exécution: pade start-runtime --port 2000 Complex3j.py

Fichier ComplexNj.py:
  - même principe que le jeu de Nim entre 3 joueurs mais avec N joueurs.
  - exécution: pade start-runtime --port 2000 ComplexNj.py 

Remarques:
  - nous avons défini une fonction "def arreter" pour arrêter le comportement d'un agent lorsqu'il envoie ou reçoit un message de type "INFORM" mais ne fonctionne pas;
  - nous avons également essayé "self.agent.behaviours.remove(self)" mais ne fonctionne pas;
  - les fichiers Complex2j.py, Complex3j.py et ComplexNj.py: nous avons décidé de remplacer la partie intelligence par le choix aléatoire d'un chiffre entre 1 et 3 pour voir l'ensemble des comportements des agents (sinon la condition où la banque est supérieure à 21 ne sera jamais prise en compte).
