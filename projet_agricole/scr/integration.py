class IntegratedDashboard:
    def __init__(self, data_manager):
        """
        Crée un tableau de bord intégré combinant
        graphiques Bokeh et carte Folium
        """
        self.data_manager = data_manager
        self.bokeh_dashboard = AgriculturalDashboard(data_manager)
        self.map_view = AgriculturalMap(data_manager)

    def initialize_visualizations(self):
        """
        Initialise toutes les composantes visuelles
        """
        # Initialiser les visualisations Bokeh et Folium
        self.bokeh_dashboard.initialize_charts()
        self.map_view.initialize_map()

    def create_streamlit_dashboard(self):
        """
        Crée une interface Streamlit intégrant toutes les visualisations
        """
        import streamlit as st

        st.title("Tableau de Bord Agricole Intégré")

        # Ajouter les visualisations dans Streamlit
        st.header("Visualisations Agricoles")
        
        # Afficher la carte Folium
        st.subheader("Carte des Parcelles Agricoles")
        folium_map = self.map_view.get_map()
        st.components.v1.html(folium_map._repr_html_(), height=500)

        # Afficher les graphiques Bokeh
        st.subheader("Graphiques Agricoles")
        bokeh_charts = self.bokeh_dashboard.get_charts()
        for chart in bokeh_charts:
            st.bokeh_chart(chart)

    def update_visualizations(self, parcelle_id):
        """
        Met à jour toutes les visualisations pour une parcelle donnée
        """
        # Mettre à jour les visualisations en fonction de la parcelle sélectionnée
        self.bokeh_dashboard.update_charts(parcelle_id)
        self.map_view.update_map(parcelle_id)
    
    ##########
    def setup_interactions(self):
        """
    Configure les interactions entre les composantes Bokeh et Folium.
        """
    # Configurer les interactions Bokeh
        if hasattr(self.bokeh_dashboard, 'parcelle_select'):
            self.bokeh_dashboard.parcelle_select.on_change('value', self.handle_parcelle_selection)

    # Configurer les interactions Folium
        if hasattr(self.map_view, 'map'):
            self.map_view.map.add_child(self.map_view.get_hover_handler(self.handle_map_hover))

    def handle_parcelle_selection(self, attr, old, new):
        """
    Gère la sélection d’une nouvelle parcelle.
    Met à jour les visualisations en fonction de la parcelle sélectionnée.
        """
        if new:
            parcelle_id = new
            print(f"Parcelle sélectionnée : {parcelle_id}")

        # Mettre à jour les graphiques Bokeh
            if hasattr(self.bokeh_dashboard, 'update_charts'):
                self.bokeh_dashboard.update_charts(parcelle_id)

        # Mettre à jour la carte Folium
            if hasattr(self.map_view, 'update_map'):
                self.map_view.update_map(parcelle_id)

    def handle_map_hover(self, feature):
        """
    Gère le survol d’une parcelle sur la carte.
    Met en évidence la parcelle sur les graphiques.
        """
        if feature and 'id' in feature['properties']:
            parcelle_id = feature['properties']['id']
            print(f"Parcelle survolée : {parcelle_id}")

        # Mettre en évidence la parcelle sur les graphiques Bokeh
        if hasattr(self.bokeh_dashboard, 'highlight_parcelle'):
            self.bokeh_dashboard.highlight_parcelle(parcelle_id)