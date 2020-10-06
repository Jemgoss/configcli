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


from .. import ConfigCLI_SubCommand

class NamespaceVersion(ConfigCLI_SubCommand):
    """

    """

    def __init__(self, cmdObj):
        ConfigCLI_SubCommand.__init__(self, cmdObj, 'version')

    def getSubcmdDescripton(self):
        return 'The version namespace from the application configuration metadata'

    def populateParserArgs(self, subparser):
        return self.command.addArgument(subparser)

    def run(self, pargs):
        return self.command._get_value("version", None)

    def complete(self, text, argsList):
        return []


ConfigCLI_SubCommand.register(NamespaceVersion)
__all__ = ['NamespaceVersion']
