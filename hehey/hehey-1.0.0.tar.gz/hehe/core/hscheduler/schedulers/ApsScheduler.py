from ..scheduler import TaskScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from ..scheduler import Task;
from ..utils import CommonUtil

class ApsScheduler(TaskScheduler):

    def __init__(self,**attrs):

        self.daemonize = False;
        self.tasks = [];
        self.options = [];
        super().__init__(**attrs);

        if self.daemonize:
            self._scheduler = BackgroundScheduler()
        else:
            self._scheduler = BlockingScheduler()

        self._init();

        return ;


    def _init(self):

        # 导入配置
        self._load_config()
        # 导入任务
        self._load_task();

        return ;

    def run(self, paused=False):

        self._scheduler.start();

        return;

    def shutdown(self, wait=True):

        self._scheduler.shutdown(wait)

        return ;

    def stop(self):

        self._scheduler.pause()

        return;

    def start(self):

        self._scheduler.resume()

        return ;

    def reload(self):

        self._scheduler.resume()

        return ;

    def getScheduler(self):

        return self._scheduler

    def buildConfig(self,options:dict):

        opts = options.copy();
        executors = opts.get("executors",{})

        default = executors.get("default",{})
        if isinstance(default,int):
            default = ThreadPoolExecutor(default)
        elif isinstance(default,dict):
            default = ThreadPoolExecutor(**default)
        executors['default'] = default;

        processpool = executors.get("processpool", {})
        if isinstance(processpool, int):
            processpool = ProcessPoolExecutor(processpool)
        elif isinstance(processpool, dict):
            processpool = ProcessPoolExecutor(**processpool)
        executors['processpool'] = processpool;

        opts['executors'] = executors

        return opts;

    def buildTask(self,task:Task):

        attrs = CommonUtil.getAttrs(task)

        return attrs;

    def loadConfig(self,options = {}):

        self._scheduler.configure(self.buildConfig(options));

        return ;

    def getAllTask(self):

        return self._scheduler.get_jobs();

    def add_task(self,task):


        # func, trigger=None, args=None, kwargs=None, id=None, name=None,
        #                 misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
        #                 next_run_time=undefined, jobstore='default', executor='default',
        #                 replace_existing=False

        taskConf = self.buildTask(task);
        func = taskConf.pop('func')

        self._scheduler.add_job(func,**taskConf)

        return ;

    def _load_config(self):

        self._scheduler.configure(self.buildConfig(self.options));

        return ;

    def _load_task(self):

        for task in self.tasks:
            taskConf = self.buildTask(task);
            self._scheduler.add_job(**taskConf)

        return ;


