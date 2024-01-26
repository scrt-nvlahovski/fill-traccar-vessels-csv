from models.captain import Captain


class Permission:
    def __init__(self):
        self.__id = None
        self.__userId = None
        self.__deviceId = None
        self.__groupId = None
        self.__geofenceId = None
        self.__notificationId = None
        self.__calendarId = None
        self.__attributeId = None
        self.__driverId = None
        self.__managedUserId = None
        self.__commandId = None

    def link_device_captain(self, device, captain: Captain):
        if isinstance(captain, Captain):
            if not isinstance(device, object) and not hasattr(device, "id"):
                if not isinstance(device, dict):
                    raise TypeError("Device must be Dict or Object")
                else:
                    self.__deviceId = device["id"]
            else:
                self.__deviceId = device.id
            self.__driverId = captain.id
        else:
            raise TypeError("Captain must be Captain")


