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
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
# custom imports
import supybot.ircmsgs as ircmsgs
import sqlite3 as lite
import os
import supybot.world as world
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('BNC')
except:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x:x

class BNC(callbacks.Plugin):
    """Add the help for "@plugin help BNC" here
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
        if 'IP:' in msg.args[1].split():
            if msg.nick == 'ElectroServ':
                irc.sendMsg(ircmsgs.privmsg('\x23ElectroBNC-Staff', msg.args[1]))
                userip = msg.args[1]
                fo = open("ip.txt", 'w')
                fo.write(userip);
        irc.noReply()
    def request(self, irc, msg, args, username, server, port, net, email):
        """<username> <server> <port> <net> <email>
        One BNC per person, if you want another network/server use !addserver // If you would like to remove your account use !remove // Not implemented at the present time, if you need to do either, highlight an op+"""
#        dbpath = self.registryValue(dbpath)
        irc.queueMsg(ircmsgs.privmsg('\x23ElectroBNC', "Request relayed to staff channel. Info: Username: %s Server: %s Port: %s NetName: %s Email: %s // Please note that if you break the rules, your bnc will be removed with no hesitation." % (username, server, port, net, email)))
        if irc.network == "ElectronIRC":
            irc.queueMsg(ircmsgs.privmsg('\x23ElectroBNC-Relay', '!add %s %s %s %s %s' % (username, server, port, net, email)))
        elif irc.network != "ElectronIRC":
            otherIrc = self._getIrc("ElectronIRC")
            otherIrc.queueMsg(ircmsgs.privmsg("\x23ElectroBNC-Relay", "!add %s %s %s %s %s" % (username, server, port, net, email)))
    request = wrap(request, ['something', 'something', 'something', 'something', 'something'])
    def nets(self, irc, msg, args):
        """See what nets are in the database and how many are on each net."""
    nets = wrap(nets)
    def staff(self, irc, msg, args):
        """Returns list of current Staff of ElectroBNC"""
        iota = "Iota - Owner and founder, and a bit of a wacko."
        don = "DonVitoCorleone - Token Serbian xD jk.. Advisor, Plugin helper"
        gl = "GL(GLolol) - Staff in training, Soon to be Support Admin, and is 'Derp of the world'"
        irc.sendMsg(ircmsgs.privmsg('\x23ElectroBNC', '%s // %s // %s' % (iota, don, gl)))
    staff = wrap(staff)
Class = BNC


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
