import logging
from RestNBP import RestNBP
from ConnectorDB import ConnectorDB

logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)


class Manager:
    def __init__(self, currencies) -> None:
        self.__currencies = currencies
        self.__db = None
        self.__updated = False

    def update_currencies(self) -> bool:
        """
        Updates currencies prices from NBP RestAPI\n
        Args:
            None
        Returns:
            Succeeded of type bool
        """
        logging.info("[UC] Gettinget values from RestNBP...")
        try:
            for key in self.__currencies.keys():
                self.__currencies[key] = RestNBP.get_price(key)
        except Exception as e:
            logging.error(f"Err: {e}")
            return False
        else:
            logging.info("[UC] RestNBP updated currencies successfully")
            self.updated = True
            return True

    def connect_to_db(self) -> bool:
        """
        Creating connection to database\n
        Args:
            None
        Returns:
            Succeeded of type bool
        """
        logging.info("[DB] Connecting to database...")
        try:
            self.__db = ConnectorDB(
                DB_USER="root",
                DB_PASSWORD="admin",
                DB_HOST="127.0.0.1",
                DB_NAME="mydb",
                DB_PORT="3306",
            )
        except Exception as e:
            logging.error(f"Err: {e}")
            return False
        else:
            logging.info("[DB] DB connection established successfully")
            return True

    def refresh_prices(self) -> None:
        """
        Refresh prices in DB with NBP RestAPI data\n
        Args:
            None
        Returns:
            Succeeded of type bool
        """
        logging.info("[RP] Updating prices for foreign currencies...")

        if (self.__db != None or self.connect_to_db()) and (
            self.__updated != False or self.update_currencies()
        ):
            try:
                self.__db.refresh_prices(self.__currencies)

            except Exception as e:
                logging.error(f"Err: {e}")
            else:
                logging.info("[RP] Prices refreshed successfully")
        else:
            logging.info("[RP] Cannot refresh prices due to previous errors")

    def generate_excel(self, path="exported_data.xlsx") -> None:
        """
        Exports database to excel(Excel 2007 and later)\n
        Args:
            path (Optional) - excel file path of type str
        Returns:
            None
        """
        logging.info("[GE] Generating excel from database...")
        if self.__db != None or self.connect_to_db():
            try:
                self.__db.generate_excel(path)
            except Exception as e:
                logging.error(f"Err: {e}")
            else:
                logging.info("[GE] Excel generated successfully")
        else:
            logging.info("[GE] Cannot generate excel due to previous errors")
