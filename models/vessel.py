from helpers.common import validate_phone_number


class Vessel:

    def __init__(self):
        self.__id = 0
        self.__name = ""
        self.__uniqueId = ""
        self.__status = ""
        self.__disabled = False
        self.__lastUpdate = ""
        self.__positionId = 0
        self.__groupId = 0
        self.__phone = ""
        self.__model = ""
        self.__contact = ""
        self.__category = ""
        self.__attributes = {}

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        self.__id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def uniqueId(self):
        return self.__uniqueId

    @uniqueId.setter
    def uniqueId(self, value: str) -> None:
        self.__uniqueId = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        self.__status = value

    @property
    def disabled(self):
        return self.__disabled

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.__disabled = value

    @property
    def lastUpdate(self):
        return self.__lastUpdate

    @lastUpdate.setter
    def lastUpdate(self, value: str) -> None:
        self.__lastUpdate = value

    @property
    def positionId(self):
        return self.__positionId

    @positionId.setter
    def positionId(self, value: int) -> None:
        self.__positionId = value

    @property
    def groupId(self):
        return self.__groupId

    @groupId.setter
    def groupId(self, value: int) -> None:
        self.__groupId = value

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = validate_phone_number(value)

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value: str) -> None:
        self.__model = value

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, value: str) -> None:
        self.__category = value

    @property
    def contact(self):
        return self.__contact

    @contact.setter
    def contact(self, value: str) -> None:
        self.__contact = value

    @property
    def attributes(self) -> dict:
        return self.__attributes

    def set(self, attribute: str, value: any) -> None:
        self.__attributes[attribute] = value

    def get(self, attribute: str) -> any:
        if attribute in self.__attributes:
            return self.__attributes[attribute]

    def get_or_default(self, attribute: str, default: any) -> any:
        if attribute in self.__attributes:
            return self.__attributes[attribute]
        else:
            return default

    def set_attributes(self, attributes: dict) -> None:
        if isinstance(attributes, dict):
            self.__attributes.update(attributes)
        else:
            raise TypeError

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "uniqueId": self.uniqueId,
            "name": self.name,
            "status": self.status,
            "disabled": self.disabled,
            "lastUpdate": self.lastUpdate,
            "positionId": str(self.positionId),
            "category": str(self.category),
            "contact": str(self.contact),
            "groupId": str(self.groupId),
            "model": str(self.model),
            "phone": str(self.phone),
            "attributes": self.attributes
        }
