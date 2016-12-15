#!/opt/python3/bin/python3
 
import sys, os, time, atexit
from signal import SIGINT
import logging
import logging.handlers
from multiuser_server import *
 
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
filehandler = logging.handlers.TimedRotatingFileHandler('/tmp/rh-server-daemon.log',when='midnight',interval=1,backupCount=10)
filehandler.setFormatter(logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(filehandler)
 
class Daemon(object):
    """
    Subclass Daemon class and override the run() method.
    """
    def __init__(self, pidfile, stdin='/dev/null', stdout='/tmp/out.txt', stderr='//tmp/err.txt'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
 
    def daemonize(self):
        """
        Deamonize, do double-fork magic.
        """
        try:
            pid = os.fork()
            if pid == 0:
                # Exit first parent.
                sys.exit(0)
        except OSError as e:
            message = "Fork #1 failed: {}\n".format(e)
            sys.stderr.write(message)
            sys.exit(1)
 
        # Decouple from parent environment.
        os.chdir("/")
        os.setsid()
        os.umask(0)
 
        # Do second fork.
        try:
            pid = os.fork()
            if pid == 0:
                # Exit from second parent.
                sys.exit(0)
        except OSError as e:
            message = "Fork #2 failed: {}\n".format(e)
            sys.stderr.write(message)
            sys.exit(1)
 
        logger.info('deamon going to background, PID: {}'.format(os.getpid()))
 
        # Redirect standard file descriptors.
        sys.stdout.flush()
        sys.stderr.flush()
        si = open(self.stdin, 'r')
        so = open(self.stdout, 'a+')
        se = open(self.stderr, 'a+')
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())
 
        # Write pidfile.
        pid = str(os.getpid())
        open(self.pidfile,'w+').write("{}\n".format(pid))
 
        # Register a function to clean up.
        atexit.register(self.delpid)
 
    def delpid(self):
        os.remove(self.pidfile)
 
    def start(self):
        """
        Start daemon.
        """
        # Check pidfile to see if the daemon already runs.
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
 
        if pid:
            message = "Pidfile {} already exist. Daemon already running?\n".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)
 
        # Start daemon.
        self.daemonize()
        self.run()
 
    def status(self):
        """
        Get status of daemon.
        """
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            message = "There is not PID file. Daemon already running?\n"
            sys.stderr.write(message)
            sys.exit(1)
 
        try:
            procfile = open("/proc/{}/status".format(pid), 'r')
            procfile.close()
            message = "There is a process with the PID {}\n".format(pid)
            sys.stdout.write(message)
        except IOError:
            message = "There is not a process with the PID {}\n".format(self.pidfile)
            sys.stdout.write(message)
 
    def stop(self):
        """
        Stop the daemon.
        """
        # Close all connections
        # server_shutdown()
        
        logging.info("Shutting down")
        for process in multiprocessing.active_children():
            logging.info("Shutting down process %r", process)
            process.terminate()
            process.join()
        logging.info("All done")

        # Get the pid from pidfile.
        try:
            pf = open(self.pidfile,'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError as e:
            message = str(e) + "\nDaemon not running?\n"
            sys.stderr.write(message)
            sys.exit(1)
 
        # Try killing daemon process.
        try:
            os.kill(pid, SIGINT)
            time.sleep(1)
        except OSError as e:
            print(str(e))
            sys.exit(1)
 
        try:
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
        except IOError as e:
            message = str(e) + "\nCan not remove pid file {}".format(self.pidfile)
            sys.stderr.write(message)
            sys.exit(1)
 
    def restart(self):
        """
        Restart daemon.
        """
        self.stop()
        time.sleep(1)
        self.start()
 
    def run(self):
        """
        You should override this method when you subclass Daemon.
        It will be called after the process has been daemonized by start() or restart().
 
        Example:
 
        class MyDaemon(Daemon):
            def run(self):
                while True:
                    time.sleep(1)
        """
 
class MyDaemon(Daemon):
    def run(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        server = Server("0.0.0.0", 5005)
        try:
            logging.info("Listening")
            server.start()
        except:
            logging.exception("Unexpected exception")
        finally:
            logging.info("Shutting down")
            for process in multiprocessing.active_children():
                logging.info("Shutting down process %r", process)
                process.terminate()
                process.join()
        logging.info("All done")
 
if __name__ == "__main__":
    daemon = MyDaemon('/tmp/python-daemon.pid')
    if len(sys.argv) == 2:
        logger.info('{} {}'.format(sys.argv[0],sys.argv[1]))
 
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        logger.warning('show cmd deamon usage')
        print ("Usage: {} start|stop|restart|status".format(sys.argv[0]))
        sys.exit(2)