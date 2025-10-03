"""Code smell detectors package."""

from .long_method import LongMethodDetector
from .god_class import GodClassDetector
from .duplicated_code import DuplicatedCodeDetector
from .large_parameter_list import LargeParameterListDetector
from .magic_numbers import MagicNumbersDetector
from .feature_envy import FeatureEnvyDetector

__all__ = [
    'LongMethodDetector',
    'GodClassDetector',
    'DuplicatedCodeDetector',
    'LargeParameterListDetector',
    'MagicNumbersDetector',
    'FeatureEnvyDetector'
]

