from bokeh.io import curdoc
from dashboard import AgriculturalDashboard  # Importez la classe
from data_manager import AgriculturalDataManager  # Importez votre gestionnaire de données

# Charger les données avec le gestionnaire de données
data_manager = AgriculturalDataManager()
data_manager.load_data()

# Initialiser le tableau de bord
dashboard = AgriculturalDashboard(data_manager)

# Créer la mise en page
layout = dashboard.create_layout()

# Ajouter la mise en page au document Bokeh
curdoc().add_root(layout)
curdoc().title = "Tableau de Bord Agricole"


# Crée la mise en page
layout = dashboard.create_layout()

# Affiche des informations pour le débogage
merged_data = data_manager.prepare_features()
print("Aperçu des données fusionnées :")
print(merged_data.columns)

stress_data = dashboard.prepare_stress_data()
print("Données préparées pour la matrice de stress :")
print(stress_data)
print("Valeur de yield_history :", data_manager.yield_history)