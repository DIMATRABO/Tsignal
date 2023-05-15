

from gate_ways.log import Log
from sqlalchemy import  and_ , exc
from entities.entity import Base , OrderEntity 
from models.model import Order
import uuid


logger = Log()
class SqlAlchimy_repo :
    def __init__(self ):
        self.Base = Base

        
    def save(self, session , order:Order):
        orderEntity = OrderEntity()
        
        orderEntity.from_domain(model=order)
        orderEntity.id=str(uuid.uuid4())
        
        session.add(orderEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("order not saved")
         
        return orderEntity.to_domain()
        


    def update(self, session , order:Order):
        orderEntity = OrderEntity()
        orderEntity.from_domain(model=order)
        
        session.merge(orderEntity)
        try:        
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("order not updated")
         
      
    
    def delete(self, session , order):
        num_deleted = session.query(OrderEntity).filter_by(id=order.id).delete()
        if num_deleted == 0:
            # handle case where no matching records were found
            raise Exception("No matching records found for order ID {}".format(order.id))

        try:
            session.commit()
        except exc.SQLAlchemyError as e:
            logger.log(e)
            session.rollback()
            raise Exception("Error deleting order with ID {}".format(order.id))
            
    

    def getAllOrders(self, session):
        orders = session.query("orders")
        return orders


    def getOrderById(self, session , uuid):
        order = session.query(OrderEntity).filter(OrderEntity.id == uuid).first()
        return None if order == None else order.to_domain()
    
 