# -*- coding: utf-8 -*-

"""
    Incursion Add-on

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
"""
from resources.lib.modules import log_utils
from resources.lib.modules import control
import threading

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

def syncTraktLibrary():
    control.execute(
        'RunPlugin(plugin://%s)' % 'plugin.video.incursion/?action=tvshowsToLibrarySilent&url=traktcollection')
    control.execute(
        'RunPlugin(plugin://%s)' % 'plugin.video.incursion/?action=moviesToLibrarySilent&url=traktcollection')

try:
    ModuleVersion = control.addon('script.module.incursion').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.incursion').getAddonInfo('version')
    #RepoVersion = control.addon('repository.colossus').getAddonInfo('version')

    log_utils.log('######################### INCURSION ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT INCURSION VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### INCURSION PLUGIN VERSION: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### INCURSION SCRIPT VERSION: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    #log_utils.log('### INCURSION REPOSITORY VERSION: %s ###' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('######################### INCURSION ############################', log_utils.LOGNOTICE)
    log_utils.log('####### CURRENT INCURSION VERSIONS REPORT ######################', log_utils.LOGNOTICE)
    log_utils.log('### ERROR GETTING INCURSION VERSIONS - NO HELP WILL BE GIVEN AS THIS IS NOT AN OFFICIAL INCURSION INSTALL. ###', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)

if control.setting('autoTraktOnStart') == 'true':
    syncTraktLibrary()

if int(control.setting('schedTraktTime')) > 0:
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
    log_utils.log('#################### STARTING TRAKT SCHEDULING ################', log_utils.LOGNOTICE)
    log_utils.log('#################### SCHEDULED TIME FRAME '+ control.setting('schedTraktTime')  + ' HOURS ################', log_utils.LOGNOTICE)
    timeout = 3600 * int(control.setting('schedTraktTime'))
    schedTrakt = threading.Timer(timeout, syncTraktLibrary)
    schedTrakt.start()
