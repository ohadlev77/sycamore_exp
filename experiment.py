"""
Experiment object class.
"""
from typing import List, Dict

class Experiment:
    """
    A data structure for experiments to be run by the `RandomSamples` class.
    """

    def __init__(self, combinations: Dict[int, List[int]]) -> None:
        """
        Args:
            combinations (Dict[int, List[int]]): a dictionary with circuit IDs as keys and
            lists of noise models' IDs as values for each circuit ID.
        """

        self.combinations = combinations

        # Storing unique noise models' IDS into the set `self.noise_models`
        self.document_noise_models()
    
    def __repr__(self) -> str:
        return f"Experiment({self.combinations})"

    def document_noise_models(self) -> None:
        """
        Stores unique noise models' IDS into the set `self.noise_models`.
        """
        
        self.noise_models = set()

        for noise_model_ids in self.combinations.values():
            self.noise_models.update(noise_model_ids)

    def add_combinations(self, combinations: Dict[int, List[int]]) -> None:
        """
        Adds more combinations of circuits and noise models to the experiment.
        """

        # Adding combinations
        self.combinations.update(combinations)

        # Updating `self.noise_models`
        self.document_noise_models()