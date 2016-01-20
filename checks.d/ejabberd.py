# Datadog Agent Check Plugin for Ejabberd
# debug for:
# sudo -u dd-agent dd-agent check ejabberd

from checks import AgentCheck
import xmlrpclib

class EjabberdCheck(AgentCheck):
    SERVICE_CHECK_NAME = 'ejabberd.is_ok'

    def __init__(self, name, init_config, agentConfig, instances=None):
        AgentCheck.__init__(self, name, init_config, agentConfig, instances)

    def check(self, instance):
        verbose = self.init_config.get('verbose', False)
        server = xmlrpclib.ServerProxy(instance['url'], verbose=verbose);
        auth = {'user': instance['user'], 'server': instance['server'], 'password': instance['password']}
        res = server.stats(auth, {'name': 'onlineusers'})
        self.gauge('ejabberd.onlineusers', res['stat'])
        res = server.stats(auth, {'name': 'onlineusersnode'})
        self.gauge('ejabberd.onlineusersnode', res['stat'])
        res = server.stats(auth, {'name': 'registeredusers'})
        self.gauge('ejabberd.registeredusers', res['stat'])
        try:
            res = server.stats(auth, {'name': 'processes'})
            self.gauge('ejabberd.processes', res['stat'])
        except:
            pass
        res = server.incoming_s2s_number(auth)
        self.gauge('ejabberd.s2s_incoming', res['s2s_incoming'])
        res = server.outgoing_s2s_number(auth)
        self.gauge('ejabberd.s2s_outgoing', res['s2s_outgoing'])
        self.service_check(self.SERVICE_CHECK_NAME, AgentCheck.OK)

