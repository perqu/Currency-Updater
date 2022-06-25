import mysql.connector
import pandas as pd


class ConnectorDB:
    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME) -> None:
        self.host = DB_HOST
        self.port = DB_PORT
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None
        self.curr = None

        self.set_conn()
        self.set_curr()

    def set_conn(self) -> None:
        """
        Creates a connection to the indicated (in init) database\n
        Args:
            None
        Returns:
            None
        """
        if self.conn == None:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                db=self.name,
                user=self.user,
                passwd=self.password,
            )

    def set_curr(self) -> None:
        """
        Sets a cursor from indicated (in init) database\n
        Args:
            None
        Returns:
            None
        """
        if self.curr == None and self.conn != None:
            self.curr = self.conn.cursor(buffered=True)

    def refresh_prices(self, currencies: dict) -> None:
        """
        Refresh prices with provided currencies prices\n
        Args:
            currencies - currencies symbols and prices of type dict
        Returns:
            None
        """
        self.curr.execute("SELECT UnitPrice FROM product")
        prices = [el[0] for el in self.curr]

        for key in currencies.keys():
            try:
                self.curr.execute(f"SELECT UnitPrice{key} FROM product")
            except Exception as e:
                self.curr.execute(
                    f"ALTER TABLE product ADD UnitPrice{key} DECIMAL(10,2) NOT NULL"
                )

        for currency_key, currency_value in currencies.items():
            if currency_value != None:
                for price in prices:
                    price_in_currency = round(price / currency_value, 2)
                    self.curr.execute(
                        f"UPDATE product SET UnitPrice{currency_key} = {price_in_currency} WHERE UnitPrice = {price}"
                    )
            else:
                pass

        self.conn.commit()

    def generate_excel(self, path) -> None:
        """
        Exports database to excel(Excel 2007 and later) file\n
        Args:
            path - excel file path of type str
        Returns:
            None
        """
        sql_query = pd.read_sql_query(
            """SELECT ProductID, DepartmentID, Category, IDSKU, ProductName, Quantity, UnitPrice, UnitPriceUSD, UnitPriceEUR, Ranking, ProductDesc, UnitsInStock, UnitsInOrder FROM mydb.product""",
            self.conn,
        )
        df = pd.DataFrame(sql_query)
        df.to_excel(path, index=False)
