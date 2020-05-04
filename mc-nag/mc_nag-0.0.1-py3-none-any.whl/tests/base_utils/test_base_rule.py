"""Tests for BaseRule."""

from pytest import raises
from mc_nag.base_utils.models.rule import BaseRule

TEMPLATE_MODEL = {'raw': 'model'}
OBJECT_ID = '001'


def test_base_rule_good_subclass():
    """Happy Path: Ensure subclass can create with required attributes."""
    class GoodSubclassBaseRule(BaseRule):
        """Create subclass of BaseRule with required attributes."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'Take these actions to fix the violation.'

        def evaluate(self):
            """Logic to implement the rule."""
            return self.template_model

    good_object = GoodSubclassBaseRule(TEMPLATE_MODEL)

    assert good_object.rule_id == OBJECT_ID
    assert good_object.evaluate() == TEMPLATE_MODEL


def test_base_rule_bad_subclass():
    """Sad Path: Catch error when subclass is missing attributes."""
    # pylint: disable=too-few-public-methods
    class RuleMissingAttributes(BaseRule):
        """Create subclass of BaseRule without setting all attributes."""

        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'

    with raises(NotImplementedError,
                match=r"must define.*attribute\(s\)!"):
        _ = RuleMissingAttributes(TEMPLATE_MODEL)

    class RuleMissingEvaluate(BaseRule):
        """Create subclass of BaseRule without evaluate() method."""

        rule_id = OBJECT_ID
        description = 'This is a rule that properly instantiates BaseRule.'
        severity = 'FAIULRE'
        url = 'http://rule.documentation/'
        resolution = 'This is how you fix this violation.'

    rule_missing_evaluate = RuleMissingEvaluate(TEMPLATE_MODEL)
    with raises(NotImplementedError,
                match=r"must implement an evaluate\(\) method with logic"):
        rule_missing_evaluate.evaluate()
