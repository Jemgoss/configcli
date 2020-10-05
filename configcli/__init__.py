#
# Copyright (c) 2018 BlueData Software, Inc.
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


try:
    from abc import ABC, abstractmethod
except:
    from abc import ABCMeta, abstractmethod
    class ABC(object):
        __metaclass__ = ABCMeta
import argparse, copy

from .utils import isDebug
from .utils.misc import processArgs
from .version import __version__


class ConfigCLI_SubCommand(ABC):
    """

    """

    def __init__(self, cmdObj, subcmd):
        self.command = cmdObj

        # Register this SubCommand with the parent Command.
        cmdObj.addSubcommand(subcmd, self)

    def setParams(self, ccli, log, config, parser):
        self.log = log
        self.ccli = ccli
        self.config = config
        self.parser = parser

    @abstractmethod
    def getSubcmdDescripton(self):
        raise Exception("Function must be implemented.")

    @abstractmethod
    def populateParserArgs(self, subparser):
        raise Exception("Function must be implemented.")

    @abstractmethod
    def run(self, processedArgs):
        """
        The implementation of this method must return True on successful
        completion and False on a failure.
        """
        raise Exception("Function must be implemented.")

    @abstractmethod
    def complete(self, text, argsList):
        raise Exception("Function must be implemented.")

class ConfigCLI_Command(ABC):
    """

    """

    def __init__(self, ccli, cmd, desc):
        """

        """
        self.cmd = cmd
        self.ccli = ccli
        self.parser = argparse.ArgumentParser(prog=cmd, description=desc)
        self.subparsers = self.parser.add_subparsers(dest='subcmd',
                                                     title='Subcommands')
        self.subcommands = {}
        ccli._add_command(cmd, self)

    def addSubcommand(self, subcmd, subcmdObj):
        desc = subcmdObj.getSubcmdDescripton()
        parser_subcmd = self.subparsers.add_parser(subcmd, help=desc,
                                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        subcmdObj.populateParserArgs(parser_subcmd)

        self.subcommands[subcmd] = subcmdObj
        subcmdObj.setParams(self.ccli, self.log, self.config, parser_subcmd)

    def getSubcommandObject(self, name):
        """
        Returns the subcommand object corresponding to the name, if it exists

        This is useful when configcli is being used as a python library to get
        the command objects. Each command object has its own publicly available
        methods.

        For example:
            macro = configcli.getCommandObject('macro')
            nodeMacro = macro.getSubcommandObject('node')
            ...

        """
        if (name != None) and (name in self.subcommands):
            return self.subcommands[name]
        else:
            return None

    def setLogger(self, log):
        self.log = log

    def setConfig(self, config):
        self.config = config

    def _split_line(self, line):
        return line.strip().split()

    def _invoke_subcmd_complete(self, splits, text):
        subcmd = splits.pop(0)
        try:
            subcmdObj = self.subcommands[subcmd]
            return getattr(subcmdObj, 'complete')(text, splits)
        except KeyError:
            raise Exception("Unknown subcommand: %s" % subcmd)

    def run(self, line):
        """
        """
        args = processArgs(self.parser, line)
        if args is not None:
            subcmdObj = self.subcommands[args.subcmd]

            if isDebug():
                print("DEBUG: ", self.cmd, " args:", args)

            return subcmdObj.run(args)

        return None

    def help(self):
        """

        """
        self.parser.print_help()

    def complete(self, text, line, begidx, endidx):
        """

        """
        splits = self._split_line(line.strip())
        if (len(splits) < 2 and text == '') or (len(splits) == 2 and text != ''):
            completionOpts = copy.deepcopy(list(self.subcommands.keys()))
            completionOpts.append('-h')
            return [x for x in completionOpts if x.startswith(text)]
        else:
            splits.pop(0)
            return self._invoke_subcmd_complete(splits, text)

from .configcli import ConfigCli

__all__ = [ "ConfigCli", "__version__" ]
