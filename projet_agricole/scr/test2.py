# test.py
from map_visualsition import AgiculturalMap
from data_manager import AgriculturalDataManager

def main():
    # Initialiser le gestionnaire de données
    data_manager = AgriculturalDataManager()
    data_manager.load_data()
    # Créer une carte agricole
    agri_map = AgiculturalMap(data_manager)
    
    # Créer la carte de base
    agri_map.create_base_map()
    
    # Ajouter les différentes couches (historique des rendements, NDVI, carte de chaleur des risques)
    agri_map.add_yield_history_layer()
    agri_map.add_current_ndvi_layer()
    agri_map.add_risk_heatmap()
    
    # Sauvegarder la carte
    agri_map.save_map("agricultural_map.html")
    
    # Tester la fonction de tendance des rendements
    history = data_manager.yield_history[['date', 'yield']]  # Juste un exemple de données historiques
    trend = agri_map._create_yield_trend(history)
    print(f"Tendance des rendements : {trend}")

if __name__ == "__main__":
    main()
