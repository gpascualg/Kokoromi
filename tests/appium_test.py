import random
import time
from lib.utils.appium_test import AppiumTest

class TestSomeApp(AppiumTest):
    def test_sth(self):
        self.screenshots.append("https://user-images.githubusercontent.com/15132522/157759298-d482a5ee-887a-4e26-8584-2b892856f95f.png")
        self.screenshots.append("https://wanderlog.com/assets/logo.png")
        self.screenshots.append("https://www.cirquedusoleil.com/-/media/cds/images/shows/luzia/2022/luzia_thumb_454x454.jpg?db=web&h=454&vs=2&w=454&sc_lang=es&hash=CB4CC2A1DEE6AC5277EB8C5891F3CE43")
        self.screenshots.append("https://www.cirquedusoleil.com/-/media/cds/images/b2c/offertypes/regular_ticket_luzia_332x170.jpg?db=web&h=170&vs=1&w=332&hash=78171105026F899EED9E7AF8D2782633")
        assert random.randrange(0, 2) == 1

    def test_sth_else(self):
        time.sleep(1 + random.random())
        assert random.randrange(0, 2) == 1
