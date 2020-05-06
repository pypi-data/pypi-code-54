import pytest

from huscy.appointments.models import Invitation
from huscy.appointments.services import accept_appointment


def test_accept_appointment_with_appointment_id_shows_deprecation_warning(invitation):
    with pytest.warns(DeprecationWarning):
        appointment = accept_appointment(invitation.appointment.id, 'participant')

    invitation.refresh_from_db()

    assert invitation.appointment == appointment
    assert invitation.participant == 'participant'
    assert invitation.status == Invitation.STATUS.get_value('accepted')


def test_accept_appointment_with_appointment_object(invitation):
    appointment = accept_appointment(invitation.appointment, 'participant')

    invitation.refresh_from_db()

    assert invitation.appointment == appointment
    assert invitation.participant == 'participant'
    assert invitation.status == Invitation.STATUS.get_value('accepted')
