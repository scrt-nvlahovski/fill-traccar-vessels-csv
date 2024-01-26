class BasePerson:
    def __init__(self):
        self.__id = 0
        self.__name = None
        self.__uniqueId = None
        self.__attributes = {}

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, id: int) -> None:
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = str(value)

    @property
    def uniqueId(self) -> str:
        return self.__uniqueId

    @uniqueId.setter
    def uniqueId(self, value: str) -> None:
        self.__uniqueId = str(value)

    @property
    def attributes(self) -> dict:
        return self.__attributes

    def set(self, attribute: str, value: any) -> None:
        self.__attributes[attribute] = value

    def setAttributes(self, attributes: dict) -> None:
        if isinstance(attributes, dict):
            self.__attributes.update(attributes)
        else:
            raise TypeError

    def get(self, attribute: str) -> any:
        if attribute in self.__attributes:
            return self.__attributes[attribute]

    def getOrDefault(self, attribute: str, default: any) -> any:
        if attribute in self.__attributes:
            return self.__attributes[attribute]
        else:
            return default

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uniqueId": self.uniqueId,
            "name": self.name,
            "attributes": self.attributes
        }
