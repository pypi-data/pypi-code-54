from .utils import CommonUtil

"""
 * 调度管理器
 *<B>说明：</B>
 *<pre>
 *  略
 *</pre>
 *<B>示例：</B>
 *<pre>
 * 略
 *</pre>
"""
class SchedulerManager():

    def __init__(self,**attrs):

        # 默认调度器
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.defaultScheduler = '';

        # 定义调度器
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.customSchedulers = {};

        # 任务调度器对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.taskSchedulers = {};


        if attrs:
            CommonUtil.setAttrs(self,attrs);

        return ;

    def makeTaskScheduler(self, schedulerType, options={})->'TaskScheduler':

        clazz = options.get('clazz', schedulerType)

        if not clazz:
            raise Exception('the {0} task scheduler conf no find clazz'.format(schedulerType))

        if clazz.find('.') == -1:
            clazzName = CommonUtil.ucfirst(clazz) + 'Scheduler'
            clazz = __package__ + '.schedulers.' + clazzName + '.' + clazzName

        taskSchedulerMeta = CommonUtil.getClassMeta(clazz)

        return taskSchedulerMeta(**options);

    def getTaskScheduler(self, schedulerType = '') -> 'TaskScheduler':

        if not schedulerType:
            schedulerType = self.defaultScheduler;

        taskScheduler = self.taskSchedulers.get(schedulerType, None)

        if taskScheduler:
            return taskScheduler

        taskSchedulerConf = self.customSchedulers.get(schedulerType, None)
        if taskSchedulerConf is None:
            raise Exception('the {0} task scheduler conf no find'.format(schedulerType))

        taskScheduler = self.makeTaskScheduler(schedulerType, taskSchedulerConf);

        self.taskSchedulers[schedulerType] = taskScheduler

        return taskScheduler;

    def __getattr__(self, schedulerType):

        return self.getTaskScheduler(schedulerType);


class TaskScheduler():

    def __init__(self,**attrs):

        self.tasks = [];

        if attrs:
            CommonUtil.setAttrs(self,attrs);

        return ;


    def run(self):

        return ;

    def start(self):

        return ;

    def shutdown(self):

        return ;

    def reload(self):

        return ;

    def stop(self):

        return ;

    def status(self):

        return ;

    def getScheduler(self):

        return ;

    def loadConfig(self,options = {}):

        return ;

    def add_task(self,task):

        return ;

    def addTask(self,task = None,**attrs):

        if task:
            self.tasks.append(task);
            self.add_task(task)
        elif attrs:
            self.add_task(Task(**attrs))

        return ;

    def getAllTask(self):

        return ;


class Task():

    def __init__(self,**attrs):

        self.name = '';

        if attrs:
            CommonUtil.setAttrs(self,attrs);

        return ;


