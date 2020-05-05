import os
import argparse
from git import Repo
from template_library.library_tools import LibraryTools
import zipfile
import requests
import json
import io, zipfile
library_tools = LibraryTools()
env_path = os.getenv("HOME") + "/.template_library"


def validate_content(node_type_path, args, api_address, headers):
    node_file_list = []
    for node_subdir, node_dirs, node_files in os.walk(node_type_path):
        for file in node_files:
            node_file_list.append(file)
    implementation = any('.yml' in x for x in node_file_list)
    definition = 'NodeType.tosca' in node_file_list
    if not implementation:
        print("Implementation missing for " + node_type_path + "\n")
    if not definition:
        print("Definition missing for " + node_type_path + "\n")

    api_url = api_address + "/api/templates"
    name, group = get_name_type(node_type_path)
    access = json.loads(args.public_access.lower())
    data = {
        "shorthand_name": args.name,
        "type_uri": group,
        "template_type_id": 7,
        "public_access": str(access)
    }

    headers = authorization(headers)

    try:
        response = requests.post(api_url, data=str(data), headers=headers)
        response.raise_for_status()
        template_id = json.loads(response.content.decode("utf-8"))["object_id"]
    except requests.HTTPError as e:
        print(e.response.content.decode("utf-8"))
        if e.response.status_code == 406:
            api_url = api_address + "/api/templates/name/" + args.name
            try:
                response = requests.get(api_url, headers=headers)
                template_id = json.loads(response.content.decode("utf-8"))["id"]
                response.raise_for_status()
            except requests.HTTPError as e:
                print(e.response.content.decode("utf-8"))

    api_url = api_address + "/api/versions"

    data = {
        "template_id": template_id,
        "version": args.version
    }
    files = {}
    if implementation:
        # TODO: add all files
        impl = {
            "implementation_file": ("create.yml", open(args.path + "/files/create.yml", 'rb'), 'application-type')
        }
        files.update(impl)
    if definition:
        defi = {
            "template_file": ("NodeType.tosca", open(args.path + "/NodeType.tosca", 'rb'), 'application-type')
        }
        files.update(defi)

    headers.pop("Content-type")
    try:
        response = requests.Session().post(api_url, headers=headers, data=data, files=files)
        response.raise_for_status()
        print("New template version created!")
    except requests.HTTPError as e:
        print(e.response.content.decode("utf-8"))
        exit(1)


def download_template(args, api_address, headers):
    api_url = api_address + "/api/versions/files/" + args.version_id
    headers = authorization(headers)
    try:
        response = requests.get(api_url, headers=headers)
        # TODO: check if response is zip
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall(path=args.path)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e.response.content.decode("utf-8"))
        exit(1)


def list_templates(args, api_address, headers):
    access = json.loads(args.public_access.lower())
    headers = authorization(headers)

    if access:
        api_url = api_address + "/api/templates"

    else:
        file = open(env_path + "/.username", "r")
        env_username = file.read()
        file.close()

        api_url = api_address + "/api/templates/user/name/" + env_username

    try:
        response = requests.get(api_url, headers=headers)
        for i in json.loads(response.content.decode("utf-8")):
            if not args.name:
                print(i)
            elif i["shorthandName"] == args.name:
                print(i)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e.response.content.decode("utf-8"))
        exit(1)


def list_versions(args, api_address, headers):
    api_url = api_address + "/api/versions/template/" + args.template_id
    # TODO: get by template name api/versions/template/name/my_template
    headers = authorization(headers)
    try:
        response = requests.get(api_url, headers=headers)
        print(response.content)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e.response.content.decode("utf-8"))
        exit(1)


def authorization(headers):
    try:
        file = open(env_path + "/.token", "r")
        env_token = file.read()
        file.close()
        if not env_token:
            print("Please log in.")
        else:
            headers["Authorization"] = "Bearer " + env_token
    except Exception as e:
        print("Please log in.")
        exit(1)
    return headers


def get_artifact_warnings():
    return library_tools.get_warnings_log()


def get_definition(node_type_path):
    node_file_list = []
    for node_subdir, node_dirs, node_files in os.walk(node_type_path):
        for file in node_files:
            node_file_list.append(file)
            if '.tosca' in file:
                return file


