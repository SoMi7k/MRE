from dotenv import load_dotenv, find_dotenv
import os

class API_keys:
    def __init__(self, env_var_name: str|None):
        """Načte .env a uloží klíč z proměnné prostředí."""
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        if env_var_name:
            self.__api_key = os.getenv(env_var_name)
        else:
            self.__api_key = None

    def get_api_key(self) -> str | None:
        """Vrátí aktuální uložený API klíč."""
        return self.__api_key

    def set_api_key(self, key: str):
        """Ruční nastavení klíče (přepíše hodnotu z env)."""
        self.__api_key = key


