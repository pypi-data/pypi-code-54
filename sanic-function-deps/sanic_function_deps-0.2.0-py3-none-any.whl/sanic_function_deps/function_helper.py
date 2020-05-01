import sanic
import inspect
import logging
logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

default_config = {
    'missingParamMessage': {
        'query': 'Missing \'{}\' query parameter',
        'header': 'Missing \'{}\' header'
    }
}
prefix = 'sanic-function-deps'


def _coerce(param_name, function_arg, value):
    (name, p) = function_arg
    if p.annotation != inspect._empty:
        try:
            return p.annotation(value)
        except ValueError:
            raise ValueError(
                f'{param_name} validation failed. {str(p.annotation)} needed.'
            )
    else:
        return value


def _get_from_query(
    request, param, config, function_arg, required=False
):
    if type(param) == str:
        _param = request.args.get(param)
        missing_param_message = config['missingParamMessage']['query']
        missing_param_message = missing_param_message.format(param)
    else:
        _param = request.args.get(param['name'])
        global_msg = config['missingParamMessage']['query']
        local_msg = param.get('missingParamMessage')
        missing_param_message = _get_message(global_msg, local_msg)
        missing_param_message = missing_param_message.format(param['name'])
    if not _param and required:
        raise ValueError(missing_param_message)

    return _coerce(
        param if type(param) == str else param['name'],
        function_arg,
        _param
    )


def _get_from_header(
        request, param, config, function_arg, required=False
):
    header_value = request.headers.get(param['name'])
    global_msg = config['missingParamMessage']['header']
    local_msg = param.get('missingParamMessage')
    missing_param_message = _get_message(global_msg, local_msg)
    if not header_value and required:
        raise ValueError(missing_param_message.format(param['name']))

    return _coerce(param['name'], function_arg, header_value)


def _pre_validation(params):
    if type(params) != list:
        raise ValueError(f'{prefix}: helper params must be list')

    for idx, param in enumerate(params):
        if type(param) == dict:
            txt = '{}: Missing \'{}\' in helper params, index: {}'
            required_params = ['name', 'source']

            for _param in required_params:
                if _param not in param:
                    raise ValueError(txt.format(prefix, _param, idx))
            if param['source'] not in ['query', 'header']:
                raise ValueError(f'{prefix}: source param not recognized')


def _get_message(global_message, local_message):
    if local_message:
        return local_message
    return global_message


def _process_args(request, consumer_function, params, config):
    values = []
    function_argument_map = list(inspect.signature(
        consumer_function
    ).parameters.items())
    try:
        for idx, param in enumerate(params):
            if type(param) == str:
                values.append(
                    _get_from_query(
                         request,
                         param,
                         config,
                         function_argument_map[idx],
                         required=True
                    )
                 )
            elif type(param) == dict:
                source = param['source']
                if source == 'query':
                    values.append(
                        _get_from_query(
                            request,
                            param,
                            config,
                            function_argument_map[idx],
                            required=param.get('required', True)
                        )
                    )
                elif source == 'header':
                    values.append(
                        _get_from_header(
                            request,
                            param,
                            config,
                            function_argument_map[idx],
                            required=param.get('required', True)
                        )
                    )
    except ValueError as e:
        return {'msg': str(e)}

    return values


def _same_sized_param_and_function_args(consumer_function, params):
    function_arguments = list(inspect.signature(
        consumer_function
    ).parameters.items())
    if len(params) != len(function_arguments):
        pluralized_param = "param" if len(params) == 1 else "params"
        pluralized_arg = "argument" if len(function_arguments) == 1 else "arguments"

        msg = f"{prefix}: {len(params)} {pluralized_param} supplied but {len(function_arguments)} {pluralized_arg} in route function"
        raise ValueError(msg)


def create_function_deps(extra_config=None):
    def function_deps(params):
        config = extra_config if extra_config else default_config
        logger.debug(f'function deps {params}')
        _pre_validation(params)

        def wrap(consumer_function):
            # func is the app/route function of the actual user, not sanic.
            _same_sized_param_and_function_args(consumer_function, params)
            logger.debug(f'Outer consumer {consumer_function}')

            async def wrapped(request):
                # Now sanic has called our function. We will begin
                # processing here and vet our params
                logger.debug(f'Outer request {request}')
                args = _process_args(request, consumer_function, params, config)
                logger.debug(f'Outer processed: {args}, {type(args)}')
                if type(args) == dict:
                    # It's an error
                    logger.debug(f'Error! {args}')
                    return sanic.response.json(args)
                else:
                    logger.debug(f'Proccessed args {args}')
                    return await consumer_function(*args)

            return wrapped

        return wrap
    return function_deps
