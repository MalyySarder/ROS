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

"""Validate motion settings without changing node state."""

import math

LIMITS = {'linear_speed': (0.0, 1.0), 'turn_rate': (-1.0, 1.0),
          'publish_hz': (1.0, 30.0)}


def validate_settings(settings):
    """Reject nonnumeric, nonfinite and out-of-range motion settings."""
    for name, (low, high) in LIMITS.items():
        value = settings[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f'{name} must be a finite number')
        if not math.isfinite(value) or not low <= value <= high:
            raise ValueError(f'{name} must be finite and in [{low}, {high}]')
