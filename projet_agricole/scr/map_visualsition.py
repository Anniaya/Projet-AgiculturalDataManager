import folium
from folium import plugins 
from branca.colormap import LinearColormap
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
class AgiculturalMap:
    def __init__(self, data_manager):
       """ 
        initialise la carte avec le gestionnaire de données
        """
       self.data_manager = data_manager
       self.map = None
       self.yield_colormap = LinearColormap(
           colors=['red', 'yellow', 'green'],
           vmin=0,
           vmax=12 # rendement maximum en tonnes:ha
       )

    def create_base_map(self, location=[45.0, 5.0], zoom_start=6):
        """ Crée la carte de base avec les couches appropriées
        """
        self.map = folium.Map(location= [51.5074, -0.1278], zoom_start=10)
        folium.TileLayer('OpenStreetMap').add_to(self.map)
        folium.TileLayer('Stamen Terrain',
                         attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(self.map)
        folium.LayerControl().add_to(self.map)
        
    def add_yield_history_layer(self):
       """ Ajoute une couche visualisant l'historique des rendements """
    
    # Afficher les colonnes du DataFrame soil_data
       print("Colonnes disponibles dans soil_data : ", self.data_manager.soil_data.columns)
    
    # Assurez-vous que les colonnes existent dans soil_data
       if 'latitude' not in self.data_manager.soil_data.columns or 'longitude' not in self.data_manager.soil_data.columns:
        print("Les colonnes 'latitude' ou 'longitude' sont manquantes dans soil_data.")
        return
    
    # Afficher les premières lignes pour vérifier les données de soil_data
        print(self.data_manager.soil_data.head())
    
    # Ajouter les cercles de données à la carte à partir de soil_data
        for _, row in self.data_manager.soil_data.iterrows():
            if pd.notnull(row['latitude']) and pd.notnull(row['longitude']):
               mean_yield = row['rendement_estime']  # Remplacez par la colonne correcte pour le rendement
            popup_content = self._create_yield_popup(
                row['rendement_estime'], mean_yield, row['progression']
            )
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                color=self.yield_colormap(mean_yield),
                fill=True,
                fill_opacity=0.8,
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(self.map)


            
    
    def add_current_ndvi_layer(self):
        """ ajoute une couche de la situation NDVI actuelle
        """
        for _, row in self.data_manager.soil_data.iterrows():
            popup_content = self._create_ndvi_popup(row)
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=8,
                color='blue',
                fill=True,
                fill_opacity=0.6,
                popup=folium.Popup(popup_content, max_width=300),
            ).add_to(self.map)
        
    def add_risk_heatmap(self):
        """ ajoute une carte de chaleur des zones à rique
        """
        risk_data = self.data_manager.risk_data[['latitude', 'longitude', 'risk_score']]
        plugins.HeatMap(risk_data, radius=15).add_to(self.map)
        


    def _create_yield_trend(self, history):
        """
    Calcule la tendance des rendements pour une parcelle
    Utilise la régression linéaire pour déterminer la tendance.
    
    history : pd.DataFrame
        Un DataFrame contenant des données historiques sur les rendements, avec au moins deux colonnes:
        - 'date' : les dates des rendements (au format datetime ou string convertible en datetime)
        - 'yield' : les rendements pour ces dates.
        """
    # Assurez-vous que les données sont bien formatées (par exemple, la colonne 'date' doit être au format datetime)
        history['date'] = pd.to_datetime(history['date'])
    
    # Convertir les dates en nombres (nombre de jours depuis la première date)
        history['days_since_start'] = (history['date'] - history['date'].min()).dt.days
    
    # Créer les données pour la régression
        X = history['days_since_start'].values.reshape(-1, 1)  # X = jours depuis le début
        y = history['yield'].values  # y = rendements
    
    # Appliquer la régression linéaire
        model = LinearRegression()
        model.fit(X, y)
    
    # Calcul de la pente et de l'ordonnée à l'origine (intercept)
        trend_slope = model.coef_[0]  # Pente de la régression (tendance)
    
    # Déterminer si la tendance est positive ou négative
        if trend_slope > 0:
           trend = "Croissante"
        elif trend_slope < 0:
           trend = "Décroissante"
        else:
           trend = "Stable"
    
    # Retourner la tendance sous forme de chaîne de caractères
        return trend

        
    
    def _create_yield_popup (self, history, mean_yield, trend):
        """ crée le contenu HTML du popup pour l'historique 
        des rendements
        """
        if mean_yield is None:
           mean_yield = "Non disponible"  # ou toute autre valeur par défaut
        else:
           mean_yield = f"{mean_yield:.2f}"  # Formate la valeur avec 2 décimales

        return f"""
        <b>Historique des rendements</b><br>
        Moyenne : {mean_yield} t/ha<br>
        Tendance : {trend}<br>
        Historique : {history}
        """
        
        
    def _create_ndvi_popup(self, row):
        """ crée le contenu HTML du popup pour les données NDVI actuelles
        """
        return f"""
        <b>NDVI Actuel</b><br>
        Parcelle : {row['parcelle_id']}<br>
        NDVI : {row['ndvi']:.2f}<br>
        Localisation : ({row['latitude']:.3f}, {row['longitude']:.3f})
        """
    def save_map(self, filepath="agricultural_map.html"):
        """
        Sauvegarde la carte dans un fichier HTML
        """
        if self.map:
            self.map.save(filepath)
        else:
            raise ValueError("La carte n'a pas été créée. Appelez d'abord create_base_map().")  
       