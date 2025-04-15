import torch
import os
from torch.utils.data import Dataset
from typing import Any
from pathlib import Path
import pickle

class MotoricaDataset(Dataset):
    def __init__(
            self,
            data_path:str,
            backup_path: str,
            train:bool,
            feature_type: str = 'jukebox',
            normalizer:Any = None,
            data_len = -1,
            include_contacts: bool = False,
            force_reload: bool = False,
    ):
        self.data_path = data_path
        self.raw_fps = 120
        self.data_fps = 30
        self.data_stride = self.raw_fps // self.data_fps
        self.feature_type = feature_type

        self.normalizer = normalizer
        self.data_len = data_len
        pickle_name = "processed_train_data.pkl" if train else "processed_test_data.pkl"
        backup_path = Path(backup_path)
        backup_path.mkdir(parents=True, exist_ok=True)

         # load raw data
        if not force_reload and pickle_name in os.listdir(backup_path):
            print("Using cached dataset...")
            with open(backup_path/ pickle_name, "rb") as f:
                data = pickle.load(f)
        else:
            print("Loading dataset...")
            data = self.load_morotica()  # Call this last
            with open(backup_path/ pickle_name, "wb") as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


    def load_morotica(self):

