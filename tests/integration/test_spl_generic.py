#
# Copyright 2019 Delphix
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
#

# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long
# pylint: disable=not-callable

from typing import Any

import pytest
from tests.integration.infra import repl_invoke, dump_exists, slurp_output_file

CMD_TABLE = [
    # avl walker
    "addr spa_namespace_avl | avl",
    "addr spa_namespace_avl | walk",
    "addr arc_mru | member [0].arcs_list[1] | walk | head",

    # multilist walker
    "addr arc_mru | member [0].arcs_list[1] | multilist | head",

    # spl_cache walker
    'spl_kmem_caches | filter \'obj.skc_name == "ddt_cache"\' | walk',
    "spl_kmem_caches | filter 'obj.skc_linux_cache == 0' | spl_cache",
    "spl_kmem_caches | filter 'obj.skc_linux_cache == 0' | spl_cache | cnt",
    # spl_cache - ensure we can walk caches backed by SLUB
    "spl_kmem_caches | filter 'obj.skc_linux_cache > 0' | filter 'obj.skc_obj_alloc > 0' | head 1 | spl_cache",

    # spl_kmem_caches
    "spl_kmem_caches",
    "spl_kmem_caches -o name,source",
    "spl_kmem_caches -v",
    "spl_kmem_caches -s entry_size",
    "spl_kmem_caches -o name,entry_size -s entry_size",
    "spl_kmem_caches -s entry_size | head 4 | spl_kmem_caches",
    "spl_kmem_caches | pp",
]


@pytest.mark.skipif(  # type: ignore[misc]
    not dump_exists(),
    reason="couldn't find crash dump to run tests against")
@pytest.mark.parametrize('cmd', CMD_TABLE)  # type: ignore[misc]
def test_cmd_output_and_error_code(capsys: Any, cmd: str) -> None:
    assert repl_invoke(cmd) == 0
    captured = capsys.readouterr()
    assert captured.out == slurp_output_file("spl", cmd)
