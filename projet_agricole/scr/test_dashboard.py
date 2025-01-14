from bokeh.plotting import output_file, save, show
from dashboard import AgriculturalDashboard
from data_manager import AgriculturalDataManager

# Initialisation
data_manager = AgriculturalDataManager()
data_manager.load_data()  # Assure-toi que cette méthode charge correctement les données

# Passe l'instance de data_manager à AgriculturalDashboard
dashboard = AgriculturalDashboard(data_manager)

# Crée la mise en page
layout = dashboard.create_layout()

# Affiche des informations pour le débogage
merged_data = data_manager.prepare_features()
print("Aperçu des données fusionnées :")
print(merged_data.columns)

stress_data = dashboard.prepare_stress_data()
print("Données préparées pour la matrice de stress :")
print(stress_data)
