import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from flask import Flask

# --- YOUR ORIGINAL BACKEND CODE ---
flask_app = Flask(__name__)

@flask_app.route('/scan')
def scan_route():
    # This acts as the gateway route you originally created!
    return "Scan Triggered"

def run_flask():
    # Starts the background network server link
    flask_app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# --- YOUR MOBILE SCREEN DESIGN ---
class WifiConnectApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Title text label
        self.label = Label(
            text="Wifi Connect App\nDeveloper Edition", 
            font_size='24sp', 
            halign='center'
        )
        layout.add_widget(self.label)
        
        # Purple UI Button
        btn = Button(
            text="Run Wifi Speed & Device Scan", 
            size_hint=(1, 0.25), 
            background_color=(0.6, 0.2, 0.8, 1)  # Purple color
        )
        btn.bind(on_press=self.start_scan)
        layout.add_widget(btn)
        
        # Start your background Flask link safely in a thread
        threading.Thread(target=run_flask, daemon=True).start()
        
        return layout

    def start_scan(self, instance):
        self.label.text = "Checking connected devices...\nRunning speed test..."

if __name__ == '__main__':
    WifiConnectApp().run()
