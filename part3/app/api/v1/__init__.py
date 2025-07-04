from .auth import api as auth_ns
api.add_namespace(auth_ns, path='/auth')
