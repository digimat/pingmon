# super basic ping monitor service

import time
import logging
import logging.handlers

# pip install ping
import ping


class PingMon(object):
	def __init__(self, logfpath=None):
		self._hosts=[]
		self._logger=logging.getLogger('pingmon')

		if not logfpath:
			logfpath='/var/log/pingmon.log'

		handler=logging.handlers.RotatingFileHandler(logfpath, maxBytes=20000, backupCount=10)
		formatter=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
		handler.setFormatter(formatter)

		self.logger.addHandler(handler)
		self.logger.setLevel(logging.DEBUG)

	@property
	def logger(self):
	    return self._logger

	def addHost(self, host):
		self._hosts.append(host)
		self.logger.info('Adding host [%s] to monitor' % host)

	def manager(self):
		if self._hosts:
			for host in self._hosts:
				try:
					(ploss, maxrt, meanrt)=ping.quiet_ping(host, count=1)
					#print "%s/%d/%d" % (host, ploss, maxrt)
					if ploss==100:
						self.logger.error('unreachable host [%s]' % host)
					elif ploss>0:
						self.logger.warning('partial ping for host [%s] loss:%d%% max:%dms mean:%dms' % (host, ploss, maxrt, meanrt))
				except:
					self.logger.error('exception occured while processing host %s' % host)

	def run(self, period=1):
		self.logger.info('starting manager with period of %ds' % period)
		try:
			while 1:
				self.manager()
				time.sleep(period)
		except:
			pass

		self.logger.info('halting manager')


if __name__=='__main__':
	pmon=PingMon()
	pmon.addHost('192.168.0.252')
	pmon.addHost('192.168.0.84')
	pmon.run(1)

