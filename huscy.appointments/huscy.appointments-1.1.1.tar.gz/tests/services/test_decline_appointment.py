import pytest

from huscy.appointments.models import Invitation
from huscy.appointments.services import decline_appointment


def test_decline_appointment_with_appointment_id_shows_deprecation_warning(invitation):
    with pytest.warns(DeprecationWarning):
        appointment = decline_appointment(invitation.appointment.id, 'participant')

    invitation.refresh_from_db()

    assert invitation.appointment == appointment
    assert invitation.participant == 'participant'
    assert invitation.status == Invitation.STATUS.get_value('declined')


def test_decline_appointment_with_appointment_object(invitation):
    appointment = decline_appointment(invitation.appointment, 'participant')

    invitation.refresh_from_db()

    assert invitation.appointment == appointment
    assert invitation.participant == 'participant'
    assert invitation.status == Invitation.STATUS.get_value('declined')
