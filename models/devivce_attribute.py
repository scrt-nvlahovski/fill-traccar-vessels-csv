class DeviceAttribute:
    __cfr = None
    __idp = None
    __ip = None
    __ext = None
    __length = None
    __width = None
    __call_sign = None
    __mmsi = None
    __owner = None
    __company_address = None
    __email = None
    __captain = None
    __contact_phone = None
    __deep = None
    __gt = None
    __fvms = None
    __name = None
    __cyr_name = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def cyr_name(self):
        return self.__cyr_name

    @cyr_name.setter
    def cyr_name(self, value):
        self.__cyr_name = value

    @property
    def fvms(self):
        return self.__fvms

    @fvms.setter
    def fvms(self, value):
        self.__fvms = value

    @property
    def deep(self):
        return self.__deep

    @deep.setter
    def deep(self, value):
        self.__deep = value

    @property
    def gt(self):
        return self.__gt

    @gt.setter
    def gt(self, value):
        self.__gt = value

    @property
    def captain(self):
        return self.__captain

    @captain.setter
    def captain(self, value):
        self.__captain = value

    @property
    def ext(self):
        return self.__ext

    @ext.setter
    def ext(self, value):
        self.__ext = value

    @property
    def cfr(self):
        return self.__cfr

    @cfr.setter
    def cfr(self, value):
        self.__cfr = value

    @property
    def contact_phone(self):
        return self.__contact_phone

    @contact_phone.setter
    def contact_phone(self, value):
        self.__contact_phone = value

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def idp(self):
        return self.__idp

    @idp.setter
    def idp(self, value):
        self.__idp = value

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        self.__email = value

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value

    @property
    def company_address(self):
        return self.__company_address

    @company_address.setter
    def company_address(self, value):
        self.__company_address = value

    @property
    def call_sign(self):
        return self.__call_sign

    @call_sign.setter
    def call_sign(self, value):
        self.__call_sign = value

    @property
    def mmsi(self):
        return self.__mmsi

    @mmsi.setter
    def mmsi(self, value):
        self.__mmsi = value

    def to_dict(self):
        return {
            'cfr': self.cfr,
            'idp': self.idp,
            'ip': self.ip,
            'ext': self.ext,
            'name': self.name,
            'cyr_name': self.cyr_name,
            'length': self.length,
            'width': self.width,
            'call_sign': self.call_sign,
            'mmsi': self.mmsi,
            'owner': self.owner,
            'company_address': self.company_address,
            'email': self.email,
            'captain': self.captain,
            'contact_phone': self.contact_phone,
            'deep': self.deep,
            'gt': self.gt,
            'fvms': self.fvms
        }
