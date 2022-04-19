from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.behaviours.protocols import Behaviour
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
import random


class Joueur(Agent):
    def __init__(self, aid, NextJoueurAID):
        super(Joueur, self).__init__(aid=aid)
        display_message(self.aid.name, 'Je suis un joueur !')
        self.JoueurNom = self.aid.name
        self.J2 = ""
        self.NextJoueur = NextJoueurAID
        self.call_later(8, self.initialize_send)

    def initialize_send(self):
        joueur_behaviour = JoueurBehaviour(self)
        self.behaviours.append(joueur_behaviour)
        joueur_behaviour.on_start()

    def arreter(self):
        self.pause_agent
        self.behaviours = []


class JoueurBehaviour(Behaviour):

    def __init__(self, agent):
        super().__init__(agent)
        self.aleatoire = 0
        self.banque = 0

    def envoyerCFP(self, message, dest):
        reponse = ACLMessage(ACLMessage.CFP)
        reponse.set_content(message)
        reponse.add_receiver(dest)
        self.agent.send(reponse)

    def envoyerPROPOSE(self, message, dest):
        reponse = ACLMessage(ACLMessage.PROPOSE)
        reponse.set_content(message)
        reponse.add_receiver(dest)
        self.agent.send(reponse)

    def on_start(self):
        if self.agent.JoueurNom == self.agent.J2:  # Le joueur 2 commence à jouer directement
            display_message(self.agent.aid.name, 'Je commence la partie')
            self.aleatoire = random.randrange(1, 4)
            self.banque += self.aleatoire
            display_message(self.agent.aid.name,
                            'Je joue ' + str(self.aleatoire) + '. Score actuel: ' + str(self.banque))
            # display_message(self.agent.aid.name, ' Score envoyé à {}'.format(self.agent.NextJoueur))
            self.envoyerCFP(str(self.banque), self.agent.NextJoueur)

    def execute(self, message):
        # La fonction execute alterne entre deux types de messages : les CFP et PROPOSE
        if message.performative == ACLMessage.CFP:
            resultat = message.content
            if resultat == "WIN":
                display_message(self.agent.aid.name, 'J\'ai gagné :)')
                # self.agent.arreter()
            elif "ARRET" in resultat:  # La fonction execute alterne entre deux types de messages : les CFP et PROPOSE
                g = resultat.replace("ARRET ", "")  # On supprime le mot ARRET pour ne garder que le nom du sender initial
                if str(self.agent.aid.name) != g:  # Si je ne suis pas le sender initial, j'envoie l'information au next joueur
                    self.envoyerPROPOSE(resultat, self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                # self.agent.arreter()
            elif "LOSE" in resultat:  # Même principe que l'arrêt.
                g = resultat.replace("LOSE ", "")
                if str(self.agent.aid.name) != g:
                    self.envoyerPROPOSE(resultat, self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                    # Dans le cas ou self.agent.aid.name == g : l'information a fait le tour des joueurs et est revenue au sender initial, donc fin de l'execution
                    # self.agent.arreter()
            else:  # Si le message n'est ni un WIN, ni un LOSE ni un ARRET, alors c'est forcément le score actuel.
                display_message(self.agent.aid.name,
                                'Score actuel: ' + resultat + ' envoyé par : {}'.format(message.sender.name))
                self.banque = int(resultat)
                """ On commence par traiter le résultat envoyé par le joueur précedent
                    Donc si le score == 21, c'est le joueur précédent qui a gagné, et l'actuel a perdu et divulgue l'information. """
                if self.banque > 21:  # Arrêt du jeu
                    self.envoyerPROPOSE("ARRET {}".format(self.agent.aid.name), self.agent.NextJoueur)
                    display_message(self.agent.aid.name, ' Le score est supérieur à 21 : Fin du jeu.')
                    # self.agent.arreter()
                elif self.banque == 21:
                    self.envoyerPROPOSE("WIN", message.sender.name)
                    display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                    # self.agent.arreter()
                else:  # Cas où le score est inférieur à 21 : on ajoute le numero joué par le joueur actuel et on traite le nouveau score
                    self.aleatoire = random.randrange(1, 4)
                    self.banque += self.aleatoire
                    display_message(self.agent.aid.name, 'Je joue ' + str(self.aleatoire))
                    if self.banque == 21:
                        display_message(self.agent.aid.name, 'Score atteint de ' + str(self.banque))
                        self.envoyerPROPOSE("LOSE {}".format(self.agent.aid.name), self.agent.NextJoueur)
                        display_message(self.agent.aid.name, 'J\'ai gagné :)')
                        # self.agent.arreter()
                    elif self.banque > 21:  # Arrêt du jeu
                        self.envoyerPROPOSE("ARRET {}".format(self.agent.aid.name), self.agent.NextJoueur)
                        display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                        # self.agent.arreter()
                    else:
                        self.envoyerPROPOSE(str(self.banque), self.agent.NextJoueur)
        if message.performative == ACLMessage.PROPOSE:  # Même principe que le CFP
            """Remarque : on aurait pu éviter la répétition du code en le regroupant dans un INFORM mais ceux-ci s'envoient mais n'arrivent jamais au destinataire.
               Et il est impossible d'utiliser un CFP ou un PROPOSE seul car le Call For Proposal nécessite un Proposal comme réponse et inversement. """
            resultat = message.content
            if resultat == "WIN":
                display_message(self.agent.aid.name, 'J\'ai gagné :)')
                # self.agent.arreter()
            elif "ARRET" in resultat:
                g = resultat.replace("ARRET ", "")
                if str(self.agent.aid.name) != g:
                    self.envoyerCFP(resultat, self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
            elif "LOSE" in resultat:
                g = resultat.replace("LOSE ", "")
                if str(self.agent.aid.name) != g:
                    self.envoyerCFP(resultat, self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                    # self.agent.arreter()
            else:
                display_message(self.agent.aid.name,
                                'Score actuel: ' + message.content + ' envoyé par : {}'.format(message.sender.name))
                self.banque = int(message.content)
                if self.banque > 21:  # Arrêt du jeu
                    self.envoyerCFP("ARRET {}".format(self.agent.aid.name), self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                    # self.agent.arreter()
                elif self.banque == 21:
                    self.envoyerCFP("WIN", message.sender.name)
                    display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                    # self.agent.arreter()
                else:
                    self.aleatoire = random.randrange(1, 4)
                    self.banque += self.aleatoire
                    display_message(self.agent.aid.name, 'Je joue ' + str(self.aleatoire))
                    if self.banque == 21:
                        display_message(self.agent.aid.name, 'Score de 21 atteint : J\'ai gagné :) ')
                        self.envoyerCFP("LOSE {}".format(self.agent.aid.name), self.agent.NextJoueur)
                        # self.agent.arreter()
                    elif self.banque > 21:  # Arrêt du jeu
                        self.envoyerCFP("ARRET {}".format(self.agent.aid.name), self.agent.NextJoueur)
                        display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                        # self.agent.arreter()
                    else:
                        self.envoyerCFP(str(self.banque), self.agent.NextJoueur)


if __name__ == '__main__':
    agents = []
    joueurs = []
    port = 2000

    j1_name = 'selma_{}@localhost:{}'.format(port, port)
    j2_name = 'reuelle_{}@localhost:{}'.format(port + 1, port + 1)
    j3_name = 'manel_{}@localhost:{}'.format(port + 2, port + 2)
    j1 = Joueur(AID(name=j1_name), j2_name)
    j2 = Joueur(AID(name=j2_name), j3_name)
    j3 = Joueur(AID(name=j3_name), j1_name)

    joueurs.append(j1_name)
    joueurs.append(j2_name)
    joueurs.append(j3_name)
    random.shuffle(joueurs)

    j1.J2 = j2.J2 = j3.J2 = joueurs[1]
    agents.append(j1)
    agents.append(j2)
    agents.append(j3)

    start_loop(agents)
