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
        if hasattr(self, 'fs'):  # bereits initialisiert?
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
            raise ValueError(f"Ungültiges Protokoll: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        folder = self.fs_root_folder if subfolder is None else posixpath.join(self.fs_root_folder, subfolder)
        return DataHandler(self.fs, folder)

    def load_app_data(self, session_state_key, file_name, initial_value=None, **load_args):
        if session_state_key in st.session_state:
            return
        
        dh = self._get_data_handler()
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.app_data_reg[session_state_key] = file_name

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        username = st.session_state.get('username')
        if not username:
            for key in self.user_data_reg:
                st.session_state.pop(key, None)
            self.user_data_reg = {}
            st.error(f"Kein Benutzer eingeloggt – kann `{file_name}` nicht laden.")
            return
        elif session_state_key in st.session_state:
            return

        user_folder = f"user_data_dom/{username}"
        dh = self._get_data_handler(user_folder)
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.user_data_reg[session_state_key] = dh.join(user_folder, file_name)

    @property
    def data_reg(self):
        return {**self.app_data_reg, **self.user_data_reg}

    def save_data(self, session_state_key):
        if session_state_key not in self.data_reg:
            self.app_data_reg[session_state_key] = f"{session_state_key}.csv"

        if session_state_key not in st.session_state:
            raise ValueError(f"Key {session_state_key} nicht im Session-State gefunden")

        # Passenden DataHandler wählen
        target_path = self.data_reg[session_state_key]
        is_user_data = session_state_key in self.user_data_reg

        handler_folder = (
            posixpath.dirname(target_path) if is_user_data else None
        )

        dh = self._get_data_handler(handler_folder)
        dh.save(posixpath.basename(target_path), st.session_state[session_state_key])

    def save_all_data(self):
        for key in [k for k in self.data_reg if k in st.session_state]:
            self.save_data(key)

    def append_record(self, session_state_key, record_dict):
        if session_state_key not in st.session_state:
            st.session_state[session_state_key] = pd.DataFrame(columns=record_dict.keys())

        # === Benutzerordner sicherstellen ===
        if session_state_key not in self.data_reg:
            username = st.session_state.get("username")
            file_name = f"{session_state_key}.csv"
            if username:
                user_folder = f"user_data_dom/{username}"
                full_path = posixpath.join(self.fs_root_folder, user_folder)
                if not self.fs.exists(full_path):
                    self.fs.makedirs(full_path)
                self.user_data_reg[session_state_key] = posixpath.join(user_folder, file_name)
            else:
                self.app_data_reg[session_state_key] = file_name

        # === Hinzufügen zum DataFrame
        current_value = st.session_state[session_state_key]

        if isinstance(current_value, pd.DataFrame):
            new_df = pd.DataFrame([record_dict])
            current_value = pd.concat([current_value, new_df], ignore_index=True)
        elif isinstance(current_value, list):
            current_value.append(record_dict)
        else:
            raise ValueError("Nur DataFrame oder Liste erlaubt.")

        st.session_state[session_state_key] = current_value
        self.save_data(session_state_key)
