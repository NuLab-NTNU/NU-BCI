import numpy as np
import threading
import time
import os
import logging

"""
    Contains the class Classifier (should maybe be renamed).

    Last edit: 15th of june 2022

    To do:
        - Load models
        - Assert that the models loaded are compatible with config (nchannels x nsamples etc)
        - More comprehensive error handling

    Author: Vegard Kjeka Broen (NTNU)
"""


class Classifier:
    def __init__(
        self,
        _n_channels,
        _sample_rate,
        _time_per_trial,
        _preprocessing_fname,
        _classifier_fname,
        _regressor_fname,
    ) -> None:
        # eeg data array
        self.n_channels = _n_channels
        self.sample_rate = _sample_rate
        self.time_per_trial = _time_per_trial  # time in seconds per trial
        self.n_samples = self.time_per_trial * self.sample_rate
        self.eeg = np.zeros(
            (self.n_channels, self.n_samples)
        )  # np.array holding eeg data for one trial

        # Filenames for models
        self.preprocessing_fname = _preprocessing_fname
        self.classifier_fname = _classifier_fname
        self.regressor_fname = _regressor_fname

        # Events
        self.trial_data_ready = threading.Event()
        self.trial_processed = threading.Event()

        # Flags
        self.stop_flag = False

        # Results
        self.y_prob = []
        self.y = []
        self.t = []
        self.discard = []

        # Data for operator
        self.feedback_msg = None

        # File stuff
        self.folder_path = "data/" + str(np.random.randint(0, 9999))
        os.mkdir(self.folder_path)

    def load_models(self):
        """
        In the future this should load models for preprocessing, feature extraction, classification and regression
        """
        time.sleep(0.5)

    def wait_for_data(self):
        logging.info("classifier: waiting for trial_data_ready")
        self.trial_data_ready.wait()
        logging.info("classifier: clearing trial_data_ready")
        self.trial_data_ready.clear()

    def process(self):
        # Placeholder for processing
        time.sleep(0.5)

        # Preprocessing
        discard = 1 if np.random.randint(0, 20) < 1 else 0

        # Classification
        y_prob = np.random.randint(0, 101) / 100.0
        y = 1 if y_prob >= 0.5 else 0

        # Regression
        t = -np.random.randint(400, 1000)

        self.y_prob.append(y_prob)
        self.y.append(y)
        self.t.append(t)
        self.discard.append(discard)

    def create_feedback_msg(self):
        self.feedback_msg = f"y = {self.y[-1]}, y_prob = {round(self.y_prob[-1], 2)}, t = {self.t[-1]}, discard = {self.discard[-1]}"
        logging.info("classifier: setting trial_processed")
        self.trial_processed.set()

    def dump_data(self):
        trial_number = len(self.y)
        path = self.folder_path + f"/trial{trial_number}.npy"
        np.save(path, self.eeg)

        path2 = self.folder_path + f"/trial{trial_number}results.npy"
        results = np.array([self.y[-1], self.y_prob[-1], self.t[-1], self.discard[-1]])
        np.save(path2, results)

    def is_ok(self):
        return True

    def main_loop(self):
        while self.is_ok():
            self.wait_for_data()

            self.process()

            self.create_feedback_msg()

            self.dump_data()
