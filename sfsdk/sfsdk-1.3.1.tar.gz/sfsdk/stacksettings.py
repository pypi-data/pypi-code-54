# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from sfsdk import exrsettings, log, utils
from ruamel import yaml
import os
import glob
import re
import shutil
import json
import copy
import uuid
import tempfile

workspace_dir = None

def load(base_dir):

    global workspace_dir

    workspace_dir = os.path.join(
            base_dir,
            'stack'
    )

    if not os.path.exists(workspace_dir):
        os.makedirs(workspace_dir)

def get_standard_stack_name(stack):

     tech = re.sub(
            "[^a-z0-9]",
            "_",
            stack['technology'].lower()
            )

     title = re.sub(
            "[^a-z0-9]",
            "_",
            stack.get('variant', '').lower()
            )

     long_uuid = stack['uuid']

     if long_uuid[:6] in ('local-', 'sfsdk-'):
         shorter_uuid = long_uuid[:10]
     else:
         shorter_uuid = long_uuid[:4]

     return '%s_%s-%s' % (tech, title, shorter_uuid)

def save_stack_meta(stack_yaml_orig):

    stack_yaml = copy.deepcopy(stack_yaml_orig)

    stack = get_standard_stack_name(stack_yaml)

    stack_dir = os.path.join(workspace_dir, stack)

    if not os.path.exists(stack_dir):
        os.makedirs(stack_dir)

    information_text = stack_yaml['md']['text']
    information_text = utils.save_and_replace_b64_with_media(
        base_folder = stack_dir,
        content = information_text,
        content_name = 'stack'
    )
    with open(os.path.join(stack_dir, 'stack.md'), 'w+') as f:
        f.write(information_text)
    stack_yaml['md']['text'] = '!import stack.md'

    if log.verbose:
        stack_meta_debug_path = os.path.join(stack_dir, '.last-saved.json')
        log.debug('Saving JSON debug to %s' % (stack_meta_debug_path))
        with open(stack_meta_debug_path, 'w') as f:
              json.dump(stack_yaml_orig, f, indent=4)

    with open(os.path.join(stack_dir, "stack.yml"), "w") as f:
        yaml.dump(stack_yaml, f, default_flow_style=False)

    return stack_dir

def load_stack_meta(stack):

    stack_dir = os.path.join(workspace_dir, stack)

    if not os.path.exists(stack_dir):
        os.makedirs(stack_dir)

    stack_meta_path = os.path.join(stack_dir, 'stack.yml')

    with open(stack_meta_path, 'r') as stream:
        try:
            stack_yaml = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise log.FatalMsg(exc)

        with open(os.path.join(stack_dir, 'stack.md'), 'r') as stream:
            stack_yaml['md']['text'] = utils.load_and_replace_media_with_b64(
                stack_dir,
                stream.read()
            )

    return stack_yaml

def get_stacks():

    stacks = {}

    for stack_yml_path in glob.glob('%s/*/stack.yml' % workspace_dir):

        current_name = stack_yml_path.split('/')[-2]
        
        stacks[current_name] = load_stack_meta(current_name)

    return stacks

def get_stack_by_name(name):

    stack_name = None
    for stack_yml_path in glob.glob('%s/*/stack.yml' % workspace_dir):

        current_name = stack_yml_path.split('/')[-2]

        if current_name == name:
            stack_name = current_name
            break

    if stack_name:
        return load_stack_meta(stack_name)
    else:
        raise log.FatalMsg('The stack does not exist locally')

def get_stack_by_uuid(stack_uuid):
    
    for stack_yml_path in glob.glob('%s/*/stack.yml' % workspace_dir):

        current_name = stack_yml_path.split('/')[-2]

        stack_data = load_stack_meta(current_name)

        if stack_data['uuid'] == stack_uuid:
            return stack_data

def update_stack_folder(old_stack_dir, new_stack_data):

    new_stack_dir = save_stack_meta(new_stack_data)

    if old_stack_dir != new_stack_dir:
        log.warn("Moved from %s to %s" % (old_stack_dir, new_stack_dir))
        shutil.rmtree(old_stack_dir)

def get_normalized_local_stacks(stacks):

    if len(stacks) == 1 and stacks[0] == 'all':
        stacks_data = get_stacks()
    else: 
        # Cut the stack/
        stacks_data = { k[6:]: get_stack_by_name(k[6:]) for k in stacks }

    return stacks_data

def fix_outgoing_stack_data(stack_json):
    
    # Int-ify status
    stack_json['obj']['status'] = int(stack_json['obj']['status'])

    # Add an empty imageUrl if not present
    if not stack_json['obj'].get('imageUrl'):
        stack_json['obj']['imageUrl'] = 'test'

    # Delete md.id flag
    del stack_json['obj']['md']['id']

def delete_stack_by_uuid(stack_uuid):
        
    for stack_yml_path in glob.glob('%s/*/stack.yml' % workspace_dir):

        current_name = stack_yml_path.split('/')[-2]
        current_folder = os.path.dirname(stack_yml_path)

        stack_data = load_stack_meta(current_name)

        if stack_data['uuid'] == stack_uuid:

            tempfolder = tempfile.mkdtemp()

            print("Moving %s to %s" % (current_folder, tempfolder))

            os.rename(current_folder, tempfolder)

            return stack_uuid