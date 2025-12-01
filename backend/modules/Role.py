class Role:
    __roleList = ['ADMIN','PATIENT','DOCTOR']
    
    def __init__(self, role):
        self.__role = role


    @staticmethod
    def create(role):
        if(role not in Role.__roleList):
            raise ValueError("Role value not in supported list -> ",Role.__roleList) 

        return Role(role)

    def getRole(self):
        return self.__role
