

from gate_ways.log import Log
from entities.entity import Base , AdminEntity 
import uuid
from sqlalchemy import   exc


logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , admin):
        adminEntity = AdminEntity()
        adminEntity.from_domain(model=admin)
        adminEntity.id=str(uuid.uuid4())
        
        session.add(adminEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("admin not saved")
         
        return adminEntity.to_domain()

    def getAdminByLogin(self, session , login):
        admin = session.query(AdminEntity).filter(AdminEntity.login == login).first()
        return None if admin == None else admin.to_domain()
    
    def getAdminById(self, session , uuid):
        admin = session.query(AdminEntity).filter(AdminEntity.id == uuid).first()
        return None if admin == None else admin.to_domain()
    
    def getAdminByIdAndLoginAndPrivilege(self, session, admin_id, login , privilege):
        admin = session.query(AdminEntity).filter(AdminEntity.id == admin_id, AdminEntity.login == login , AdminEntity.privilege == privilege).first()
        return None if admin is None else admin.to_domain()

    
