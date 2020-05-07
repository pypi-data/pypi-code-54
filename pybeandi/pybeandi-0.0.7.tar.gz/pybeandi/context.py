import inspect
from typing import Dict, Any, Callable, Type, Set, List, Union

import yaml

from pybeandi.errors import NoSuchBeanError, MultipleBeanInstancesError, ContextInitError, BeanIdAlreadyExistsError
from pybeandi.model import BeanDef, BeanRef, SetBeanRef, GeneralBeanRef, CloseableBean
from pybeandi.util import setup_yaml_env_vars


class BeansList:
    """
    Readonly dictionary-like object to access beans
    """

    def __init__(self, beans=None):
        if beans is None:
            beans = {}
        self._beans = beans

    def get_beans_set(self, bean_ref: SetBeanRef) -> Set[Any]:
        """
        Return set of beans with :bean_ref.ref: class or its subclass
        :param bean_ref: Bean reference instance
        :return: set of beans
        """
        return set(self.get_beans_set_by_class(bean_ref.ref).values())

    def get_beans_set_by_class(self, cls: Type) -> Dict[str, Any]:
        """
        Return dictionary of {bean id : bean object} with :cls: class or its subclass
        :param cls: class or superclass of beans
        :return: dictionary of {bean id : bean object}
        """
        return {bean_id: bean for (bean_id, bean) in self._beans.items() if issubclass(type(bean), cls)}

    def get_bean_by_id(self, bean_id: str) -> Any:
        """
        Return bean from context by its id
        @param bean_id: id of bean
        @return: bean
        @raise NoSuchBeanError: if such bean does not exist
        """
        if bean_id not in self._beans:
            raise NoSuchBeanError(f'Bean with id \'{bean_id}\' does not exist')
        return self._beans[bean_id]

    def get_bean_by_class(self, cls: Type) -> Any:
        """
        Return bean from context by its class
        @param cls: class of bean
        @return: bean
        @raise NoSuchBeanError: if such bean does not exist
        @raise MultipleBeanInstancesError: if more than one beans exist that satisfied given reference
        (for example multiple instances of class or it subclasses)
        """
        beans = self.get_beans_set_by_class(cls)
        if len(beans) == 0:
            raise NoSuchBeanError(f'Bean of class \'{cls.__name__}\' does not exist')
        elif len(beans) > 1:
            raise MultipleBeanInstancesError(f'There are more than one instances of class \'{cls.__name__}\': '
                                             f'{", ".join(beans.keys())}')
        return list(beans.values())[0]

    def _add_as_bean(self, bean_id: str, obj: Any) -> None:
        """
        Register obj as bean
        @param bean_id: id of new bean
        @param obj: object to register as a bean
        """
        if bean_id in self._beans:
            raise BeanIdAlreadyExistsError(f'Bean with id \'{bean_id}\' already exists')
        self._beans[bean_id] = obj

    def values(self):
        return self._beans.values()

    def ids(self):
        return self._beans.keys()

    def __contains__(self, bean_ref: GeneralBeanRef):
        """
        Checks do bean exists by its reference
        @param bean_ref: reference
        @return: do bean exists
        """

        try:
            self[bean_ref]
        except NoSuchBeanError:
            return False
        except MultipleBeanInstancesError:
            return True
        return True

    def __getitem__(self, bean_ref: GeneralBeanRef) -> Union[Any, Set[Any]]:
        """
        General method that returns beans by any type of reference (id, class, BeanRef instance)
        :param bean_ref: id, class or BeanRef instance
        :return: bean or set of beans, depends on :bean_ref:
        """
        if type(bean_ref) is str or inspect.isclass(bean_ref):
            bean_ref = BeanRef(bean_ref)

        if type(bean_ref) is BeanRef:
            if type(bean_ref.ref) is str:
                return self.get_bean_by_id(bean_ref.ref)
            if inspect.isclass(bean_ref.ref):
                return self.get_bean_by_class(bean_ref.ref)
        if type(bean_ref) is SetBeanRef:
            return self.get_beans_set(bean_ref)
        raise ValueError('Provided bean reference is illegal (check its type)')

    def __len__(self):
        return len(self._beans)

    def __iter__(self):
        return iter(self._beans)

    def __str__(self):
        return str(self._beans)


