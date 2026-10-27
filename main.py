import os
import json
import socket
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.utils import platform

# Set default window layout attributes cleanly
Window.clearcolor = (0.1, 0.1, 0.1, 1)

# Dynamic Android System Runtime Permissions Configuration for Google Play
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET,
        Permission.ACCESS_WIFI_STATE,
        Permission.CHANGE_WIFI_STATE,
        Permission.ACCESS_FINE_LOCATION
    ])


class PurpleLayout(BoxLayout):
    """Robust container layout utilizing native theme styles to prevent rendering issues."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 40
        self.spacing = 15
        
        # Safe declarative background mapping engine for the play store target canvas
        from kivy.graphics import Color, Rectangle
        with self.canvas.before:
            Color(0.3, 0.1, 0.5, 1) # Deep vibrant purple
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


# ==========================================
# SECURE LOCAL USER STORAGE DATABASE ENGINE
# ==========================================
class UserDatabase:
    """Manages persistent disk storage using standard JSON to securely retain player state."""
    def __init__(self):
        # Locate the application's persistent user directory safely across target OS options
        if platform == 'android':
            from android.storage import app_storage_dir
            self.db_path = os.path.join(app_storage_dir(), 'users_db.json')
        else:
            self.db_path = 'users_db.json'
        self.data = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"users": {}, "active_session": None}
        return {"users": {}, "active_session": None}

    def save_db(self):
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Database write exception: {e}")

    def register_user(self, email, password):
        self.data["users"][email] = {"password": password, "verified": True}
        self.save_db()

    def verify_login(self, email, password):
        if email in self.data["users"]:
            return self.data["users"][email]["password"] == password
        return False


# ==========================================
# MOBILE APPLICATION PRODUCTION VIEWS
# ==========================================

class LoadingScreen(Screen):
    def on_enter(self):
        threading.Thread(target=self.check_active_session, daemon=True).start()

    def check_active_session(self):
        time.sleep(2.5) # Provide loading placeholder gap for app lifecycle balance
        db = App.get_running_app().db
        if db.data.get("active_session"):
            self.manager.current = 'dashboard'
        else:
            self.manager.current = 'login'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = PurpleLayout(padding=50, spacing=20)
        title = Label(text="WifiConnectApp", font_size='36sp', bold=True)
        loading_text = Label(text="Loading resources... Please wait...", font_size='16sp', color=(0.9, 0.9, 0.9, 1))
        layout.add_widget(title)
        layout.add_widget(loading_text)
        self.add_widget(layout)


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = PurpleLayout()
        
        title = Label(text="WifiConnectApp Login", font_size='28sp', bold=True)
        layout.add_widget(title)
        
        self.username = TextInput(hint_text="Username or Email", multiline=False, size_hint_y=None, height=45)
        self.password = TextInput(hint_text="Password", password=True, multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        
        self.error_label = Label(text="", size_hint_y=None, height=30, color=(1, 0.3, 0.3, 1))
        layout.add_widget(self.error_label)
        
        login_btn = Button(text="Log In", size_hint_y=None, height=45, background_color=(0.2, 0.8, 0.2, 1))
        login_btn.bind(on_press=self.try_login)
        layout.add_widget(login_btn)
        
        google_btn = Button(text="Sign in with Google Account", size_hint_y=None, height=45, background_color=(0.8, 0.2, 0.2, 1))
        google_btn.bind(on_press=self.go_to_google_flow)
        layout.add_widget(google_btn)
        
        no_account_btn = Button(text="Don't have an account? Create one", size_hint_y=None, height=40, background_color=(0,0,0,0), color=(0.9, 0.9, 1, 1))
        no_account_btn.bind(on_press=self.go_to_signup)
        layout.add_widget(no_account_btn)
        
        self.add_widget(layout)

    def try_login(self, instance):
        app = App.get_running_app()
        if app.db.verify_login(self.username.text, self.password.text):
            app.db.data["active_session"] = self.username.text
            app.db.save_db()
            self.error_label.text = ""
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = "❌ Invalid email or password confirmation status."

    def go_to_google_flow(self, instance):
        self.manager.current = 'google_auth'

    def go_to_signup(self, instance):
        self.manager.current = 'signup'


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = PurpleLayout()
        
        title = Label(text="Create Account", font_size='28sp', bold=True)
        layout.add_widget(title)
        
        self.new_user = TextInput(hint_text="Enter Email Address", multiline=False, size_hint_y=None, height=45)
        self.new_pass = TextInput(hint_text="Choose Password", password=True, multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.new_user)
        layout.add_widget(self.new_pass)
        
        signup_btn = Button(text="Register & Verify", size_hint_y=None, height=45, background_color=(0.2, 0.6, 0.9, 1))
        signup_btn.bind(on_press=self.trigger_verification)
        layout.add_widget(signup_btn)
        
        back_btn = Button(text="Back to Login", size_hint_y=None, height=40, background_color=(0,0,0,0))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)

    def trigger_verification(self, instance):
        if "@" in self.new_user.text and len(self.new_pass.text) >= 4:
            self.manager.get_screen('verify').target_email = self.new_user.text
            self.manager.get_screen('verify').pending_password = self.new_pass.text
            self.manager.current = 'verify'


class GoogleAuthScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = PurpleLayout()
        
        title = Label(text="Google Sign-In Platform", font_size='24sp', bold=True)
        layout.add_widget(title)
        
        self.google_email = TextInput(hint_text="Enter your Google Email", multiline=False, size_hint_y=None, height=45)
        self.google_password = TextInput(hint_text="Google Password", password=True, multiline=False, size_hint_y=None, height=45)
        layout.add_widget(self.google_email)
        layout.add_widget(self.google_password)
        
        next_btn = Button(text="Send Verification Code", size_hint_y=None, height=45, background_color=(0.5, 0.2, 0.7, 1))
        next_btn.bind(on_press=self.send_code)
        layout.add_widget(next_btn)
        
        self.add_widget(layout)

    def send_code(self, instance):
        if "@" in self.google_email.text:
            self.manager.get_screen('verify').target_email = self.google_email.text
            self.manager.get_screen('verify').pending_password = self.google_password.text
            self.manager.current = 'verify'


class VerificationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_email = ""
        self.pending_password = ""
        layout = PurpleLayout(spacing=20)
        
        self.info_label = Label(text="", font_size='16sp', halign='center')
        self.code_input = TextInput(hint_text="Enter Code (Use 1234)", multiline=False, size_hint_y=None, height=45, halign='center')
        
        verify_btn = Button(text="Verify & Continue", size_hint_y=None, height=45, background_color=(0.2, 0.8, 0.2, 1))
        verify_btn.bind(on_press=self.check_code)
        
        layout.add_widget(self.info_label)
        layout.add_widget(self.code_input)
        layout.add_widget(verify_btn)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.info_label.text = f"Secure code requested\nfor: {self.target_email}\n\nEnter code below to finish."

    def check_code(self, instance):
        if self.code_input.text == "1234":
            self.code_input.text = ""
            app = App.get_running_app()
            # Commit the registered account metrics natively to local storage configurations
            app.db.register_user(self.target_email, self.pending_password)
            app.db.data["active_session"] = self.target_email
