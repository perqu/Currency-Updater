from Manager import Manager


def main():
    # In case of new currency - add proper symbol from NBP Rest API at the end of the dict
    currencies = {"USD": None, "EUR": None}
    mng = Manager(currencies)
    mng.refresh_prices()
    mng.generate_excel()


if __name__ == "__main__":
    main()
