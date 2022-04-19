from pade.acl import aid
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
        display_message(self.agent.aid.name, 'Je suis un joueur')
        self.aleatoire = 0
        self.banque = 0

    def on_start(self):
        if self.agent.JoueurNom == self.agent.J2:  # Le joueur 2 commence à jouer directement
            display_message(self.agent.aid.name, 'Je commence la partie')
            self.aleatoire = random.randrange(1, 4)
            self.banque += self.aleatoire
            display_message(self.agent.aid.name,
                            'Je joue ' + str(self.aleatoire) + '. Score actuel: ' + str(self.banque))
            display_message(self.agent.aid.name, ' Score envoyé à {}'.format(self.agent.NextJoueur))
            reponse = ACLMessage(ACLMessage.CFP)
            reponse.set_content(str(self.banque))
            reponse.add_receiver(self.agent.NextJoueur)
            self.agent.send(reponse)

    def execute(self, message):
        if message.performative == ACLMessage.CFP:  # Le joueur 1 reçoit une demande de proposition du joueur 2
            display_message(self.agent.aid.name,
                            'Score actuel: ' + message.content + ' envoyé par : {}'.format(message.sender.name))
            self.banque = int(message.content)
            if self.banque > 21:  # Arrêt du jeu
                display_message(self.agent.aid.name, ' Le score de ' + str(self.banque) +
                                ' est supérieur à 21 ' + message.sender.name)
                refus = ACLMessage(ACLMessage.INFORM)
                refus.set_content("ARRET")
                refus.add_receiver(message.sender.name)
                self.agent.send(refus)
                self.agent.arreter()
            elif self.banque == 21:  # Le joueur 2 gagne
                reponse = ACLMessage(ACLMessage.INFORM)
                reponse.set_content("WIN")
                reponse.add_receiver(message.sender.name)
                self.agent.send(reponse)
                display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                self.agent.arreter()
            else:
                self.aleatoire = random.randrange(1, 4)
                self.banque += self.aleatoire
                display_message(self.agent.aid.name, 'Je joue ' + str(self.aleatoire))
                if self.banque == 21:  # Le joueur 1 gagne
                    display_message(self.agent.aid.name, 'Score atteint de ' + str(self.banque))
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("LOSE")
                    reponse.add_receiver(message.sender.name)
                    self.agent.send(reponse)
                    display_message(self.agent.aid.name, 'J\'ai gagné :)')
                    self.agent.arreter()
                elif self.banque > 21:  # Arrêt du jeu
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("ARRET")
                    reponse.add_receiver(message.sender.name)
                    self.agent.send(reponse)
                    display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                    self.agent.arreter()
                else:
                    reponse = ACLMessage(ACLMessage.PROPOSE)
                    reponse.set_content(str(self.banque))
                    reponse.add_receiver(self.agent.NextJoueur)
                    self.agent.send(reponse)
        if message.performative == ACLMessage.PROPOSE:  # Le joueur 2 reçoit les propositions du joueur 1
            display_message(self.agent.aid.name,
                            'Score actuel: ' + message.content + ' envoyé par : {}'.format(message.sender.name))
            self.banque = int(message.content)
            if self.banque > 21:  # Arrêt du jeu
                display_message(self.agent.aid.name, 'Le score de ' + str(self.banque) +
                                ' est supérieur à 21 ' + message.sender.name)
                refus = ACLMessage(ACLMessage.INFORM)
                refus.set_content("ARRET")
                refus.add_receiver(message.sender.name)
                self.agent.send(refus)
                self.agent.arreter()
            elif self.banque == 21:  # Le joueur 1 gagne
                reponse = ACLMessage(ACLMessage.INFORM)
                reponse.set_content("WIN")
                reponse.add_receiver(message.sender.name)
                self.agent.send(reponse)
                display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                self.agent.arreter()
            else:
                self.aleatoire = random.randrange(1, 4)
                self.banque += self.aleatoire
                display_message(self.agent.aid.name, 'Je joue ' + str(self.aleatoire))
                if self.banque == 21:  # Le joueur 2 gagne
                    display_message(self.agent.aid.name, 'Score atteint de :' + str(self.banque))
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("LOSE")
                    reponse.add_receiver(message.sender.name)
                    self.agent.send(reponse)
                    display_message(self.agent.aid.name, 'J\'ai gagné :)')
                    self.agent.arreter()
                elif self.banque > 21:  # Arrêt du jeu
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("ARRET")
                    reponse.add_receiver(message.sender.name)
                    self.agent.send(reponse)
                    display_message(self.agent.aid.name, 'Fin du jeu, score supérieur à 21 !')
                    self.agent.arreter()
                else:
                    reponse = ACLMessage(ACLMessage.CFP)
                    reponse.set_content(str(self.banque))
                    reponse.add_receiver(self.agent.NextJoueur)
                    display_message(self.agent.aid.name, 'Score envoyé à {}'.format(self.agent.NextJoueur))
                    self.agent.send(reponse)
        if message.performative == ACLMessage.INFORM:
            resultat = message.content
            if resultat == "WIN":
                display_message(self.agent.aid.name, 'J\'ai gagné :)')
                self.agent.arreter()
            elif resultat == "LOSE":
                display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                self.agent.arreter()
            elif resultat == "ARRET":
                display_message(self.agent.aid.name, 'Fin du jeu,  score supérieur à 21 !')
                self.agent.arreter()


if __name__ == '__main__':
    agents = []
    joueurs = []
    port = 2000

    j1_name = 'selma_{}@localhost:{}'.format(port, port)
    j2_name = 'reuelle_{}@localhost:{}'.format(port + 1, port + 1)
    j1 = Joueur(AID(name=j1_name), j2_name)
    j2 = Joueur(AID(name=j2_name), j1_name)

    joueurs.append(j1_name)
    joueurs.append(j2_name)
    random.shuffle(joueurs)

    j1.J2 = j2.J2 = joueurs[1]
    agents.append(j1)
    agents.append(j2)

    start_loop(agents)
