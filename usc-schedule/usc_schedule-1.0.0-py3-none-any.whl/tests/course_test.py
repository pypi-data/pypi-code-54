import pytest
from uscschedule import Schedule

schedule = Schedule()


def test_course_counts():
    assert True


def test_course_details():
    csci_201 = schedule.get_course(course_id="CSCI-201", semester_id=20201)
    assert csci_201.cross_listed is False
    assert len(csci_201.sections) == 9
    assert len(csci_201.sections[0].instructors) == 1
    assert csci_201.sections[0].instructors[0].get_name() == "Jeffrey Miller"
    assert csci_201.sections[0].canceled is False
    assert csci_201.sections[0].distance_learning is False
    assert csci_201.sections[0].requires_d_clearance() is True
    assert csci_201.has_lab_sections() is True
    assert csci_201.has_lecture_sections() is True
    assert csci_201.has_discussion_sections() is False


def test_department_details():
    assert True