def get_name_type(node_type_path):
    node_type_path += "/" + get_definition(node_type_path)
    data_dict = library_tools.implementation_to_dictionary(node_type_path)
    group, name = list(data_dict['node_types'].keys())[0].rsplit('.', 1)
    return name, group


def store_true():
    return True


def main():

    parser = argparse.ArgumentParser()

    command_options = parser.add_subparsers(dest='command')

    templates = command_options.add_parser('template', help='Edit a template.')
    template_options = templates.add_subparsers(dest='template_options')
    save = template_options.add_parser('save', help='Save a template to database.')
    get = template_options.add_parser('get', help='Get a template from database.')
    list_parser = template_options.add_parser('list', help='List templates from database.')
    version_parser = template_options.add_parser('version', help='Version options for templates.')

    version_options = version_parser.add_subparsers(dest='version_options')
    list_version = version_options.add_parser('list', help='List versions of a template from database.')
    list_version.add_argument('--template_id', help='Id of the template.', dest='template_id', required=True)

    save.add_argument('--name', help='Name of the template.', dest='name', required=True)
    save.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                           required=True)
    save.add_argument('--public_access', help='Is template available to the public or just this account',
                           dest='public_access', required=True)
    save.add_argument('--version', help='Version of the template to upload/download',
                           dest='version', required=True)

    get.add_argument('--version_id', help='Id of the template.', dest='version_id', required=True)
    get.add_argument('--path', help='Path to the template code or desired template location.', dest='path',
                           required=True)
    get.add_argument('--public_access', help='Is template available to the public or just this account',
                           dest='public_access', required=True)

    list_parser.add_argument('--name', help='Name of the template.', dest='name')
    list_parser.add_argument('--public_access', help='Is template available to the public or just this account',
                     dest='public_access', required=True)

    setup = command_options.add_parser('setup', help='Setup client variables.')

    login = command_options.add_parser('login', help='Login to your account.')
    login.add_argument('--username', help='Username of the user.', dest='username', required=True)
    login.add_argument('--password', help='Password of the user.', dest='password', required=True)

    args = parser.parse_args()

    if args.command == "setup":
        try:
            os.mkdir(env_path)
        except Exception as e:
            pass
        api_endpoint = input("Enter API endpoint (http://host:port):")
        file_endpoint = open(env_path + "/.endpoint", "w")
        file_endpoint.write(api_endpoint)
        file_endpoint.close()

    try:
        file = open(env_path + "/.endpoint", "r")
        api_address = file.read()
        file.close()
    except Exception as e:
        print("Please run xopera-template-library setup first to configure API endpoint.")
        exit(1)

    headers = {"Content-type": "application/json"}

    if args.command == "register":
        api_url = api_address + "/api/auth/register"
        data = {
            "full_name": args.full_name,
            "username": args.username,
            "email": args.email,
            "password": args.password
        }
        try:
            response = requests.post(url=api_url, data=str(data), headers=headers)
            response.raise_for_status()
        except requests.HTTPError as e:
            print(e.response.content.decode("utf-8"))

    if args.command == "login":
        api_url = api_address + "/api/auth/login"
        data = {
            "username": args.username,
            "password": args.password
        }
        try:
            response = requests.post(api_url, data=str(data), headers=headers)
            response.raise_for_status()
            token = json.loads(response.text)["token"]
        except requests.HTTPError as e:
            print(e.response.content.decode("utf-8"))
            exit(1)

        file_token = open(env_path + "/.token", "w")
        file_token.write(token)
        file_token.close()

        file_username = open(env_path + "/.username", "w")
        file_username.write(args.username)
        file_username.close()
        print("User " + args.username + " logged in.")

    if args.command == "template":
        if args.template_options == "save":
            validate_content(args.path, args, api_address, headers)
        if args.template_options == "get":
            download_template(args, api_address, headers)
        if args.template_options == "list":
            list_templates(args, api_address, headers)
        if args.template_options == "version":
            if args.version_options == "list":
                list_versions(args, api_address, headers)
