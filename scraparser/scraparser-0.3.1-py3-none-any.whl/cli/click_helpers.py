import inspect
import sys
import os
from functools import wraps

import click
import pandas as pd


def do_each(outer_keyword="inputs", inner_keyword="input", keep_outer_keyword=False):
    """
    Consumes the keyword argument named as the `outer_keyword`,
    loop through them to invoke the inner function with the string
    remapped to the `inner_keyword` name.
    """
    def decorator(fn):

        @click.argument(outer_keyword, nargs=-1)
        @click.pass_context
        @wraps(fn)
        def wrapper(ctx, *args, **kwargs):
            if outer_keyword not in kwargs:
                # TODO: throw some exception
                sys.exit(1)
            inputs = kwargs[outer_keyword]

            if len(inputs) == 0:
                inputs = sys.stdin

            results = [] # TODO: Rewrite as iterator
            for input in inputs:
                input = input.rstrip("\r\n")
                innerKwargs = kwargs.copy()
                innerKwargs[inner_keyword] = input
                if not keep_outer_keyword and inner_keyword != outer_keyword:
                    del innerKwargs[outer_keyword]
                results.append(ctx.invoke(fn, *args, **innerKwargs))
            return results

        return wrapper
    return decorator


def csv_to_dataframe(outer_keyword="filename", inner_keyword="df", keep_outer_keyword=False):
    """
    Consumes the keyword argument named as the `outer_keyword` as if
    it is filename, open the file, convert to panda.Dataframe, then
    pass the dataframe to the inner function as the keyword argument
    named by `inner_keyword`.
    """
    def decorator(fn):

        @click.pass_context
        @wraps(fn)
        def wrapper(ctx, *args, **kwargs):

            if outer_keyword not in kwargs:
                # TODO: throw some exception
                sys.exit(1)
            filename = kwargs[outer_keyword]

            innerKwargs = kwargs.copy()
            innerKwargs[inner_keyword] = pd.read_csv(filename)

            if not keep_outer_keyword and inner_keyword != outer_keyword:
                del innerKwargs[outer_keyword]

            return ctx.invoke(fn, *args, **innerKwargs)
        return wrapper
    return decorator


def dataframe_to_csv(input_keyword="filename", default_filename="output.csv", force_in_place=False, keep_input_keyword=False):
    """
    Consumes the keyword argument named, as specified by the `input_keyword`
    then, with reference to `in_place` and `default_filename`, output the dataframe
    to the default filename or the input filename.

    Also check the `print_filename` flag to see if it should print the filename to STDOUT.
    """
    def decorator(fn):

        @click.option('--in-place', default=False, is_flag=True, help="Modify the file in-place.")
        @click.pass_context
        @wraps(fn)
        def wrapper(ctx, in_place=False, *args, **kwargs):

            if input_keyword not in kwargs:
                # TODO: throw some exception
                sys.exit(1)
            filename = kwargs[input_keyword]

            # Pass everything to the inner function
            innerKwargs = kwargs.copy()
            if not keep_input_keyword:
                del innerKwargs[input_keyword]
            df = ctx.invoke(fn, *args, **innerKwargs)

            # Save output of inner function (supposed DataFrame)
            # to the output csv file.
            if in_place or force_in_place:
                filename_basename = os.path.basename(filename)
                filename_basic, filename_ext = os.path.splitext(filename_basename)
                if filename_ext.lower() != ".csv":
                    # rename the file to csv, if needed.
                    filename = os.path.join(
                        os.path.dirname(os.path.abspath(filename)),
                        filename_basic + ".csv",
                    )
            else:
                filename = default_filename

            df.to_csv(filename, index=False)
            return filename

        return wrapper
    return decorator


def post_hook(
    callback=None,
    flag_name="--run-post-hook",
    flag_keyword="run_post_hook",
    keep_flag_keyword=False,
    **decorator_kwargs,
):
    """
    Run the wrapped function anyway. If the specified `flag_name` specified is True,
    then run `callback(ctx, *args, **kwargs)` and discard its output. Return the
    original wrapped function output.

    The `flag_keyword` is for mapping the click option to keyword variables.
    Default mapped variable name is "run_post_hok". You may override it when needed.
    """
    def decorator(fn):

        @click.option(flag_name, flag_keyword, is_flag=True, **decorator_kwargs)
        @click.pass_context
        @wraps(fn)
        def wrapper(ctx, *args, **kwargs):
            if callback is None:
                # TODO: throw some exception
                sys.exit(1)
            if flag_keyword not in kwargs:
                # TODO: throw some exception
                sys.exit(1)

            should_print = kwargs[flag_keyword]
            if not keep_flag_keyword:
                del kwargs[flag_keyword]

            # Pass everything to the inner function
            output = ctx.invoke(fn, *args, **kwargs)

            # If flagged to print output, print it.
            if should_print:
                callback(ctx, *args, **kwargs)
            return output

        return wrapper
    return decorator


def print_output(flag_name="--print", flag_keyword="print", keep_flag_keyword=False, **decorator_kwargs):
    """
    Run the wrapped function and print any output if the specified `flag_name`
    is specified in the CLI as True (or not set and default True).

    The `flag_keyword` is for mapping the click option to keyword variables.
    Default mapped variable name is "print". You may override it when needed.
    """
    def decorator(fn):

        @click.option(flag_name, flag_keyword, is_flag=True, **decorator_kwargs)
        @click.pass_context
        @wraps(fn)
        def wrapper(ctx, *args, **kwargs):
            if flag_keyword not in kwargs:
                # TODO: throw some exception
                sys.exit(1)
            to_print = kwargs[flag_keyword]

            if not keep_flag_keyword:
                del kwargs[flag_keyword]

            # Pass everything to the inner function
            output = ctx.invoke(fn, *args, **kwargs)

            # If flagged to print output, print it.
            if to_print:
                print(output)
            return output

        return wrapper
    return decorator
