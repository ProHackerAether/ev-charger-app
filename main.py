import asyncio
import threading
import random
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy_garden.mapview import MapView, MapMarkerPopup

# ---------------------------------------------------------
# UI Layout (The Screen Design)
# ---------------------------------------------------------
KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "ZeroCost EV Aggregator"
            elevation: 4
            right_action_items: [["refresh", lambda x: app.refresh_map()]]

        RelativeLayout:
            id: map_container
'''

# ---------------------------------------------------------
# Custom Map Pin
# ---------------------------------------------------------
class StationMarker(MapMarkerPopup):
    def __init__(self, station_data, **kwargs):
        super().__init__(**kwargs)
        self.station_data = station_data
        self.lat = station_data['lat']
        self.lon = station_data['lon']
        # Standard blue bubble icon provided by Kivy
        self.source = "atlas://data/images/defaulttheme/bubble"
        self.bind(on_release=self.on_marker_click)

    def on_marker_click(self, instance):
        app = MDApp.get_running_app()
        app.show_station_details(self.station_data)

# ---------------------------------------------------------
# Main App Logic
# ---------------------------------------------------------
class EVMapApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        screen = Builder.load_string(KV)
        
        # 1. Create Map centered on Bhopal, India
        self.map_view = MapView(zoom=10, lat=23.2599, lon=77.4126)
        
        # 2. Set Satellite Mode (Esri World Imagery)
        self.map_view.map_source.url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
        self.map_view.map_source.attribution = "Esri, USGS, NOAA"
        
        screen.ids.map_container.add_widget(self.map_view)
        return screen

    def on_start(self):
        self.refresh_map()

    def refresh_map(self):
        threading.Thread(target=self.fetch_stations_thread).start()

    def fetch_stations_thread(self):
        # SIMULATION: We generate fake data here because scraping requires 
        # complex legal checks. This proves the App works.
        import time
        time.sleep(1) # Fake loading time
        
        new_stations = []
        center_lat = self.map_view.lat
        center_lon = self.map_view.lon
        
        for i in range(15):
            new_stations.append({
                'operator': random.choice(['Jio-bp', 'Tata Power', 'Statiq']),
                'lat': center_lat + random.uniform(-0.05, 0.05),
                'lon': center_lon + random.uniform(-0.05, 0.05),
                'status': random.choice(['Available', 'Busy']),
                'power': "60 kW"
            })
            
        Clock.schedule_once(lambda x: self.update_markers(new_stations), 0)

    def update_markers(self, stations):
        # Remove old markers
        layer = self.map_view._scatter
        for child in layer.children[:]:
            if isinstance(child, StationMarker):
                layer.remove_widget(child)
        
        # Add new markers
        for s in stations:
            self.map_view.add_marker(StationMarker(station_data=s))

    def show_station_details(self, data):
        # The Bottom Sheet Popup
        content = MDBoxLayout(orientation='vertical', padding="20dp", spacing="10dp", size_hint_y=None)
        content.height = "180dp"
        
        lbl_title = MDLabel(text=f"{data['operator']} Station", font_style="H6", theme_text_color="Custom", text_color=(1,1,1,1))
        lbl_status = MDLabel(text=f"Status: {data['status']}", theme_text_color="Custom", text_color=(0,1,0,1) if data['status']=='Available' else (1,0,0,1))
        
        btn_nav = MDFillRoundFlatButton(
            text="OPEN GOOGLE MAPS", 
            pos_hint={"center_x": .5},
            on_release=lambda x: self.open_google_maps(data['lat'], data['lon'])
        )
        
        content.add_widget(lbl_title)
        content.add_widget(lbl_status)
        content.add_widget(btn_nav)
        
        self.bs = MDCustomBottomSheet(screen=content)
        self.bs.open()

    def open_google_maps(self, lat, lon):
        # Android specific code to open the real Google Maps App
        if platform == 'android':
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(f"google.navigation:q={lat},{lon}"))
            intent.setPackage("com.google.android.apps.maps")
            from org.kivy.android import PythonActivity
            PythonActivity.mActivity.startActivity(intent)

if __name__ == "__main__":
    EVMapApp().run()

