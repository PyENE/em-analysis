"""Testing a user case."""
from ema.eye_movement_data import EyeMovementData
from ema.indicator import Indicator
from ema.model import Model
import numpy as np


# import data
data = EyeMovementData()

# model with auto-initilization (non random)
model = Model(data, k=5)

# iterate EM for convergence
model.iterate_em(1000)

# plot indicators
fdur = Indicator(model, 'FDUR')
fdur.boxplot()

sacamp = Indicator(model, 'SACAMP')
sacamp.boxplot()

winc = Indicator(model, 'WINC')
winc.boxplot()

cosinst = Indicator(model, 'COSINST')
cosinst.boxplot()
