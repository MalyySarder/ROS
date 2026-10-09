# Copyright 2026 Nikita
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Keep package linters scoped to patrol when pytest starts at workspace root."""

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def package_working_directory(monkeypatch):
    """Match colcon's package-local working directory for all entry points."""
    monkeypatch.chdir(Path(__file__).resolve().parents[1])
