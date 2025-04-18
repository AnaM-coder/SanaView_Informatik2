import fsspec, posixpath
import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler

class DataManager:
    """
    A singleton class for managing application data persistence and user-specific storage.
    """

    def __new__(cls, *args, **kwargs):
        if 'data_manager' in st.session_state:
            return st.session_state.data_manager
        else:
            instance = super(DataManager, cls).__new__(cls)
            st.session_state.data_manager = instance
            return instance

    def __init__(self, fs_protocol='file', fs_root_folder='app_data'):
        if hasattr(self, 'fs'):  # check if instance is already initialized
            return

        self.fs_root_folder = fs_root_folder
        self.fs = self._init_filesystem(fs_protocol)
        self.app_data_reg = {}
        self.user_data_reg = {}

    @staticmethod
    def _init_filesystem(protocol: str):
        if protocol == 'webdav':
            secrets = st.secrets['webdav']
            return fsspec.filesystem('webdav',
                                     base_url=secrets['base_url'],
                                     auth=(secrets['username'], secrets['password']))
        elif protocol == 'file':
            return fsspec.filesystem('file')
        else:
            raise ValueError(f"AppManager: Invalid filesystem protocol: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        if subfolder is None:
            return DataHandler(self.fs, self.fs_root_folder)
        else:
            return DataHandler(self.fs, posixpath.join(self.fs_root_folder, subfolder))

    def load_app_data(self, session_state_key, file_name, initial_value=None, **load_args):
        if session_state_key in st.session_state:
            return

        dh = self._get_data_handler()
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.app_data_reg[session_state_key] = file_name

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        username = st.session_state.get('username', None)
        if username is None:
            for key in self.user_data_reg:
                st.session_state.pop(key, None)
            self.user_data_reg = {}
            st.error(f"DataManager: No user logged in, cannot load file `{file_name}` into session state with key `{session_state_key}`")
            return
        elif session_state_key in st.session_state:
            return

        user_data_folder = f"user_data_dom/{username}"

        # 📁 Ordner automatisch erstellen, falls er nicht existiert
        user_folder_path = posixpath.join(self.fs_root_folder, user_data_folder)
        if not self.fs.exists(user_folder_path):
            self.fs.makedirs(user_folder_path)
            st.info(f"📁 Benutzerordner wurde erstellt: {user_folder_path}")

        dh = self._get_data_handler(user_data_folder)
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.user_data_reg[session_state_key] = dh.join(user_data_folder, file_name)

    @property
    def data_reg(self):
        return {**self.app_data_reg, **self.user_data_reg}

    def save_data(self, session_state_key):
        """
        Speichert einen Eintrag aus dem Session-State dauerhaft.
        """
        if session_state_key not in self.data_reg:
            self.app_data_reg[session_state_key] = f"{session_state_key}.csv"

        if session_state_key not in st.session_state:
            raise ValueError(f"DataManager: Key {session_state_key} not found in session state")

        dh = self._get_data_handler()
        dh.save(self.data_reg[session_state_key], st.session_state[session_state_key])

    def save_all_data(self):
        """
        Speichert alle registrierten Daten aus dem Session-State dauerhaft.
        """
        keys = [key for key in self.data_reg.keys() if key in st.session_state]
        for key in keys:
            self.save_data(key)

    def append_record(self, session_state_key, record_dict):
        """
        Fügt einen neuen Eintrag zum Session-State hinzu und speichert ihn.
        """
        if session_state_key not in st.session_state:
            st.session_state[session_state_key] = pd.DataFrame(columns=["datum_zeit", "blutzuckerwert", "zeitpunkt"])
            st.warning(f"Session state key '{session_state_key}' wurde initialisiert.")

        if session_state_key not in self.data_reg:
            self.app_data_reg[session_state_key] = f"{session_state_key}.csv"

        data_value = st.session_state[session_state_key]

        if not isinstance(record_dict, dict):
            raise ValueError(f"DataManager: The record_dict must be a dictionary")

        if isinstance(data_value, pd.DataFrame):
            data_value = pd.concat([data_value, pd.DataFrame([record_dict])], ignore_index=True)
        elif isinstance(data_value, list):
            data_value.append(record_dict)
        else:
            raise ValueError(f"DataManager: The session state value for key '{session_state_key}' must be a DataFrame or a list")

        st.session_state[session_state_key] = data_value
        self.save_data(session_state_key)
