
campaign_response_schema = {
    "name": "campaign_response",
    "type": "record",
    "fields": [
        {"name": "email_address", "type": "string", "default": ""},
        {"name": "ext_tactic_id", "type": "string", "default": ""},
        {"name": "int_tactic_id", "type": "string", "default": ""},
        {"name": "offer_id", "type": "string", "default": ""},
        {"name": "offer_consumption_timestamp","type": "string", "default": ""},
        {
            "name": "tracking_ids",
            "type": {
                "type": "record",
                "name": "tracking_id_schema",
                "fields": [
                    {"name": "eloqua_contacts_inquiries_id", "type": "string", "default": ""},
                    {"name": "sfdc_contact_id", "type": "string", "default": ""},
                    {"name": "sfdc_lead_id","type": "string", "default": ""},
                    {"name": "sfdc_ext_tactic_lead_id", "type": "string", "default": ""},
                    {"name": "sfdc_int_tactic_lead_id", "type": "string", "default": ""},
                    {"name": "sfdc_offer_lead_id", "type": "string", "default": ""},
                    {"name": "sfdc_ext_tactic_contact_id", "type": "string", "default": ""},
                    {"name": "sfdc_int_tactic_contact_id", "type": "string", "default": ""},
                    {"name": "sfdc_offer_contact_id", "type": "string", "default": ""}
                ]
            }
        }
    ]
}
