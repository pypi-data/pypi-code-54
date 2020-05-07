import zcrmsdk
import threading

localzoho_config = \
    {
            "currentUserEmail": "aswinkumar.m+apiautomation@zohocorp.com",
            "client_id": "1000.8TAE9Z2NUVCY20458BMAR9XSXW2ENH",
            "client_secret": "927df925ab8e7c3b1a4603b14173311a84dd064f4d",
            "redirect_uri": "https://crm.zoho.com",
            "accounts_url": "https://accounts.localzoho.com",
            "apiBaseUrl": "https://crm.localzoho.com"
    }

threading.current_thread().__setattr__('currentUserEmail', 'aswinkumar.m+apiautomation@zohocorp.com')
zcrmsdk.ZCRMRestClient.initialize(localzoho_config)

oauth_instance = zcrmsdk.ZohoOAuth.get_client_instance()
oauth_instance.generate_access_token('grant_token')
oauth_instance.generate_access_token_from_refresh_token('refresh-token','user_email')
oauth_instance.refresh_access_token()


# junction_instance = zcrmsdk.ZCRMJunctionRecord.get_instance('Contact_Roles','525508000004767046')
# junction_instance.related_data['Contact_Role'] = "Developer/Evaluator"
# resp = zcrmsdk.ZCRMRecord.get_instance('Potentials').add_relation(junction_instance)

resp = zcrmsdk.ZCRMModule.get_instance('Leads').get_records().data

for each_resp in resp:
    print(vars(each_resp))
# user_list = zcrmsdk.operations.ZCRMOrganization.get_instance().get_users(None)
# user_map = dict()
# user_map['params'] = dict()
# a = 1.2
# b = 1
# print(type(a))
# print(type(b))
# print("TRUE") if type(a) == type(b) else print("FALSE")
#
# test_resp = zcrmsdk.ZCRMRecord.get_instance('Leads','525508000004139013').upload_link_as_attachment('www.zoho.com')
# print("here")
# # user_list = zcrmsdk.Org.ZCRMOrganization.get_instance().get_all_users()
# # user_list = zcrmsdk.operations.org.ZCRMOrganization.get_instance().get_users(user_map)
#
# user = zcrmsdk.operations.ZCRMUser.get_instance()
# user.first_name='first'
# user.last_name='last'
# user.email='aswinkumar.m+firstlast@zohocorp.com'
# role_inst = zcrmsdk.operations.ZCRMRole.get_instance()
# role_inst.id=525508000000015969
# role_inst.name='Manager'
# user.role=role_inst
# profile_inst = zcrmsdk.operations.ZCRMProfile.get_instance()
# profile_inst.id=525508000000015972
# profile_inst.name='Administrator'
# user.profile=profile_inst
# user.create_user(user_map)
# print("here")

# a = zcrmsdk.automation.Automate.get_instance()
# a.test()

# org_inst = zcrmsdk.ZCRMRestClient.get_instance().get_organization_details()
# users_inst = zcrmsdk.ZCRMOrganization.get_instance().get_all_users()
# user_inst = zcrmsdk.ZCRMOrganization.get_instance().get_user('525508000000546001')
# modules_inst = zcrmsdk.ZCRMRestClient.get_instance().get_all_modules()
# cv_inst = zcrmsdk.ZCRMModule.get_instance('Leads').get_all_customviews()
# rec_inst = zcrmsdk.ZCRMModule.get_instance('Leads').get_records(cvid='cvid',page=1,per_page=30)
# layout_inst = zcrmsdk.ZCRMModule.get_instance('Leads').get_all_layouts()
# l_inst = zcrmsdk.ZCRMModule.get_instance('Leads').get_layout(layout_id=id)
# notes_list = zcrmsdk.ZCRMRecord.get_instance('Leads','525508000004136046').get_relatedlist_records()


# related_list = zcrmsdk.ZCRMModule.get_instance('Leads').get_all_relatedlists()
# try:
#     rel_inst = zcrmsdk.ZCRMRecord.get_instance('Leads','525508000004136046').get_relatedlist_records('Products')
# print("here")

import os
import webbrowser
# dir_path = '/Users/aswin-7455/Downloads/'
# filename = 'test.html'
# os.chdir(dir_path)
# f = open(filename,'w')
# html_string = """<html>
# <head></head>
# <body><p>Hello World!</p></body>
# </html>
# """
# f.write(html_string)
# f.close()
# print(dir_path + filename)
# filename = dir_path + filename
# try:
#     webbrowser.open_new_tab(filename)
# except Exception:
#     raise Exception