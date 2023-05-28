

from gate_ways.log import Log
from sqlalchemy import   exc ,func
from entities.entity import Base , OrderEntity , StrategyEntity , AccountEntity
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
    

    def getAllByStrategyId(self, session , strategy_id):
        orders = session.query(OrderEntity).filter_by(strategy_id=strategy_id).order_by(OrderEntity.reception_date.desc()).all()
        return [order.to_domain() for order in orders]


    def getAllByStrategyIdAndUserId(self, session, strategy_id, user_id):
        orders = session.query(OrderEntity).filter(
        OrderEntity.strategy_id == strategy_id,
        OrderEntity.strategy_id.in_(
            session.query(StrategyEntity.webhook_id).filter(
                StrategyEntity.account_id.in_(
                    session.query(StrategyEntity.account_id).filter(
                        StrategyEntity.account_id.in_(
                            session.query(AccountEntity.id).filter(AccountEntity.user_id == user_id)
                        )
                    )
                )
            )
        )
        ).all()
        return [order.to_domain() for order in orders]


    def getTotalOrdersByUserId(self, session, user_id):
        total = session.query(OrderEntity).filter(
        OrderEntity.strategy_id.in_(
            session.query(StrategyEntity.webhook_id).filter(
                StrategyEntity.account_id.in_(
                    session.query(StrategyEntity.account_id).filter(
                        StrategyEntity.account_id.in_(
                            session.query(AccountEntity.id).filter(AccountEntity.user_id == user_id)
                        )
                    )
                )
            )
        )
        ).count()
        return total



    def getTotalBuyOrdersByUserId(self, session, user_id):
        total = session.query(OrderEntity).filter(
            OrderEntity.is_buy == True,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).count()
        return total

    def getTotalSellOrdersByUserId(self, session, user_id):
        total = session.query(OrderEntity).filter(
            OrderEntity.is_buy == False,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).count()
        return total

    def getAverageSellpriceByUserId(self, session, user_id):
        average_sell_price = session.query(func.avg(OrderEntity.execution_price)).filter(
            OrderEntity.is_buy == False,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).scalar()
        return average_sell_price

    def getAverageBuyPriceByUserId(self, session, user_id):
        average_buy_price = session.query(func.avg(OrderEntity.execution_price)).filter(
            OrderEntity.is_buy == True,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).scalar()
        return average_buy_price

    def getTotalSellQuantityByUserId(self, session, user_id):
        total_sell_quantity = session.query(func.sum(OrderEntity.amount)).filter(
            OrderEntity.is_buy == False,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).scalar()
        return total_sell_quantity

    def getTotalBuyQuantityByUserId(self, session, user_id):
        total_buy_quantity = session.query(func.sum(OrderEntity.amount)).filter(
            OrderEntity.is_buy == True,
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(
                                session.query(AccountEntity.id).filter(
                                    AccountEntity.user_id == user_id
                                )
                            )
                        )
                    )
                )
            )
        ).scalar()
        return total_buy_quantity