class BeanContext:
    _bean_defs: List[BeanDef]
    _beans: BeansList
    _profiles: Set[str]

    closed: bool = False

    def __init__(self, bean_defs: List[BeanDef], profiles: Set[str]):
        self._bean_defs: List[BeanDef] = bean_defs
        self._beans: BeansList = BeansList()
        self._profiles = profiles

    @property
    def beans(self):
        return self._beans

    @property
    def profiles(self):
        return self._profiles

    def init(self) -> None:
        """
        Initialize context using bean definitions provided earlier
        @raise ContextInitError: is context incorrect
        """
        self._bean_defs = [bean_def for bean_def in self._bean_defs
                           if bean_def.profile_func(self.profiles)]

        bean_ids = [bean_def.bean_id for bean_def in self._bean_defs]
        duplicate_ids = set([x for x in bean_ids if bean_ids.count(x) > 1])
        if len(duplicate_ids) > 0:
            raise ContextInitError(f'Multiple beans with same id exist: {", ".join(duplicate_ids)}')

        # Add BeanContext itself to beans with an id 'context'
        self._beans._add_as_bean('context', self)
        while any((bean_def.bean_id not in self.beans for bean_def in self._bean_defs)):
            # Get all uninitialized beans
            to_init: List[BeanDef] = list(filter(
                lambda bean_def: bean_def.bean_id not in self.beans,
                self._bean_defs))

            # Remove beans with unsatisfied unary dependencies
            to_init = [bean_def for bean_def in to_init
                       if all((dep_def in self.beans
                               for dep_def in bean_def.dependencies.values()
                               if type(dep_def) is BeanRef))]
            # Remove beans with unsatisfied set dependencies
            to_init = [bean_def for bean_def in to_init
                       if all((self._all_beans_of_class_ready(dep_def.ref)
                               for dep_def in bean_def.dependencies.values()
                               if type(dep_def) is SetBeanRef))]

            if len(to_init) == 0:
                raise ContextInitError(f'Circular or missing dependency was founded')

            for bean_def in to_init:
                bean = bean_def.factory_func(**{arg_name: self.beans[arg_bean_ref]
                                                for (arg_name, arg_bean_ref)
                                                in bean_def.dependencies.items()})
                self.beans._add_as_bean(bean_def.bean_id, bean)

    def close(self):
        for closeable_bean in filter(
                lambda bean: isinstance(bean, CloseableBean),
                self.beans.values()):
            closeable_bean.close_bean()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closed = True
        self.close()

    def _all_beans_of_class_ready(self, cls: Type) -> bool:
        return all((dep_cls_def.bean_id in self.beans for dep_cls_def in self._bean_defs
                    if dep_cls_def.bean_cls is cls))


class BeanContextBuilder:
    def __init__(self):
        self.bean_defs: List[BeanDef] = []
        self.profiles = set()

    def init(self) -> BeanContext:
        ctx = BeanContext(self.bean_defs, self.profiles)
        ctx.init()
        return ctx

    def load_yaml(self, file_path: str) -> None:
        """
        Load configuration from specified file
        @param file_path: YAML config file
        """

        loader = setup_yaml_env_vars(yaml.SafeLoader)

        with open(file_path, 'r', encoding='utf-8') as file:
            conf_raw = yaml.load(file, loader)
            if 'pybeandi' not in conf_raw:
                return
            conf = conf_raw['pybeandi']

            if 'profiles' in conf and 'active' in conf['profiles']:
                for profile in conf['profiles']['active']:
                    self.profiles.add(profile)
            if 'beans' in conf:
                for bean in conf['beans'].items():
                    bean_id, bean_obj = bean
                    self.add_as_bean(bean_id, bean_obj)

    def scan(self, globalns) -> None:
        """
        Scan provided namespace for beans
        @param globalns: result of globals() function
        """
        for cls in (x for x in globalns.values()
                    if (inspect.isclass(x) or callable(x))
                       and '_bean_meta' in vars(x)):
            self.register_bean_by_class(cls)

    def register_bean(self,
                      bean_id: str,
                      bean_cls: Type,
                      factory_func: Callable[..., Any],
                      dependencies: Dict[str, GeneralBeanRef],
                      profile_func: Callable[[Set[str]], bool] = lambda profs: True) -> None:
        """
        Register bean to be created at init phase
        @param bean_id: id of registered bean
        @param bean_cls: class of bean
        @param factory_func: function or class that returns object of bean
        @param dependencies: dictionary of names of factory_func arg to reference to bean
        @param profile_func: function that returns do context need to create bean
        """
        dependencies = {dep_id: (dep_ref if isinstance(dep_ref, BeanRef) else BeanRef(dep_ref))
                        for (dep_id, dep_ref) in dependencies.items()}
        self.bean_defs.append(BeanDef(bean_id, bean_cls, factory_func, dependencies, profile_func))

    def register_bean_by_class(self, cls: Type) -> None:
        """
        Register bean to be created at init phase by class
        Class must be decorated by @bean first!
        @param cls: class of bean
        """
        self.register_bean(
            cls._bean_meta['id'],
            cls,
            cls,
            cls._bean_meta['depends_on'],
            cls._bean_meta['profile_func']
        )

    def add_as_bean(self, bean_id: str, bean_obj: Any):
        self.register_bean(bean_id, type(bean_obj), lambda: bean_obj, {})
