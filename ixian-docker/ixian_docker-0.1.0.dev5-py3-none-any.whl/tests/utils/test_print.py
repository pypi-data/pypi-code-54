# Copyright [2018-2020] Peter Krenesky
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

from ixian_docker.utils.print import ProgressPrinter


def test_print(snapshot, capsys):
    """
    Test ProgressPrinter
    :param snapshot:
    """

    # create printer and add lines
    printer = ProgressPrinter()
    assert printer.add_line("1") == 0
    assert printer.add_line("2") == 1
    assert printer.add_line("3") == 2

    # can't add the same more than once, but it doesn't raise an error
    assert printer.add_line("1") is None
    assert printer.add_line("2") is None
    assert printer.add_line("3") is None

    # move cursor up and down
    printer.goto(0)
    printer.goto(1)
    printer.goto(2)
    printer.goto(1)
    printer.goto(0)

    # move cursor multiple lines
    printer.goto(2)
    printer.goto(0)

    # repeat lines
    printer.goto(0)
    printer.goto(0)
    printer.goto(2)
    printer.goto(2)

    # add printers from various starting lines
    printer.goto(0)
    assert printer.add_line("4") == 3
    printer.goto(1)
    assert printer.add_line("5") == 4

    # print to all lines
    printer.print("1", "1")
    printer.print("2", "2")
    printer.print("3", "3")
    printer.print("4", "4")
    printer.print("5", "5")

    # print to lines without moving to new line
    printer.print("1", "11")
    printer.print("1", "111")

    # move cursor and print lines
    printer.print("1", "1111")
    printer.print("5", "5555")
    printer.print("2", "2222")
    printer.print("4", "4444")
    printer.print("3", "3333")

    # complete printing
    printer.complete()

    out, err = capsys.readouterr()
    snapshot.assert_match(out)
