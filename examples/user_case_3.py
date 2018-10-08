"""Testing a user case."""
from ema.eye_movement_data import EyeMovementData
from ema.model import Model
from ema.html_report import Htmlreport

# import data
data = EyeMovementData()

# model with auto-initilization (non random)
# model = Model(data, k=5, dynamic_model=True, dynamic_model_frequency=2)
model = Model(data, k=5)

# iterate EM for convergence
model.iterate_em(50)

html_report = Htmlreport(model, number_of_text_restorations_to_display=0)
html_report.make_html(open_in_web_browser=True)
