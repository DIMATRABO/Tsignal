

from gate_ways.log import Log
from forms.order.ordersPaginated import OrdersPage
from sqlalchemy import   exc ,func ,extract
from entities.entity import Base , OrderEntity , StrategyEntity , AccountEntity
from models.model import Order 
import uuid
from datetime import datetime, timedelta
from typing import List, Tuple



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
        ).order_by(OrderEntity.reception_date.desc()).all()
        return [order.to_domain() for order in orders]
    

    def getAllByUserId(self, session, user_id):
        orders = session.query(OrderEntity).filter(
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
        ).order_by(OrderEntity.reception_date.desc()).all()
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

  


    def getAverageBuyPriceByUserId(self, session, user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount) / func.sum(OrderEntity.amount))
            .filter(
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price




    def getAverageSellPriceByUserId(self, session, user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount) / func.sum(OrderEntity.amount))
            .filter(
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price



    def getTotalSellQuantityByUserId(self, session, user_id):
        total_sell_quantity = session.query(func.sum(OrderEntity.amount)).filter(
            OrderEntity.is_buy == False,
            OrderEntity.status == "closed",
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
            OrderEntity.status == "closed",
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
    

    def getTotalFailedOrdersByUserId(self, session, user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        total_failed = session.query(OrderEntity).filter(
                OrderEntity.status == 'failed',
                OrderEntity.strategy_id.in_(subquery_2)
            ).count()
        return total_failed

    

    def getTotalInvistedByUser(self, session , user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price
    

    def getTotalIncomeByUser(self, session , user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price


    def getTotalIncomeByMonthByUser(self, session, user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        current_year = datetime.now().year

        monthly_profits = (
            session.query(
                extract('month', OrderEntity.execution_date),
                func.sum(OrderEntity.execution_price * OrderEntity.amount)
            )
            .filter(
                not OrderEntity.execution_price is None,
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                extract('year', OrderEntity.execution_date) == current_year
            )
            .group_by(extract('month', OrderEntity.execution_date))
            .all()
        )

        logger.log(monthly_profits)


        # Initialize list with 12 elements representing each month of the year
        monthly_income = [0] * 12
        
        for month_decimal, profit in monthly_profits:
            # Convert Decimal month to integer for indexing
            month_index = int(month_decimal)

            # Assign the profit to the corresponding month index
            if profit is None:
                 monthly_income[month_index - 1] = 0
            else:
                monthly_income[month_index - 1] = float(profit)
        return monthly_income
    


    def getTotalInvestedByMonthByUser(self, session, user_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        current_year = datetime.now().year

        monthly_invested = (
            session.query(
                extract('month', OrderEntity.execution_date),
                func.sum(OrderEntity.execution_price * OrderEntity.amount)
            )
            .filter(
                not OrderEntity.execution_price is None,
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                extract('year', OrderEntity.execution_date) == current_year
            )
            .group_by(extract('month', OrderEntity.execution_date))
            .all()
        )
        logger.log(monthly_invested)
        monthly_investeds = [0] * 12
        
        for month_decimal, invested in monthly_invested:
            month_index = int(month_decimal)
            if invested is None:
                 monthly_investeds[month_index - 1] = 0
            else:
                monthly_investeds[month_index - 1] = float(invested)
        return monthly_investeds
    


    def get_total_trades_by_strategy(self, session, user_id) -> List[Tuple[str, int]]:
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )
       

        trades_by_strategy = (
            session.query(
                StrategyEntity.name,
                func.count(OrderEntity.id)
            )
            .join(OrderEntity, StrategyEntity.webhook_id == OrderEntity.strategy_id)
            .filter(
                    OrderEntity.status == 'closed',
                    OrderEntity.strategy_id.in_(subquery_2)
                    )
            .group_by(StrategyEntity.name)
            .all()
        )        
        # Convert the result to a list of tuples
        total_trades_by_strategy = [(name, count) for name, count in trades_by_strategy]
        
        return total_trades_by_strategy



##############################################################




    def getTotalOrdersByStrategyAndUserId(self, session, user_id , strategy_id):
        total = session.query(OrderEntity).filter(
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
        ).count()
        return total



    def getTotalBuyOrdersByStrategyAndUserId(self, session, user_id , strategy_id):
        total = session.query(OrderEntity).filter(
            OrderEntity.strategy_id == strategy_id,
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

    def getTotalSellOrdersByStrategyAndUserId(self, session, user_id , strategy_id):
        total = session.query(OrderEntity).filter(
            OrderEntity.strategy_id == strategy_id,
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

  


    def getAverageBuyPriceByStrategyAndUserId(self, session, user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount) / func.sum(OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price




    def getAverageSellPriceByStrategyAndUserId(self, session, user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount) / func.sum(OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price



    def getTotalSellQuantityByStrategyAndUserId(self, session, user_id , strategy_id):
        total_sell_quantity = session.query(func.sum(OrderEntity.amount)).filter(
            OrderEntity.strategy_id == strategy_id,
            OrderEntity.is_buy == False,
            OrderEntity.status == "closed",
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

    def getTotalBuyQuantityByStrategyAndUserId(self, session, user_id , strategy_id):
        total_buy_quantity = session.query(func.sum(OrderEntity.amount)).filter(
            OrderEntity.strategy_id == strategy_id,
            OrderEntity.is_buy == True,
            OrderEntity.status == "closed",
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
    

    def getTotalFailedOrdersByStrategyAndUserId(self, session, user_id , strategy_id):
        total_failed = session.query(OrderEntity).filter(
            OrderEntity.strategy_id == strategy_id,
            OrderEntity.status == "failed",
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
        return total_failed

    

    def getTotalInvistedByStrategyAndUser(self, session , user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price
    

    def getTotalIncomeByStrategyAndUser(self, session , user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        average_buy_price = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .scalar()
        )

        return average_buy_price


    def getTotalIncomeByMonthByStrategyAndUser(self, session, user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        current_year = datetime.now().year

        monthly_profits = (
            session.query(
                extract('month', OrderEntity.execution_date),
                func.sum(OrderEntity.execution_price * OrderEntity.amount)
            )
            .filter(
                not OrderEntity.execution_price is None,
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                extract('year', OrderEntity.execution_date) == current_year
            )
            .group_by(extract('month', OrderEntity.execution_date))
            .all()
        )
        logger.log(monthly_profits)

        # Initialize list with 12 elements representing each month of the year
        monthly_income = [0] * 12
        
        for month_decimal, profit in monthly_profits:
            # Convert Decimal month to integer for indexing
            month_index = int(month_decimal)

            # Assign the profit to the corresponding month index
            if profit is None:
                 monthly_income[month_index - 1] = 0
            else:
                monthly_income[month_index - 1] = float(profit)
        return monthly_income
    


    def getTotalInvestedByMonthByStrategyAndUser(self, session, user_id , strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        current_year = datetime.now().year

        monthly_invested = (
            session.query(
                extract('month', OrderEntity.execution_date),
                func.sum(OrderEntity.execution_price * OrderEntity.amount)
            )
            .filter(
                not OrderEntity.execution_price is None,
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                extract('year', OrderEntity.execution_date) == current_year
            )
            .group_by(extract('month', OrderEntity.execution_date))
            .all()
        )
        logger.log(monthly_invested)


        monthly_investeds = [0] * 12
        
        for month_decimal, invested in monthly_invested:
            month_index = int(month_decimal)
            if invested is None:
                 monthly_investeds[month_index - 1] = 0
            else:
                monthly_investeds[month_index - 1] = float(invested )
        return monthly_investeds
    


    def get_total_trades_by_pair(self, session, user_id, strategy_id) -> List[Tuple[str, int]]:
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        trades_by_pair = (
            session.query(
                OrderEntity.symbol,
                func.count(OrderEntity.id)
            )
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2)
            )
            .group_by(OrderEntity.symbol)
            .all()
        )

        # Convert the result to a list of tuples
        total_trades_by_pair = [(name, count) for name, count in trades_by_pair]

        return total_trades_by_pair



    
    def getTotalOrdersByStrategyAndUserIdLast7Days(self, session, user_id , strategy_id):
        seven_days_ago = datetime.now() - timedelta(days=7)

        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        total = session.query(OrderEntity).filter(
            OrderEntity.strategy_id == strategy_id,
            OrderEntity.execution_date >= seven_days_ago,  # Filter orders within the last 7 days
            OrderEntity.strategy_id.in_(subquery_2)
            ).count()
        
        return total
        

        
    def getTotalIncomeLast7DaysByStrategyAndUser(self, session, user_id, strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        seven_days_ago = datetime.now() - timedelta(days=7)

        total_income = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == False,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                OrderEntity.execution_date >= seven_days_ago
            )
            .scalar()
        )

        return total_income


    def getTotalInvestedLast7DaysByStrategyAndUser(self, session, user_id, strategy_id):
        subquery_1 = (
            session.query(AccountEntity.id)
            .filter(AccountEntity.user_id == user_id)
            .subquery()
        )

        subquery_2 = (
            session.query(StrategyEntity.webhook_id)
            .filter(StrategyEntity.account_id.in_(subquery_1))
            .subquery()
        )

        seven_days_ago = datetime.now() - timedelta(days=7)

        total_invested = (
            session.query(func.sum(OrderEntity.execution_price * OrderEntity.amount))
            .filter(
                OrderEntity.strategy_id == strategy_id,
                OrderEntity.is_buy == True,
                OrderEntity.status == 'closed',
                OrderEntity.strategy_id.in_(subquery_2),
                OrderEntity.execution_date >= seven_days_ago
            )
            .scalar()
        )

        return total_invested
    

    def getAllByStrategyIdAndUserIdPaginated(self, session, strategy_id, user_id, page_number, page_size):
        query = session.query(OrderEntity).filter(
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
        ).order_by(OrderEntity.reception_date.desc())

        total_records = query.count()
        starting_index = (page_number - 1) * page_size
     
        orders = query.offset(starting_index).limit(page_size).all()

        return OrdersPage(
            total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            orders= [order.to_domain() for order in orders]
            )
    


    def getAllByUserIdPaginated(self, session, user_id, page_number, page_size):
        subquery = session.query(AccountEntity.id).filter(AccountEntity.user_id == user_id)

        query = session.query(OrderEntity).filter(
            OrderEntity.strategy_id.in_(
                session.query(StrategyEntity.webhook_id).filter(
                    StrategyEntity.account_id.in_(
                        session.query(StrategyEntity.account_id).filter(
                            StrategyEntity.account_id.in_(subquery)
                        )
                    )
                )
            )
        ).order_by(OrderEntity.reception_date.desc())

        total_records = query.count()
        starting_index = (page_number - 1) * page_size
      
        orders = query.offset(starting_index).limit(page_size).all()
        
        return OrdersPage(
             total_records =  total_records,
            page_number= page_number,
            page_size= page_size,
            orders= [order.to_domain() for order in orders]
            )
