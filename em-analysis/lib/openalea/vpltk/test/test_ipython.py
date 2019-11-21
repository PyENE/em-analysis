from openalea.vpltk.check.ipython import has_ipython, has_ipython_config
from openalea.vpltk.check.ipython_deps import has_pygments, has_zmq

def test_has_ipython():
	assert has_ipython()
	
def test_has_pygments():
	assert has_pygments()
	
def test_has_zmq():
	assert has_zmq()
	
def test_has_ipython_config():
	assert has_ipython_config()
