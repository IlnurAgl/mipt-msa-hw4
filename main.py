from converters.currency_converter import Converter


def main():    
    amount = int(input('Введите значение в USD: \n'))

    converter = Converter(amount)
    for currency in ['RUB', 'EUR', 'GBP', 'CNY']:
        print(f'Значение в {currency}: {converter.convert(currency)}')


if __name__ == "__main__":
    main()
