# NoQueryBuilderRepositoryMixin

`from framework.repository import NoQueryBuilderRepositoryMixin`

Миксин для репозиториев, с методами конвертации

***

# ABSRepository

`from framework.repository import ABSRepository`

Миксин для репозиториев, с методами конвертации

***

## Functions

#### \_\_init\_\_

**`ABSRepository(session)`**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| session |  ISessionTypeVar |  | Актуально для некоторых типов хранилищ или ORM |

#### exists

**`self.exists(filter_params)`**

Проверка на существование записей в хранилище
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| filter_params |  Optional[ABSQueryObject] |  | Настроенные параметры фильтрации |

_Returns:_  Булево значение true или false

#### count

**`self.count()`**

**`self.count(filter_params=None)`**

Подсчет количества объектов в хранилище
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| filter_params |  Optional[ABSQueryObject] | None | Настроенные параметры фильтрации |

_Returns:_  Количество объектов в хранилище

#### fetch_one

**`self.fetch_one()`**

**`self.fetch_one(filter_params=None, order_params=None, raise_if_empty=True)`**

Получить один элемент из хранилища
:raise NotFoundException:
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| filter_params |  Optional[ABSQueryObject] | None | Параметры фильтрации для выборки |
| order_params |  Optional[ABSOrderObject] | None | Параметры сортировки последовательности элементов |
| raise_if_empty |  bool  | True | Бросать ли исключение, если ни одного объекта не найдено |

_Returns:_  Один элемент

#### fetch_many

**`self.fetch_many()`**

**`self.fetch_many(filter_params=None, order_params=None, offset=0, limit=None, chunk_size=1000)`**

Получить несколько элементов из хранилища
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| filter_params |  Optional[ABSQueryObject] | None | Параметры фильтрации для выборки |
| order_params |  Optional[ABSOrderObject] | None | Параметры сортировки последовательности элементов |
| offset |  int  | 0 | Смещение относительно начала элементов |
| limit |  Optional[int] | None | Количество элементов в выборке |
| chunk_size |  int  | 1000 | Какое количество элементов за раз выбирать из хранилища |

_Returns:_  Генератор отдающий по одному значению

#### add

**`self.add(domain_model)`**

Сохранить один элемент в хранилище
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| domain_model |  EntityTypeVar |  | Объект, на основе которого будет создана запись в хранилище |

_Returns:_  Ничего не возвращает, потому что не все хранилища поддерживают RETURNING

#### add_many

**`self.add_many(domain_model_sequence)`**

Добавить несколько записей в хранилище
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| domain_model_sequence |  Iterable[EntityTypeVar] |  | Список сущностей, на основе которыхз будут созданы записи в базе |

#### update_one

**`self.update_one(domain_model)`**

Обновить одну запись
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| domain_model |  EntityTypeVar |  | Объект, запись на основе которого нужно обновить |

_Returns:_  Ничего не возвращает, потому что не все хранилища поддерживают RETURNING

#### update_many

**`self.update_many(domain_model)`**

Обновить несколько записей в хранилище
| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| domain_model |  Iterable[EntityTypeVar] |  | :param domain_model: |

_Returns:_  Ничего не возвращает, потому что не все хранилища поддерживают RETURNING

