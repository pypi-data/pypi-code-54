from jinja2 import Template
import os
import json
from wickedhot.one_hot_encode import unknown_level_value


def get_templates_text():
    template_dir = os.path.realpath(os.path.dirname(__file__) + '/templates')
    template_files = {'alpaca_index': 'alpaca_index.html',
                      'alpaca_form': 'alpaca_form.html',
                      'alpaca_header': 'alpaca_header.html',
                      'alpaca_example_data': 'alpaca_example.json'}

    paths = {key: "%s/%s" % (template_dir, file) for key, file in template_files.items()}
    templates = {key: open(filename, 'r').read() for key, filename in paths.items()}
    return templates


def generate_alpaca_form(form_data, templates):
    alpaca_json_data = json.dumps(form_data, indent=2)
    template = Template(templates['alpaca_form'])
    return template.render(alpaca_json_data=alpaca_json_data)


def generate_alpaca_index(form_data=None, index_file=None):
    templates = get_templates_text()
    if form_data is None:
        templates_text = templates['alpaca_example_data']
        form_data = json.loads(templates_text)

    form_div = generate_alpaca_form(form_data, templates)

    alpaca_header = templates['alpaca_header']
    if index_file is None:
        index_file = 'alpaca_index'

    index_template = Template(templates[index_file])

    index_html = index_template.render(form_div=form_div, alpaca_header=alpaca_header)

    return index_html


def encoder_package_to_schema(encoder_package):

    properties = {}
    stats = encoder_package['numeric_stats']
    for field in encoder_package['numeric_cols']:
        properties[field] = {
                "type": "number",
                "title": field.capitalize(),
                "required": True
        }

        if stats is not None:
            properties[field]['minimum'] = stats[field]['min']
            properties[field]['maximum'] = stats[field]['max']

    encoder_dicts = encoder_package['one_hot_encoder_dicts']

    for field, value_dicts in encoder_dicts.items():
        values = sorted(value_dicts.items(), key=lambda x: x[1])
        levels = [v[0] for v in values]
        levels = levels + [unknown_level_value]

        properties[field] = {
            "type": "string",
            "title": field.capitalize(),
            "required": True,
            "enum": levels
        }

    schema = {
        "title": "Input features",
        "description": "Enter features",
        "type": "object",
        "properties": properties
    }

    return schema


def encoder_package_to_options(encoder_package):

    fields = {}
    for field in encoder_package['numeric_cols']:
        fields[field] = {
            "size": 20,
            # "helper": "Please enter %s" % field
        }

    encoder_dicts = encoder_package['one_hot_encoder_dicts']

    for field, value_dicts in encoder_dicts.items():
        values = sorted(value_dicts.items(), key=lambda x: x[1])
        levels = [v[0] for v in values]
        levels = levels + [unknown_level_value]

        fields[field] = {
            "type": "select",
            # "helper": "Select %s" % field,
            "optionLabels": levels,
            "sort": False
        }

    options = {
        "form": {
            "attributes": {
                "action": "http://httpbin.org/post",
                "method": "post"
            },
            "buttons": {
                "submit": {}
            }
        },
        "helper": "Hit submit to update the prediction",
        "fields": fields}

    return options


def encoder_package_to_form_data(encoder_package):
    schema = encoder_package_to_schema(encoder_package)
    options = encoder_package_to_options(encoder_package)

    stats = encoder_package['numeric_stats']

    if stats is None:
        data = {field: 0 for field in encoder_package['numeric_cols']}
    else:
        data = {field: "%0.2f" % stats[field]['median'] for field in encoder_package['numeric_cols']}

    form_data = {"schema": schema,
                 "options": options,
                 "view": "bootstrap-edit",
                 "data": data}

    return form_data


def generate_form(encoder_package):
    form_data = encoder_package_to_form_data(encoder_package)
    index_html = generate_alpaca_index(form_data=form_data)
    return index_html


def test_generate_form():
    index_html = generate_alpaca_index()
    filename = 'test_generate_form_example.html'
    fp = open(filename, 'w')
    fp.write(index_html)
    fp.close()
    print('wrote test file: %s' % filename)


if __name__ == "__main__":
    test_generate_form()
