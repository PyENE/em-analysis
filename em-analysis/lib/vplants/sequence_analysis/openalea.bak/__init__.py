
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

# Local setup for openalea subversion
try:
    from __init_path__ import set_path
    set_path()
except:
    pass

