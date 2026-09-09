from app_exceptions.db_exception import DatabaseException
from data_lib.datalib import DataLib


class ItemManager:
    """Item Manager is responsible for managing items in the application."""
    
    @staticmethod
    def item_add(
        title: str, 
        body: str , 
        org_id: int, 
        created_by: int, 
        assigned_to: int, 
        item_state_id: int, 
        priority_id:int, 
        rank:int=0,
    ) -> int:
        item_id: int = -1
        
        query = f"INSERT INTO myio.item (title, body, org_id, item_state_id, created_by, assigned_to, priority_id, rank) VALUES ( '{title}', '{body}', {org_id}, {item_state_id}, {created_by}, {assigned_to}, {priority_id}, {rank}) returning item_id;"
        
        item_id = DataLib.query_return_single_value_in_one(query)
        
        return item_id
    
    @staticmethod
    def item_history_add_by_email(
        item_id: int,
        history_note: str,
        history_by: str = "(system)",
    ):
        query = f"select myio.item_history_add({item_id}, '{history_note}', '{history_by}');"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise DatabaseException(f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}", query)

   
    @staticmethod
    def item_history_add_by_id(
        item_id: int,
        history_note: str,
        history_by: int = -1
    ):
        query = f"select myio.item_history_add_by_id({item_id}, '{history_note}', {history_by});"
        result = DataLib.query_execute_in_one(query)
        if not result:
            raise DatabaseException(f"Failed to add item history for item_id: {item_id} with note: {history_note} by: {history_by}", query)
