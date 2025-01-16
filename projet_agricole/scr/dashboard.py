from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, Select, DateRangeSlider, HoverTool, ColorBar, LinearColorMapper
from bokeh.plotting import figure
import pandas as pd
from bokeh.palettes import RdYlBu11 as palette
import bokeh.plotting as bk
from bokeh.models import Select
from data_manager import AgriculturalDataManager
class AgriculturalDashboard:
    def __init__(self, data_manager):
        """
        Initialise le tableau de bord avec le gestionnaire de données.
        Le gestionnaire de données (data_manager) doit avoir chargé :
        - Les données de monitoring actuelles
        - L’historique des rendements
        - Les données météorologiques
        - Les caractéristiques des sols
        """
        self.data_manager = data_manager
        # self.data_manager = AgriculturalDataManager()
        self.source = None
        self.hist_source = None
        self.selected_parcelle = None
        self.create_data_sources()
    def create_data_sources(self):
        """
        Prépare les sources de données pour Bokeh en intégrant
        les données actuelles et historiques.
        """
        if self.data_manager.yield_history is None:
            raise ValueError("yield_history is not loaded in data_manager.")
        if self.data_manager.monitoring_data is None:
            raise ValueError("monitoring_data is not loaded in data_manager.")
        yield_history_df = self.data_manager.yield_history.reset_index(drop=True)
        monitoring_data_df = self.data_manager.monitoring_data.reset_index(drop=True)
        self.hist_source = ColumnDataSource(yield_history_df)
        self.source = ColumnDataSource(monitoring_data_df)
    def create_yield_history_plot(self):
        """
        Crée un graphique montrant l’évolution historique des rendements.
        """
        p = figure(
            title="Historique des Rendements par Parcelle",
            x_axis_type="datetime",
            height=400,
            width=800,
            x_axis_label="Date",
            y_axis_label="Rendement Estimé (t/ha)"
        )
        # Utiliser la source globale pour les données
        p.line('date', 'rendement_estime', source=self.hist_source, line_width=2, color='blue', legend_label="Parcelle")
        p.circle('date', 'rendement_estime', source=self.hist_source, size=6, color='blue', alpha=0.5)
        # Ajouter des interactions
        hover = HoverTool(tooltips=[("Date", "@date{%F}"), ("Rendement Estimé", "@rendement_estime"), ("Parcelle", "@parcelle_id")], formatters={"@date": "datetime"})
        p.add_tools(hover)
        p.legend.location = "top_left"
        return p
    def create_ndvi_temporal_plot(self):
        """
        Crée un graphique montrant l’évolution du NDVI avec des seuils.
        """
        # Créer la figure
        p = figure(
            title="Évolution du NDVI et Seuils Historiques",
            x_axis_type="datetime",
            height=400,
            width=800,
            x_axis_label="Date",
            y_axis_label="NDVI"
        )
        # Utiliser la source globale pour les données
        p.line('date', 'ndvi', source=self.source, line_width=2, color='green', legend_label="NDVI")
        p.circle('date', 'ndvi', source=self.source, size=6, color='green', alpha=0.6)
        # Déterminer les limites temporelles
        if len(self.source.data['date']) > 0:
            x_start = min(self.source.data['date'])
            x_end = max(self.source.data['date'])
            # Ajouter les seuils comme lignes indépendantes
            p.line(x=[x_start, x_end], y=[0.4, 0.4], color='red', line_dash='dashed', legend_label="Seuil Bas (0.4)")
            p.line(x=[x_start, x_end], y=[0.7, 0.7], color='blue', line_dash='dashed', legend_label="Seuil Élevé (0.7)")
        # Ajouter des interactions
        hover = HoverTool(tooltips=[("Date", "@date{%F}"), ("NDVI", "@ndvi"), ("Parcelle", "@parcelle_id")], formatters={"@date": "datetime"})
        p.add_tools(hover)
        p.legend.location = "top_left"
        return p
    def create_stress_matrix(self):
        """
        Crée une matrice de stress combinant stress hydrique et météo.
        """
        stress_data = self.prepare_stress_data()
        if stress_data.empty:
            print("Aucune donnée disponible pour la matrice de stress.")
            return figure(title="Matrice de Stress (Données indisponibles)", height=400, width=400)
        mapper = LinearColorMapper(palette=palette, low=stress_data['count'].min(), high=stress_data['count'].max())
        p = figure(
            title="Matrice de Stress",
            x_range=["Stress Hydrique", "Conditions Météo"],
            y_range=["Faible", "Modéré", "Élevé"],
            height=400,
            width=400,
            toolbar_location=None
        )
        p.rect(
            x="stress_type",
            y="stress_hydrique_level",
            width=1,
            height=1,
            source=ColumnDataSource(stress_data),
            fill_color={"field": "count", "transform": mapper},
            line_color=None
        )
        color_bar = ColorBar(color_mapper=mapper, label_standoff=12, location=(0, 0))
        p.add_layout(color_bar, 'right')
        # Ajouter des labels aux axes
        p.xaxis.axis_label = "Type de Stress"
        p.yaxis.axis_label = "Niveau de Stress Hydrique"
        p.title.text_font_size = "16px"
        p.xaxis.major_label_orientation = "vertical"
        return p
    def create_layout(self):
        """
        Organise tous les graphiques et le widget de sélection dans une mise en page.
        """
        parcelle_selector = self.create_parcelle_selector()
        if parcelle_selector is None:
            print("Erreur : Le sélecteur de parcelle n'a pas été créé.")
            return None
        yield_plot = self.create_yield_history_plot()
        ndvi_plot = self.create_ndvi_temporal_plot()
        stress_matrix = self.create_stress_matrix()
        # Ajoutez le sélecteur en haut de la page
        layout = column(parcelle_selector, yield_plot, ndvi_plot, stress_matrix)
        return layout
    # def prepare_stress_data(self):
    #     """
    #     Prépare les données pour la matrice de stress.
    #     """
    #     data = self.data_manager.prepare_features()
    #     # Renommer les colonnes ambiguës si nécessaire
    #     data.rename(columns={'date_x': 'date', 'date_y': 'date_meteo'}, inplace=True)
    #     # Vérifier les colonnes nécessaires
    #     if 'stress_hydrique' not in data.columns or 'temperature' not in data.columns:
    #         print("Colonnes nécessaires manquantes dans les données.")
    #         return pd.DataFrame()
    #     # Remplir les valeurs manquantes
    #     data['stress_hydrique'].fillna(0, inplace=True)
    #     data['temperature'].fillna(data['temperature'].mean(), inplace=True)
    #     # Catégoriser les niveaux de stress
    #     data['stress_hydrique_level'] = pd.cut(data['stress_hydrique'],
    #                                         bins=[0, 0.05, 0.1, 1],
    #                                         labels=["Faible", "Modéré", "Élevé"])
    #     data['stress_type'] = data['temperature'].apply(
    #         lambda x: "Conditions Météo" if x > 30 or x < 5 else "Stress Hydrique")
    #     # Compter les occurrences pour chaque catégorie
    #     stress_data = data.groupby(['stress_hydrique_level', 'stress_type']).size().reset_index(name='count')
    #     return stress_data
    def prepare_stress_data(self):
        """
        Prépare les données pour la matrice de stress.
        """
        # Pass monitoring_data or any relevant DataFrame to prepare_features
        data = self.data_manager.prepare_features()
        # Renommer les colonnes ambiguës si nécessaire
        if 'date_x' in data.columns or 'date_y' in data.columns:
            data.rename(columns={'date_x': 'date', 'date_y': 'date_meteo'}, inplace=True)

        # Vérifier les colonnes nécessaires
        if 'stress_hydrique' not in data.columns or 'temperature' not in data.columns:
            print("Colonnes nécessaires manquantes dans les données.")
            return pd.DataFrame()

        # Remplir les valeurs manquantes
        data['stress_hydrique'].fillna(0, inplace=True)
        data['temperature'].fillna(data['temperature'].mean(), inplace=True)
        # Catégoriser les niveaux de stress
        data['stress_hydrique_level'] = pd.cut(
            data['stress_hydrique'],
            bins=[0, 0.05, 0.1, 1],
            labels=["Faible", "Modéré", "Élevé"]
        )
        data['stress_type'] = data['temperature'].apply(
            lambda x: "Conditions Météo" if x > 30 or x < 5 else "Stress Hydrique"
        )
        # Compter les occurrences pour chaque catégorie
        stress_data = data.groupby(['stress_hydrique_level', 'stress_type']).size().reset_index(name='count')
        return stress_data
    def get_parcelle_options(self):
        """
        Retourne la liste des parcelles disponibles dans les données de monitoring.
        """
        if self.data_manager.monitoring_data is not None:
            # Récupère les parcelles uniques
            return sorted(self.data_manager.monitoring_data['parcelle_id'].unique())
        else:
            print("Erreur : Les données de monitoring ne sont pas chargées.")
            return []
        
    def create_parcelle_selector(self):
        """
        Crée un widget de sélection de parcelle.
        """
        parcelle_ids = self.get_parcelle_options()
        parcelle_selector = Select(
            title="Sélectionnez une parcelle",
            value=parcelle_ids[0],  # Première parcelle par défaut
            options=parcelle_ids    # Liste des parcelles
        )
        parcelle_selector.on_change('value', self.update_plots)  # Lien avec le callback
        return parcelle_selector
    def update_plots(self, attr, old, new):
        """
        Met à jour les graphiques lorsqu'une nouvelle parcelle est sélectionnée.
        """
        parcelle_id = new  # Nouvelle valeur sélectionnée dans le sélecteur
        print(f"Parcelle sélectionnée : {parcelle_id}")
        # Filtrer les données de monitoring et d'historique pour la parcelle sélectionnée
        updated_monitoring_data = self.data_manager.monitoring_data[self.data_manager.monitoring_data['parcelle_id'] == parcelle_id]
        updated_yield_history = self.data_manager.yield_history[self.data_manager.yield_history['parcelle_id'] == parcelle_id]
        # Mettre à jour les sources de données
        self.source.data = ColumnDataSource.from_df(updated_monitoring_data)
        self.hist_source.data = ColumnDataSource.from_df(updated_yield_history)
        print("Sources de données mises à jour pour la parcelle :", parcelle_id)
    def update_parcelle(self, parcelle_id):
        """
        Met à jour les graphiques pour une parcelle donnée.
        """
        updated_data = self.data_manager.monitoring_data[
            self.data_manager.monitoring_data['parcelle_id'] == parcelle_id
        ]

        if updated_data.empty:
            print(f"Aucune donnée disponible pour la parcelle {parcelle_id}.")
            return

        # Mettre à jour les sources Bokeh
        self.source.data = ColumnDataSource.from_df(updated_data)
        self.hist_source.data = ColumnDataSource.from_df(
        self.data_manager.yield_history[self.data_manager.yield_history['parcelle_id'] == parcelle_id]
        )