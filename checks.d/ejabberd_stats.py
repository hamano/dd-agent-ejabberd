from checks import AgentCheck
import xmlrpclib

class EjabberdStats(AgentCheck):
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

