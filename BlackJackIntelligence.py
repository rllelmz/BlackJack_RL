from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.behaviours.protocols import Behaviour
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
import random
import sys


class Juge(Agent):
    def __init__(self, aid):
        super(Juge, self).__init__(aid=aid, debug=False)
        print(" === ====================================== === \n")
        print(" ===              Simple Blackjack          === \n")
        print(" === ====================================== === \n")
        self.call_later(8, self.initialize_send)

    def initialize_send(self):
        juge_behaviour = JugeBehaviour(self)
        self.behaviours.append(juge_behaviour)
        juge_behaviour.on_start()

    def arreter(self):
        self.pause_agent
        self.behaviours = []


class JugeBehaviour(Behaviour):
    def __init__(self, agent):
        super().__init__(agent)
        self.banque = 0
        self.cpt = 0

    def envoyerMessage(self, dest, message):
        msg = ACLMessage(ACLMessage.CFP)
        msg.add_receiver(dest)
        msg.set_content(str(message))
        self.agent.send(msg)

    def on_start(self):
        display_message(self.agent.aid.name, 'Envoi du premier message à : {}'.format(self.agent.receivers[1]))
        self.envoyerMessage(self.agent.receivers[1], self.banque)  # Joueur 2 commence

    def execute(self, message):
        if message.performative == ACLMessage.PROPOSE:
            display_message(self.agent.aid.name,
                            'J\'ai reçu la valeur ' + message.content + ' de : {}'.format(message.sender.name))
            if self.banque + int(message.content) > 21:
                # Le nombre est rejeté & n'est pas ajouté à la banque
                display_message(self.agent.aid.name, 'La résultat de ' + str(
                    self.banque) + ' + ' + message.content + ' est supérieur à 21 !!' + message.sender.name)
                refus = ACLMessage(ACLMessage.INFORM)
                refus.set_content("ARRET")
                refus.add_receiver(message.sender.name)
                self.agent.send(refus)
                self.agent.arreter()
            else:
                # Le nombre est ajouté à la banque
                self.banque += int(message.content)
                if self.banque == 21:
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("WIN")
                    reponse.add_receiver(message.sender.name)
                    self.agent.send(reponse)
                    display_message(self.agent.aid.name, '{} a gagné !'.format(message.sender.name))
                    reponse = ACLMessage(ACLMessage.INFORM)
                    reponse.set_content("LOSE")
                    for receiver in self.agent.receivers:
                        if receiver != message.sender.name:
                            reponse.add_receiver(receiver)
                    self.agent.send(reponse)
                    self.agent.arreter()
                else:
                    display_message(self.agent.aid.name, 'Score actuel : ' + str(self.banque))
                    reponse = ACLMessage(ACLMessage.CFP)
                    reponse.set_content(str(self.banque))
                    for receiver in self.agent.receivers:
                        if receiver != message.sender.name:
                            reponse.add_receiver(receiver)
                            display_message(self.agent.aid.name, 'Envoi du score actuel à {} '.format(receiver))
                    self.agent.send(reponse)


class Joueur(Agent):
    def __init__(self, aid, juge):
        super(Joueur, self).__init__(aid=aid, debug=False)
        display_message(self.aid.name, 'Je suis un joueur !')
        self.banque = 0
        self.JoueurNom = self.aid.name
        self.J2 = "null"
        self.juge = juge
        self.behaviours.append(JoueurBehaviour(self))

    def arreter(self):
        self.pause_agent
        self.behaviours = []


class JoueurBehaviour(Behaviour):

    def __init__(self, agent):
        super().__init__(agent)
        self.aleatoire = 0

    def on_start(self):
        if self.agent.JoueurNom == self.agent.J2:
            display_message(self.agent.aid.name, 'Je suis le Joueur_2')
        else:
            display_message(self.agent.aid.name, 'Je suis le Joueur_1')

    def execute(self, message):
        if message.performative == ACLMessage.CFP:
            if int(message.content) == 18:
                self.aleatoire = 3
                display_message(self.agent.aid.name, 'Je joue 3')
            elif int(message.content) == 19:
                self.aleatoire = 2
                display_message(self.agent.aid.name, 'Je joue 2')
            else:
                self.aleatoire = 1
                display_message(self.agent.aid.name, 'Je joue 1')
            reponse = ACLMessage(ACLMessage.PROPOSE)
            reponse.set_content(str(self.aleatoire))
            reponse.add_receiver(self.agent.juge)
            self.agent.send(reponse)
        if message.performative == ACLMessage.INFORM:
            resultat = message.content
            if resultat == "WIN":
                display_message(self.agent.aid.name, 'J\'ai gagné :)')
                self.agent.arreter()
            if resultat == "LOSE":
                display_message(self.agent.aid.name, 'J\'ai perdu :\'(')
                self.agent.arreter()
            elif resultat == "ARRET":
                display_message(self.agent.aid.name, 'Fin du jeu :\'(')
                self.agent.arreter()


if __name__ == '__main__':
    agents = []
    joueurs = []
    port = 2000

    juge_name = 'juge_{}@localhost:{}'.format(port, port)
    juge = Juge(AID(name=juge_name))

    j1_name = 'selma_{}@localhost:{}'.format(port + 1, port + 1)
    joueurs.append(j1_name)
    j1 = Joueur(AID(name=j1_name), juge_name)

    j2_name = 'reuelle_{}@localhost:{}'.format(port + 2, port + 2)
    joueurs.append(j2_name)
    j2 = Joueur(AID(name=j2_name), juge_name)

    random.shuffle(joueurs)
    juge.receivers = joueurs
    j1.J2 = j2.J2 = juge.receivers[1]

    agents.append(juge)
    agents.append(j1)
    agents.append(j2)

    start_loop(agents)
