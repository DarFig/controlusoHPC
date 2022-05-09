# -*- coding: utf-8 -*-

from controller import Controller

if __name__ == "__main__":
    new_controller = Controller()

    #print(new_controller.match_all())
    print(new_controller.match_date_range("04/05/2022","05/05/2022"))
