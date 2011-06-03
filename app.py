import re
import sys

import bottle
from bottle import route, request, HTTPResponse, SimpleTemplate, view, static_file

bottle.debug(True)

SimpleTemplate.defaults['url'] = bottle.url

def makeJSONP(callback, data):
    # wraps the data in callback to prep it for JSONP response
    response_data = callback
    response_data += '('
    response_data += bottle.json_dumps(data)
    response_data += ');'
    return response_data

def auto_jsonp(f):
    # Automatically convert JSON response to JSONP
    def new(*arg, **kw):
        callback = request.GET.get('callback')
        result_data = f(*arg, **kw)
        if callback and isinstance(result_data, dict):
            # We only do JSONP for dicts
            response.headers['Content-type'] = 'text/javascript'
            return makeJSONP(callback, result_data)
        # otherwise, we just return as usual
        return result_data
    
    return new

def load_mod(mod_path, from_mod=None):
    mod_comps = mod_path.split('.')
    mod = mod_comps.pop(0)
    subpath = '.'.join(mod_comps)
    if from_mod:
        try:
            # Load a submodule
            module = getattr(from_mod, mod)
        except AttributeError:
            # The module doesn't contain such submodule
            raise ImportError('%s.%s', (from_mod, mod))
    else:
        # We import the full module path here
        module = __import__(mod_path)
    if subpath:
        # We still have work to do
        return load_mod(subpath, module)
    # All done, return the module
    return module

@route('/')
@view('index')
def index():
    return dict()

@route('/rpc/:mod#[a-zA-Z_][\w.-]*#/:func#[a-zA-Z_][\w-]*#',
       method=['GET', 'POST'])
@auto_jsonp
def rpc(mod, func):
    try:
        module = load_mod(mod)
    except ImportError:
        raise HTTPResponse('Module %s does not exist.' % mod, 400)

    function = getattr(module, func)

    if not all([function, callable(function)]):
        raise HTTPResponse('Function %s is not callable.' % func, 400)

    if request.params.get('_args[]'):
        args = request.params.get('_args[]')
        if not isinstance(args, list):
            args = [args]
        result = function(*args)
    else:
        result = function(**request.params)

    if isinstance(result, dict):
        return result
    else:
        return dict(r=result)

@route('/static/:path#[\w_./-]+#',
       name='static')
def static(path):
    return static_file(path, root='static')

if __name__ == '__main__':
    bottle.run(port=9000)
