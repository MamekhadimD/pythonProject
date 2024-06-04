from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Tache:
    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
        dependances: List["Tache"] = None,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances = dependances or []

    def ajouter_dependance(self, tache: "Tache"):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut


class Equipe:
    def __init__(self):
        self.membres = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres


class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    def __init__(self, description: str, version: int):
        self.description = description
        self.version = version
        self.date = datetime.now()


class NotificationStrategy(ABC):
    @abstractmethod
    def envoyer_message(self, message: str, destinataire: Membre):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    def envoyer_message(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par Push: {message}")


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        for destinataire in destinataires:
            self.strategy.envoyer_message(message, destinataire)


class Projet:
    def __init__(
        self, nom: str, description: str, date_debut: datetime, date_fin: datetime, budget: float = 0.0
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches = []
        self.equipe = Equipe()
        self.risques = []
        self.jalons = []
        self.version = 1
        self.changements = []
        self.chemin_critique = []
        self.notification_context = None

    def ajouter_membre(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def generer_rapport_performance(self):
        rapport = f"Performance Report for Project '{self.nom}':\n"
        # Ajoutez le contenu du rapport ici
        return rapport




    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(
            f"Le budget du projet a été défini à {self.budget} Unité Monétaire"
        )

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}")

    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version)
        self.changements.append(changement)
        self.version += 1
        self.notifier(f"Changement enregistré: {description} (version {self.version})")

    def calculer_chemin_critique(self):
        def find_longest_path(tache, memo):
            if tache in memo:
                return memo[tache]
            if not tache.dependances:
                memo[tache] = (0, [tache])
                return memo[tache]
            max_length, max_path = 0, []
            for dep in tache.dependances:
                dep_length, dep_path = find_longest_path(dep, memo)
                if dep_length > max_length:
                    max_length = dep_length
                    max_path = dep_path
            total_length = max_length + (tache.date_fin - tache.date_debut).days
            memo[tache] = (total_length, max_path + [tache])
            return memo[tache]

        memo = {}
        all_paths = [find_longest_path(tache, memo) for tache in self.taches]
        self.chemin_critique = max(all_paths, key=lambda x: x[0])[1]

    def notifier(self, message: str):
        if self.notification_context:
            self.notification_context.notifier(message, self.equipe.membres)

    def generer_rapport(self):
        rapport = f"Rapport d'activités du Projet '{self.nom}':\n"
        rapport += f"Version: {self.version}\n"
        rapport += f"Dates: {self.date_debut} à {self.date_fin}\n"
        rapport += f"Budget: {self.budget} Unité Monétaire\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.membres:
            rapport += f"- {membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"- {tache.nom} ({tache.date_debut} à {tache.date_fin}), Responsable: {tache.responsable.nom}, Statut: {tache.statut}\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"- {jalon.nom} ({jalon.date})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"- {risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})\n"
        rapport += "Chemin Critique:\n"
        for tache in self.chemin_critique:
            rapport += f"- {tache.nom} ({tache.date_debut} à {tache.date_fin})\n"
        return rapport


# Création des membres
modou = Membre("Modou", "Chef de projet")
christian = Membre("Christian", "Développeur")

# Création du projet
projet = Projet(
    "Nouveau Produit",
    "Développement d'un nouveau produit",
    datetime(2024, 1, 1),
    datetime(2024, 12, 31),
)

# Définir la stratégie de notification par email
email_strategy = EmailNotificationStrategy()
projet.set_notification_strategy(email_strategy)

# Ajouter des membres à l'équipe
projet.ajouter_membre_equipe(modou)
projet.ajouter_membre_equipe(christian)

# Ajouter des tâches
tache1 = Tache(
    "Analyse des besoins",
    "Description de l'analyse des besoins",
    datetime(2024, 1, 1),
    datetime(2024, 1, 31),
    modou,
    "Terminée",
)
tache2 = Tache(
    "Développement",
    "Description du développement",
    datetime(2024, 2, 1),
    datetime(2024, 6, 30),
    christian,
    "Non démarrée",
    dependances=[tache1],
)

projet.ajouter_tache(tache1)
projet.ajouter_tache(tache2)

# Définir le budget
projet.definir_budget(50000.0)

# Ajouter un risque
risque = Risque("Retard de livraison", 0.3, "Élevé")
projet.ajouter_risque(risque)

