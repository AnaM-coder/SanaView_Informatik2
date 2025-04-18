import fsspec, posixpath
import streamlit as st
import pandas as pd
from utils.data_handler import DataHandler

class DataManager:
    def __new__(cls, *args, **kwargs):
        if 'data_manager' in st.session_state:
            return st.session_state.data_manager
        else:
            instance = super(DataManager, cls).__new__(cls)
            st.session_state.data_manager = instance
            return instance

    def __init__(self, fs_protocol='file', fs_root_folder='SanaView2'):
        if hasattr(self, 'fs'):
            return

        self.fs_root_folder = fs_root_folder
        self.fs = self._init_filesystem(fs_protocol)
        self.app_data_reg = {}
        self.user_data_reg = {}

        # Benutzerordner bei Init anlegen (falls User eingeloggt)
        username = st.session_state.get('username')
        if username:
            self._ensure_user_folder_exists(username)

    @staticmethod
    def _init_filesystem(protocol: str):
        if protocol == 'webdav':
            secrets = st.secrets['webdav']
            return fsspec.filesystem(
                'webdav',
                base_url=secrets['base_url'],
                auth=(secrets['username'], secrets['password'])
            )
        elif protocol == 'file':
            return fsspec.filesystem('file')
        else:
            raise ValueError(f"Ungültiges Protokoll: {protocol}")

    def _get_data_handler(self, subfolder: str = None):
        if subfolder is None:
            return DataHandler(self.fs, self.fs_root_folder)
        else:
            return DataHandler(self.fs, posixpath.join(self.fs_root_folder, subfolder))

    def _ensure_user_folder_exists(self, username):
        user_path = posixpath.join(self.fs_root_folder, f"user_data_{username}")
        if not self.fs.exists(user_path):
            self.fs.mkdir(user_path)
            print(f"✅ Benutzerordner erstellt: {user_path}")

    def load_user_data(self, session_state_key, file_name, initial_value=None, **load_args):
        username = st.session_state.get('username')
        if not username:
            st.error("❌ Kein Benutzer eingeloggt!")
            return

        if session_state_key in st.session_state:
            return

        user_folder = f"user_data_{username}"
        dh = self._get_data_handler(user_folder)
        data = dh.load(file_name, initial_value, **load_args)
        st.session_state[session_state_key] = data
        self.user_data_reg[session_state_key] = dh.join(user_folder, file_name)

    def save_data(self, session_state_key):
        if session_state_key not in st.session_state:
            raise ValueError(f"Session-Key '{session_state_key}' nicht gefunden")

        path = self.data_reg.get(session_state_key)
        if not path:
            # Wenn noch nicht registriert, speichere unter dem Benutzerpfad
            username = st.session_state.get('username', 'default')
            user_folder = f"user_data_{username}"
            path = posixpath.join(user_folder, f"{session_state_key}.csv")
            self.user_data_reg[session_state_key] = path

        dh = self._get_data_handler()
        dh.save(path, st.session_state[session_state_key])

    def save_all_data(self):
        for key in self.data_reg:
            if key in st.session_state:
                self.save_data(key)

    def append_record(self, session_state_key, record_dict):
        if session_state_key not in st.session_state:
            st.session_state[session_state_key] = pd.DataFrame(columns=record_dict.keys())

        current = st.session_state[session_state_key]
        new = pd.DataFrame([record_dict])
        updated = pd.concat([current, new], ignore_index=True)

        st.session_state[session_state_key] = updated
        self.save_data(session_state_key)

    @property
    def data_reg(self):
        return {**self.app_data_reg, **self.user_data_reg}
