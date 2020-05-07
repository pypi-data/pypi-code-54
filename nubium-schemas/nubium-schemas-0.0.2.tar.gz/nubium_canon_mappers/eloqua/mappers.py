from nubium_canon_mappers.eloqua.timestamp_helpers import elq_est_timestamp_to_utc_timestamp
from nubium_schemas.campaign_response import campaign_response_schema


def contacts_inquiries_mapper(record):
    """
    Remaps cdo update to a Campaign Response for the canonical topic
    :param record: relevant cdo record
    :type record: dict
    :return: cdo record remapped for the Campaign Response canonical topic
    :rtype: list
    """
    return {
        "email_address": record['field_map']["Contacts.Inquiries.C_EmailAddress"],
        "ext_tactic_id": record['field_map'].get("Contacts.Inquiries.A_TacticID_External", ""),
        "int_tactic_id": record['field_map'].get("Contacts.Inquiries.A_TacticID_Internal", ""),
        "offer_id": record['field_map']["Contacts.Inquiries.A_OfferID"],
        "offer_consumption_timestamp": elq_est_timestamp_to_utc_timestamp(record['field_map']["Contacts.Inquiries.A_Timestamp"]),
        "last_updated_by": "eloqua",
        "tracking_ids": {
            "eloqua_contacts_inquiries_id": record["cdo_record_id"],
            "sfdc_contact_id": record['field_map'].get("Contacts.Inquiries.S_SFDC_ContactID", ""),
            "sfdc_lead_id": record['field_map'].get("Contacts.Inquiries.S_SFDC_LeadID", ""),
            "sfdc_ext_tactic_lead_id": record['field_map'].get("Contacts.Inquiries.S_Tactic_Ext_Member_ID_Lead", ""),
            "sfdc_int_tactic_lead_id": record['field_map'].get("Contacts.Inquiries.S_Tactic_Int_Member_ID_Lead", ""),
            "sfdc_offer_lead_id": record['field_map'].get("Contacts.Inquiries.S_Offer_Member_ID_Lead", ""),
            "sfdc_ext_tactic_contact_id": record['field_map'].get("Contacts.Inquiries.S_Tactic_Ext_Member_ID_Contact", ""),
            "sfdc_int_tactic_contact_id": record['field_map'].get("Contacts.Inquiries.S_Tactic_Int_Member_ID_Contact", ""),
            "sfdc_offer_contact_id": record['field_map'].get("Contacts.Inquiries.S_Offer_Member_ID_Contact", "")
        }
    }


def elq_contacts_mapper():
    return None


def get_eloqua_records_mapper_for_canon(mapper_name):
    eloqua_canon_mapper = {
        "Contacts.Inquiries": contacts_inquiries_mapper,
        "Eloqua_Contacts": elq_contacts_mapper
    }
    return eloqua_canon_mapper[mapper_name]


def get_canon_schema(mapper_name):
    canon_schemas = {
        "Contacts.Inquiries": campaign_response_schema
    }
    return canon_schemas[mapper_name]
