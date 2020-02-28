import os

from consolemenu import SelectionMenu

from lab1.spiders import BigmirSpider, SokolSpider


def show_start_menu():
    """Entrance point in menu"""
    menu = SelectionMenu([
        'Crawl bigmir.net',
        'Find page from bigmir.net with the smallest number of images',
        'Crawl sokol.ua',
        'Create XHTML table with fridges from sokol.ua'
    ], title="Select a task to do")
    menu.show()

    if menu.is_selected_item_exit():
        print('Bye!')
    else:
        index = menu.selected_option
        (crawl_bigmir, analize_bigmir,
         crawl_sokol, create_xhtml_table)[index]()


def press_enter(msg):
    return input(f'{msg}\nPress ENTER to continue...')


def crawl_bigmir():
    BigmirSpider.run()
    press_enter('bigmir.net was crawled, results are saved to '
                f'{BigmirSpider.get_data_filename()}')
    show_start_menu()


def analize_bigmir():
    url, count = BigmirSpider.analyze()
    press_enter(f'Page with the smallest number of images: {url} ({count} images)')
    show_start_menu()


def crawl_sokol():
    SokolSpider.run()
    press_enter('sokol.ua was crawled, results are saved to '
                f'{SokolSpider.get_data_filename()}')
    show_start_menu()


def create_xhtml_table():
    SokolSpider.create_xhtml_table()
    request = input('XHTML table was created, results are saved to output/table.xhtml\n'
                'Would you like to view it in browser? [y/n]\n')
    if request.lower() == 'y':
        os.system('google-chrome-stable output/table.xhtml')
    show_start_menu()


if __name__ == '__main__':
    show_start_menu()
