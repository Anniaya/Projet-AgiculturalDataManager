from data_manager import AgriculturalDataManager

# Initialiser et tester le DataManager
data_manager = AgriculturalDataManager()
data_manager.load_data()
features = data_manager.prepare_features(data_manager.monitoring_data)
# Tester quelques fonctionnalités
parcelle_id = 'P001'
history, trend = data_manager.get_temporal_patterns(parcelle_id)
risk_metrics = data_manager.calculate_risk_metrics(features)

print(f"Tendance de rendement : {trend['pente']:.2f} tonnes/ha/an")
print ( f"Variation moyenne : { trend['variation_moyenne']*100 :.1f}%" )
