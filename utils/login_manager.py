import secrets
import streamlit as st
import streamlit_authenticator as stauth
from utils.data_manager import DataManager

class LoginManager:
    """
    Singleton-Klasse, die Authentifizierung und Anwendungszustand verwaltet.
    """

    def __new__(cls, *args, **kwargs):
        if 'login_manager' in st.session_state:
            return st.session_state.login_manager
        else:
            instance = super(LoginManager, cls).__new__(cls)
            st.session_state.login_manager = instance
            return instance

    def __init__(self, data_manager: DataManager = None,
                 auth_credentials_file: str = 'credentials.yaml',
                 auth_cookie_name: str = 'bmld_inf2_streamlit_app'):
        if hasattr(self, 'authenticator'):
            return  # Schon initialisiert

        if data_manager is None:
            return

        self.data_manager = data_manager
        self.auth_credentials_file = auth_credentials_file
        self.auth_cookie_name = auth_cookie_name
        self.auth_cookie_key = secrets.token_urlsafe(32)
        self.auth_credentials = self._load_auth_credentials()

        self.authenticator = stauth.Authenticate(
            self.auth_credentials,
            self.auth_cookie_name,
            self.auth_cookie_key
        )

    def _load_auth_credentials(self):
        dh = self.data_manager._get_data_handler()
        return dh.load(self.auth_credentials_file, initial_value={"usernames": {}})

    def _save_auth_credentials(self):
        dh = self.data_manager._get_data_handler()
        dh.save(self.auth_credentials_file, self.auth_credentials)

    def login_register(self, login_title='Login', register_title='Registrieren'):
        if st.session_state.get("authentication_status") is True:
            return  # Kein Logout-Button hier mehr
        else:
            login_tab, register_tab = st.tabs((login_title, register_title))
            with login_tab:
                self.login(stop=False)
            with register_tab:
                self.register()

    def login(self, stop=True):
        if st.session_state.get("authentication_status") is True:
            return
        self.authenticator.login()
        if "authentication_status" in st.session_state:
            if st.session_state["authentication_status"] is False:
                st.error("Benutzername oder Passwort ist falsch.")
            elif st.session_state["authentication_status"] is None:
                st.warning("Bitte geben Sie Ihren Benutzernamen und Ihr Passwort ein.")
        else:
            st.warning("Bitte geben Sie Ihren Benutzernamen und Ihr Passwort ein.")
        if stop:
            st.stop()

    def register(self, stop=True):
        if st.session_state.get("authentication_status") is True:
            return  # Kein Logout-Button mehr hier
        else:
            st.info("""
            Passwortanforderungen: 8–20 Zeichen, Gross-/Kleinbuchstaben, Zahl und ein Sonderzeichen (@$!%*?&).
            """)
            res = self.authenticator.register_user()
            if res[1] is not None:
                st.success(f"Benutzer {res[1]} erfolgreich registriert.")
                try:
                    self._save_auth_credentials()
                    self.auth_credentials = self._load_auth_credentials()
                    self.authenticator = stauth.Authenticate(
                        self.auth_credentials,
                        self.auth_cookie_name,
                        self.auth_cookie_key
                    )
                    st.info("Bitte loggen Sie sich jetzt mit Ihrem neuen Benutzer ein.")
                    st.stop()
                except Exception as e:
                    st.error(f"Fehler beim Speichern: {e}")
        if stop:
            st.stop()

    def go_to_login(self, login_page_py_file):
        if not st.session_state.get("authentication_status"):
            st.warning("⚠️ Sie müssen sich anmelden, um fortzufahren.")
            st.switch_page(login_page_py_file)

    def logout(self):
        """
        Führt Logout durch, entfernt alle relevanten Daten aus st.session_state.
        """
        if hasattr(self, 'authenticator'):
            self.authenticator.logout("Logout", "sidebar")  # Optional, aber wenn du es brauchst

        for key in list(st.session_state.keys()):
            if key not in ["data_manager", "login_manager"]:
                del st.session_state[key]

        st.success("✅ Erfolgreich ausgeloggt.")
        st.experimental_rerun()