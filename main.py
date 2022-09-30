from sheets_api.parser import Parser as sheet_parser

if __name__ == '__main__':
    is_power_on = True

    while is_power_on:
        try:
            print('* Введите 1 для начала парсинга.')
            print('* Введите 0 для выхода.')
            print('Ввод:')
            option = int(input())
            if option == 0:
                is_power_on = False
            elif option != 1 and option != 0:
                print('Неизвестная опция.')
            elif option == 1:
                sheet_parser.set_connection()
                print('Введите id таблицы:')
                id = str(input())
                titles = sheet_parser.get_sheets(id)
                in_parsing = True
                while in_parsing:
                    print('Список доступных листов:', titles)
                    print('Введите название для получение точной информации:')
                    title = str(input())
                    sheet_parser.get_sheet(id, title)
                    sheet_parser.parse_tasks()

        except ValueError:
            print('Пожалуйста, вводите цифры, а не символы!')
