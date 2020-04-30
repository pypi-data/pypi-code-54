#!/usr/bin/python
#
# Copyright 2018-2020 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest

from marshmallow.exceptions import ValidationError
from tests.utils import BaseTestCase, assert_equal_dict

from polyaxon.polyflow import V1RunKind
from polyaxon.polyflow.operations import V1CompiledOperation
from polyaxon.polyflow.parallel.iterative import V1Iterative


@pytest.mark.workflow_mark
class TestWorkflowV1Iterative(BaseTestCase):
    def test_iterative_config(self):
        config_dict = {
            "kind": "iterative",
            "numIterations": 10,
            "container": {"image": "my-parallel"},
        }
        config = V1Iterative.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

        # Raises for negative values
        config_dict["numIterations"] = -5
        with self.assertRaises(ValidationError):
            V1Iterative.from_dict(config_dict)

        config_dict["numIterations"] = -0.5
        with self.assertRaises(ValidationError):
            V1Iterative.from_dict(config_dict)

        # Add num_runs percent
        config_dict["numIterations"] = 0.5
        with self.assertRaises(ValidationError):
            V1Iterative.from_dict(config_dict)

        config_dict["numIterations"] = 5
        config = V1Iterative.from_dict(config_dict)
        assert_equal_dict(config.to_dict(), config_dict)

    def test_iterative_without_num_iterations(self):
        config_dict = {
            "kind": "compiled_operation",
            "parallel": {
                "kind": "iterative",
                "params": {"lr": {"kind": "choice", "value": [1, 2, 3]}},
                "seed": 1,
                "container": {"image": "my-parallel"},
            },
            "run": {"kind": V1RunKind.JOB, "container": {"image": "foo/bar"}},
        }

        with self.assertRaises(ValidationError):
            V1CompiledOperation.from_dict(config_dict)

        config_dict["parallel"]["numIterations"] = 10
        config = V1CompiledOperation.from_dict(config_dict)
        assert config.to_dict() == config_dict
