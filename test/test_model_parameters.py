"""Testing class ObservationDistribution."""
from ema.eye_movement_data import EyeMovementData
from ema.model import Model
from ema.__init__ import TEST_PATH
import os
import pytest


@pytest.fixture
def model():
    return Model(EyeMovementData(), init_hsmc_file=os.path.join(TEST_PATH, 'input_model.hsmc'))


def test_swap_hidden_state_order(model):
    # cant do stg clean by deepcopying and testing using assert because
    # deepcopy requires pickling all the python C++ wrappers
    parameters = model.parameters
    print parameters
    parameters.swap_hidden_state_order(0, 2, 3)
    print parameters
    print model.parameters._model.hsmm.display()

test_swap_hidden_state_order(model())
