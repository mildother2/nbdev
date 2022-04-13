# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/12_linkify.ipynb.

# %% auto 0
__all__ = ['is_lib_module', 'get_link']

# %% ../nbs/12_linkify.ipynb 2
import importlib, re, inspect
from fastcore.test import test_eq
from fastcore.utils import Path
from .read import get_config

# %% ../nbs/12_linkify.ipynb 4
def is_lib_module(name):
    "Test if `name` is a library module."
    if name.startswith('_'): return False
    try:return importlib.import_module(f'{get_config().lib_name}.{name}')
    except: return None

# %% ../nbs/12_linkify.ipynb 6
_re_nb_ln = re.compile(r'^# %% (\S+)')
_re_nb_mod = re.compile(r'^# AUTOGENERATED! DO NOT EDIT! File to edit: (\S+).', flags=re.MULTILINE)

def _get_baseurl() -> str:
    baseurl = get_config()['doc_host']
    return baseurl if baseurl.endswith('/') else baseurl + '/'

def _get_path(s:str, rp:re.Pattern) -> str:
    r = rp.search(s)
    if r: return Path(r.group(1)).with_suffix('.html').name
    else: return None

# %% ../nbs/12_linkify.ipynb 8
def get_link(name:str) -> str:
    "Get a link to the docs from a name."
    baseurl = get_config()['doc_host']
    if '.' in name: *m,o=name.split('.')
    else: m,o=[name],None
    mod = is_lib_module('.'.join(m))
    if mod:
        mod_src = inspect.getsource(mod)
        path = _get_path(mod_src, _re_nb_mod)
        if o:
            obj = getattr(mod, o, None)
            if not obj: return None
            if obj:
                lnum = inspect.getsourcelines(obj)[1] - 2
                path = _get_path(mod_src.splitlines()[lnum], _re_nb_ln) + f'#{o}'
        return f'{_get_baseurl()}{path}'
    else: return None
        
