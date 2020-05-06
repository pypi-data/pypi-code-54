import pandas as pd


def extract_event_date_by_sorting(
    events_shipment_df: pd.DataFrame, mask, ascending: bool, location_key=None
):
    events_shipment = (
        events_shipment_df[mask]
        .sort_values(by="date", ascending=ascending)
        .reset_index(drop=True)
    )
    if len(events_shipment) > 0 and location_key is not None:
        if events_shipment.loc[0, "location_type"] == location_key:
            return events_shipment.loc[0, "date"]
        return None
    if len(events_shipment) > 0:
        return events_shipment.loc[0, "date"]
    return None


def extract_pickup_event_date(shipment_id: float, events_shipment_df: pd.DataFrame):
    mask_shipment = events_shipment_df["shipment_id"] == shipment_id
    mask_event = events_shipment_df["event_description"].apply(lambda e: "Pickup" in e)
    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_event,
        ascending=True,
    )

    event_found_by_order = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment,
        ascending=True,
        location_key="warehouse",
    )

    return event_found_by_description or event_found_by_order


def extract_departure_event_date(shipment_id: float, events_shipment_df: pd.DataFrame):
    mask_shipment = events_shipment_df["shipment_id"] == shipment_id
    mask_etd = events_shipment_df["is_used_for_etd"] == True
    mask_event = events_shipment_df["event_description"].apply(
        lambda e: "Departure" in e or "Vessel Departure" in e
    )
    event_found_by_etd = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_etd,
        ascending=True,
    )

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_event,
        ascending=True,
    )

    event_first = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment,
        ascending=True,
        location_key="harbor",
    )
    return event_found_by_etd or event_found_by_description or event_first


def extract_arrival_event_date(shipment_id: float, events_shipment_df: pd.DataFrame):
    mask_shipment = events_shipment_df["shipment_id"] == shipment_id
    mask_eta = events_shipment_df["is_used_for_eta"] == True
    mask_event = events_shipment_df["event_description"].apply(
        lambda e: "Arrival" in e or "Vessel Arrival" in e
    )
    events_shipment = (
        events_shipment_df[mask_shipment & mask_eta]
        .sort_values(by="date", ascending=False)
        .reset_index(drop=True)
    )
    if len(events_shipment) > 0:
        return events_shipment.loc[0, "date"]

    event_found_by_eta = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_eta,
        ascending=False,
    )

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_event,
        ascending=False,
    )

    event_last = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment,
        ascending=False,
        location_key="harbor",
    )
    return event_found_by_eta or event_found_by_description or event_last


def extract_delivery_event_date(shipment_id: float, events_shipment_df: pd.DataFrame):
    mask_shipment = events_shipment_df["shipment_id"] == shipment_id
    mask_event = events_shipment_df["event_description"].apply(
        lambda e: "Delivery" in e
    )

    event_found_by_description = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment & mask_event,
        ascending=False,
    )

    event_last = extract_event_date_by_sorting(
        events_shipment_df=events_shipment_df,
        mask=mask_shipment,
        ascending=False,
        location_key="warehouse",
    )

    return event_found_by_description or event_last
