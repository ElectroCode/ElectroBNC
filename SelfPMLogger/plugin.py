###
# Copyright (c) 2013, Ken Spencer
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
import supybot.ircmsgs as ircmsgs
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.world as world

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('SelfPMLogger')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class SelfPMLogger(callbacks.Plugin):
    """Add the help for "@plugin help SelfPMLogger" here
    This should describe *how* to use this plugin."""
    threaded = True
    def _getIrc(self, network):
        irc = world.getIrc(network)
        if irc:
            return irc
        else:
            raise callbacks.Error, \
                  'I\'m not currently connected to %s.' % network

    def doPrivmsg(self, irc, msg):
        if irc.network == self.registryValue('masternetwork'):
            if irc.isChannel(msg.args[0]) == False:
                irc.sendMsg(ircmsgs.privmsg('\x23ElectroBNC.log', "MSG from %s: %s" % (msg.nick, msg.args[1])))
        elif irc.network != self.registryValue('masternetwork'):
            if irc.isChannel(msg.args[0]) == False:
                otherIrc = self._getIrc(self.registryValue('masternetwork'))
                otherIrc.queueMsg(ircmsgs.privmsg("\x23ElectroBNC.log", "MSG from %s@%s: %s" % (msg.nick, irc.network, msg.args[1])))
        irc.noReply()

Class = SelfPMLogger


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