# Ajouter un jalon
jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
projet.ajouter_jalon(jalon)

# Enregistrer un changement
projet.enregistrer_changement("Changement de la portée du projet")

# Calculer le chemin critique
projet.calculer_chemin_critique()

# Générer un rapport
rapport = projet.generer_rapport()
print(rapport)


import unittest
from datetime import datetime
from Projet import Membre, Equipe, Tache, Jalon, Risque, Changement, Projet, EmailNotificationStrategy

class TestProjet(unittest.TestCase):

    def setUp(self):
        self.projet = Projet(
            nom="MEVC",
            description="Projet operationel de fin de cycle",
            date_debut=datetime(2024, 1, 28),
            date_fin=datetime(2024, 4, 30),
            budget=100000
        )
        self.membre1 = Membre(nom="Mame k.Diakhate", role="Chef de projet")
        self.membre2 = Membre(nom="Mouhamed Diakhate", role="Développeur")
        self.tache1 = Tache(
            nom="Tâche 1",
            description="Implementer un systeme de notification par email",
            date_debut=datetime(2024, 3, 15),
            date_fin=datetime(2024, 4, 20),
            responsable=self.membre1,
            statut="En cours"
        )
        self.tache2 = Tache(
            nom="Tâche 2",
            description="Implementer la page de connexion",
            date_debut=datetime(2024, 4, 12),
            date_fin=datetime(2024, 5, 10),
            responsable=self.membre2,
            statut="Pas commencé"
        )

    def test_ajouter_membre(self):
        self.projet.ajouter_membre(self.membre1)
        self.assertIn(self.membre1, self.projet.equipe.obtenir_membres())
        self.projet.ajouter_membre(self.membre2)
        self.assertIn(self.membre2, self.projet.equipe.obtenir_membres())

    def test_ajouter_tache(self):
        self.projet.ajouter_tache(self.tache1)
        self.assertIn(self.tache1, self.projet.taches)
        self.projet.ajouter_tache(self.tache2)
        self.assertIn(self.tache2, self.projet.taches)

    def test_generer_rapport_performance(self):
        # Autres instructions de test
        rapport = self.projet.generer_rapport()
    import unittest
    from datetime import datetime
    from Projet import Membre, Equipe, Tache, Jalon, Risque, Changement, Projet, EmailNotificationStrategy

    class TestProjet(unittest.TestCase):

        def setUp(self):
            self.projet = Projet(
                nom="MEVC",
                description="Projet operationel de fin de cycle",
                date_debut=datetime(2024, 1, 28),
                date_fin=datetime(2024, 4, 30),
            )
            self.membre1 = Membre(nom="Mame K.Diakhate", role="Chef de projet")
            self.membre2 = Membre(nom="Mouhamed Diakhate", role="Développeur")
            self.tache1 = Tache(
                nom="Tâche 1",
                description="Implementer un systeme de notification par email",
                date_debut=datetime(2024, 3, 20),
                date_fin=datetime(2024, 4, 5),
                responsable=self.membre1,
                statut="En cours"
            )
            self.tache2 = Tache(
                nom="Tâche 2",
                description="Implementer la page de connexion",
                date_debut=datetime(2024, 3, 10),
                date_fin=datetime(2024, 4, 15),
                responsable=self.membre2,
                statut="Pas commencé"
            )

        def test_ajouter_membre(self):
            self.projet.ajouter_membre_equipe(self.membre1)
            self.assertIn(self.membre1, self.projet.equipe.membres)
            self.projet.ajouter_membre_equipe(self.membre2)
            self.assertIn(self.membre2, self.projet.equipe.membres)

        def test_ajouter_tache(self):
            self.projet.ajouter_tache(self.tache1)
            self.assertIn(self.tache1, self.projet.taches)
            self.projet.ajouter_tache(self.tache2)
            self.assertIn(self.tache2, self.projet.taches)

        def test_generer_rapport_performance(self):
            self.projet.ajouter_membre_equipe(self.membre1)
            self.projet.ajouter_tache(self.tache1)
            rapport = self.projet.generer_rapport()
            self.assertIn("Rapport d'activités du Projet 'MEVC':", rapport)
            self.assertIn("Nafissatou Sow", rapport)
            self.assertIn("Tâche 1", rapport)

    if __name__ == '__main__':
        unittest.main()
