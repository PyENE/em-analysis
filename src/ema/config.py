# import logging
import os
import seaborn as sns
# logging.basicConfig(level=logging.CRITICAL)
# filename='/home/bolivier/coding-workspace/oculonimbus/ema/ema.log'

PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..' + os.sep + '..' + os.sep)
SHARE_PATH = os.path.join(PROJECT_PATH, 'share')
DATA_PATH = os.path.join(SHARE_PATH, 'data')
PNG_TEXTS_PATH = os.path.join(DATA_PATH, "Materiel")
MODELS_PATH = os.path.join(SHARE_PATH, 'models')
GRAPHICS_PATH = os.path.join(SHARE_PATH, 'graphics')
REPORTS_PATH = os.path.join(SHARE_PATH, 'reports')
SRC_PATH = os.path.join(PROJECT_PATH, 'src')
ANALYSIS_PATH = os.path.join(PROJECT_PATH, 'notebooks')
TEST_PATH = os.path.join(PROJECT_PATH, 'test')
FIXATION_PATH = os.path.join(PROJECT_PATH, '..' + os.sep + 'fixation-word-assignation')
PLOTS_PATH = os.path.join(PROJECT_PATH, '..' + os.sep + 'plots')
FASTTEXT_PATH = os.path.join(PROJECT_PATH, '..', 'fasttext')

COLOR_PALETTE = sns.color_palette('dark', 10)
