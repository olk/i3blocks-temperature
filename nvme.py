'''
                     Copyright Oliver Kowalke 2018.
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. 
'''

from subprocess import Popen, PIPE

class NVMe(object):
    class QueryOptions(object):
        def __init__(self):
            self.__options = []

        def temperature(self):
            self.__options.append("-A")

        def arguments(self):
            args = []
            if self.__options:
                qry_args = ""
                for option in self.__options:
                    qry_args += " " + option
                args.extend([qry_args[1:]])
            else:
                raise 
            args.append("/dev/nvme0");
            return args


    class Status(object):
        def __init__(self, proc, timeout=2):
            self.__proc = proc
            self.__timeout = timeout

        def wait(self):
            try:
                out, err = self.__proc.communicate(timeout=self.__timeout)
            except TimeoutExpired:
                self.__proc.kill()
                out, err = self.__proc.communicate()
            return [
                    self.__proc.returncode, out, err]
            

    def _locate(self):
        with Popen(["which", "smartctl"],
                    stdout=PIPE,
                    universal_newlines=True) as proc:
            try:
                out, _ = proc.communicate(timeout=self.timeout)
            except TimeoutExpired:
                proc.kill()
                out, _ = proc.communicate()
        return out.strip()

    def __init__(self, options, timeout=1):
        self.timeout = timeout
        self.cmd = self._locate()
        if not self.cmd:
            raise IOError("failed to locate smartctl")
        if not isinstance(options, (NVMe.QueryOptions)):
            raise TypeError("invalid options provided")
        self.args = options.arguments()

    def execute(self):
        return NVMe.Status(Popen([self.cmd] + self.args,
                    stdout=PIPE, stderr=PIPE,
                    universal_newlines=True))
