from config import *
from eye_movement_data import *
from html_report import *
from initial_probabilities import *
from model import *
from model_parameters import *
from observation_distribution import *
from occupancy_distribution import *
from output_process import *
from png_plot import *
from transition_graph_display import *
from transition_probabilities import *
from openalea.deploy.shared_data import get_shared_data_path
from os.path import join as pj


def get_shared_data(file):
    import openalea.stat_tool
    shared_data_path = get_shared_data_path(openalea.ema.__path__)
    return pj(shared_data_path, file)
