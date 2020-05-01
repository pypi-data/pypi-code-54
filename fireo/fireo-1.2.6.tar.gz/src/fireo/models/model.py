from fireo import fields
from fireo.managers.managers import Manager
from fireo.models.errors import AbstractNotInstantiate
from fireo.models.model_meta import ModelMeta
from fireo.queries.errors import InvalidKey
from fireo.utils import utils


class Model(metaclass=ModelMeta):
    """Provide easy way to handle firestore features

    Model is used to handle firestore operation easily and provide additional features for best
    user experience.

    Example
    -------
    .. code-block:: python

        class User(Model):
            username = TextField(required=True)
            full_name = TextField()
            age = NumberField()

        user = User()
        user.username = "Axeem"
        user.full_name = "Azeem Haider"
        user.age = 25
        user.save()

        # or you can also pass args into constructor
        user = User(username="Axeem", full_name="Azeem", age=25)
        user.save()

        # or you can use it via managers
        user = User.collection.create(username="Axeem", full_name="Azeem", age=25)

    Attributes
    ----------
    _meta : Meta
        Hold all model information like model fields, id, manager etc

    id : str
        Model id if user specify any otherwise it will create automatically from firestore
        and attached with this model

    key : str
        Model key which contain the model collection name and model id and parent if provided, Id can be user defined
        or generated from firestore

    _update_doc: str
        Update doc hold the key which is used to update the document

    parent: str
        Parent key if user specify

    collection_name : str
        Model name which is saved in firestore if user not specify any then Model class will convert
        automatically in collection name

        For example: UserProfile will be user_profile

    collection : Manager
        Class level attribute through this you can access manager which can be used to save, retrieve or
        update the model in firestore

        Example:
        -------
        .. code-block:: python
            class User(Model):
                name = TextField()

            user = User.collection.create(name="Azeem")

    Methods
    --------
    _get_fields() : dict
        Private method that return values of all attached fields.

    save() : Model instance
        Save the model in firestore collection

    update(doc_key, transaction) : Model instance
        Update the existing document, doc_key optional can be set explicitly

    _set_key(doc_id):
        Set the model key

    Raises
    ------
    AbstractNotInstantiate:
        Abstract model can not instantiate
    """
    # Id of the model specify by user or auto generated by firestore
    # It can be None if user changed the name of id field it is possible
    # to call it from different name e.g user_id
    id = None

    # Private for internal user but there is key property which hold the
    # current document id and collection name and parent if any
    _key = None

    # For sub collection there must be a parent
    parent = ""

    # Hold all the information about the model fields
    _meta = None

    # This is for manager
    collection: Manager = None

    # Collection name for this model
    collection_name = None

    # Track which fields are changed or not
    # it is useful when updating document
    _field_list = []
    _field_changed = []

    # check instance is modified or not
    # When you get the document from firestore or
    # save the document then the model instance changed
    # This also give the help to track update fields
    _instance_modified = False

    # Update doc hold the key which is used to update the document
    _update_doc = None

    def __init__(self, *args, **kwargs):
        # check this is not abstract model otherwise stop creating instance of this model
        if self._meta.abstract:
            raise AbstractNotInstantiate(f'Can not instantiate abstract model "{self.__class__.__name__}"')

        # Allow users to set fields values direct from the constructor method
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Create instance for nested model
        # for direct assignment to nested model
        for f in self._meta.field_list.values():
            if isinstance(f, fields.NestedModel):
                if f.name in kwargs:
                    setattr(self, f.name, f.nested_model.from_dict(kwargs[f.name]))
                else:
                    setattr(self, f.name, f.nested_model())

    @classmethod
    def from_dict(cls, model_dict):
        """Instantiate model from dict"""
        return cls(**model_dict)

    def to_dict(self):
        """Convert model into dict"""
        model_dict = self._get_fields()
        id = 'id'
        if self._meta.id is not None:
            id, _ = self._meta.id
        model_dict[id] = utils.get_id(self.key)
        model_dict['key'] = self.key
        return model_dict

    # Get all the fields values from meta
    # which are attached with this mode
    # and convert them into corresponding db value
    # return dict {name: value}
    def _get_fields(self):
        """Get Model fields and values

        Retrieve all fields which are attached with Model from `_meta`
        then get corresponding value from model

        Example
        -------
        .. code-block:: python

            class User(Model):
                name = TextField()
                age = NumberField()

            user = User()
            user.name = "Azeem"
            user.age = 25

            # if you call this method `_get_field()` it will return dict{name, val}
            # in this case it will be
            {name: "Azeem", age: 25}

        Returns
        -------
        dict:
            name value dict of model
        """
        field_list = {}
        for f in self._meta.field_list.values():
            if isinstance(f, fields.NestedModel):
                model_instance = getattr(self, f.name)
                if f.valid_model(model_instance):
                    field_list[f.name] = model_instance._get_fields()
            else:
                field_list[f.name] = getattr(self, f.name)
        return field_list

    @property
    def _id(self):
        """Get Model id

        User can specify model id otherwise it will return None and generate later from
        firestore and attached to model

        Example
        --------
        .. code-block:: python
            class User(Mode):
                user_id = IDField()

            u = User()
            u.user_id = "custom_doc_id"

            # If you call this property it will return user defined id in this case
            print(self._id)  # custom_doc_id

        Returns
        -------
        id : str or None
            User defined id or None
        """
        if self._meta.id is None:
            return None
        name, field = self._meta.id
        return field.get_value(getattr(self, name))

    @_id.setter
    def _id(self, doc_id):
        """Set Model id

        Set user defined id to model otherwise auto generate from firestore and attach
        it to with model

        Example:
        --------
            class User(Model):
                user_id = IDField()
                name = TextField()

            u = User()
            u.name = "Azeem"
            u.save()

            # User not specify any id it will auto generate from firestore
            print(u.user_id)  # xJuythTsfLs

        Parameters
        ----------
        doc_id : str
            Id of the model user specified or auto generated from firestore
        """
        id = 'id'
        if self._meta.id is not None:
            id, _ = self._meta.id
        setattr(self, id, doc_id)
        # Doc id can be None when user create Model directly from manager
        # For Example:
        #   User.collection.create(name="Azeem")
        # in this any empty doc id send just for setup things
        if doc_id:
            self._set_key(doc_id)

    @property
    def key(self):
        if self._key:
            return self._key
        try:
            k = '/'.join([self.parent, self.collection_name, self._id])
        except TypeError:
            k = '/'.join([self.parent, self.collection_name, '@temp_doc_id'])
        if k[0] == '/':
            return k[1:]
        else:
            return k

    def _set_key(self, doc_id):
        """Set key for model"""
        p = '/'.join([self.parent, self.collection_name, doc_id])
        if p[0] == '/':
            self._key = p[1:]
        else:
            self._key = p

    def get_firestore_create_time(self):
        """returns create time of document in Firestore

        Returns:
            :class:`google.api_core.datetime_helpers.DatetimeWithNanoseconds`,
            :class:`datetime.datetime` or ``NoneType``:
        """
        return self._meta._firestore_create_time

    def get_firestore_update_time(self):
        """returns update time of document in Firestore

        Returns:
            :class:`google.api_core.datetime_helpers.DatetimeWithNanoseconds`,
            :class:`datetime.datetime` or ``NoneType``:
        """
        return self._meta._firestore_update_time

    def list_subcollections(self):
        """return a list of any subcollections of the doc"""
        if self._meta._referenceDoc is not None:
            return [ c.id for c in self._meta._referenceDoc.collections() ]

    def save(self, transaction=None, batch=None):
        """Save Model in firestore collection

        Model classes can saved in firestore using this method

        Example
        -------
        .. code-block:: python
            class User(Model):
                name = TextField()
                age = NumberField()

            u = User(name="Azeem", age=25)
            u.save()

            # print model id
            print(u.id) #  xJuythTsfLs

        Same thing can be achieved from using managers

        See Also
        --------
        fireo.managers.Manager()

        Returns
        -------
        model instance:
            Modified instance of the model contains id etc
        """
        # pass the model instance if want change in it after save, fetch etc operations
        # otherwise it will return new model instance
        return self.__class__.collection.create(self, transaction, batch, **self._get_fields())

    def update(self, key=None, transaction=None, batch=None):
        """Update the existing document

        Update document without overriding it. You can update selected fields.

        Examples
        --------
        .. code-block:: python
            class User(Model):
                name = TextField()
                age = NumberField()

            u = User.collection.create(name="Azeem", age=25)
            id = u.id

            # update this
            user = User.collection.get(id)
            user.name = "Arfan"
            user.update()

            print(user.name)  # Arfan
            print(user.age)  # 25

        Parameters
        ----------
        key: str
            Key of document which is going to update this is optional you can also set
            the update_doc explicitly

        transaction:
            Firestore transaction

        batch:
            Firestore batch writes
        """

        # Check doc key is given or not
        if key:
            self._update_doc = key

        # make sure update doc in not None
        if self._update_doc is not None and '@temp_doc_id' not in self._update_doc:
            # set parent doc from this updated document key
            self.parent = utils.get_parent_doc(self._update_doc)
            # Get id from key and set it for model
            setattr(self, '_id', utils.get_id(self._update_doc))
            # Add the temp id field if user is not specified any
            if self._id is None and self.id:
                setattr(self._meta, 'id', ('id', fields.IDField()))
        elif self._update_doc is None and '@temp_doc_id' in self.key:
            raise InvalidKey(f'Invalid key to update model "{self.__class__.__name__}" ')

        # Get the updated fields
        updated_fields = {}
        for k, v in self._get_fields().items():
            if k in self._field_changed:
                updated_fields[k] = v
            # Get nested fields if any
            # Nested model store as dict in firestore so check values type is dict
            if type(v) is dict:
                # nested field name and value
                for name, value in v.items():
                    if name in self._field_changed:
                        # create the name with parent field name and child name
                        # For example:
                        #   class User(Model):
                        #       address = TextField()
                        #   class Student(Model):
                        #       age = NumberField()
                        #       user = NestedModel(User)
                        #
                        # Then the field name for nested model will be "user.address"
                        updated_fields[k+"."+name] = value
        # pass the model instance if want change in it after save, fetch etc operations
        # otherwise it will return new model instance
        return self.__class__.collection._update(self, transaction=transaction, batch=batch, **updated_fields)

    def __setattr__(self, key, value):
        """Keep track which filed values are changed"""
        if key in self._field_list or not self._instance_modified:
            self._field_changed.append(key)
        else:
            self._field_list.append(key)
        super(Model, self).__setattr__(key, value)
