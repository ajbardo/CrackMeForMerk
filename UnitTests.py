import time
import unittest
import main
from datetime import datetime

class TestCase_1(unittest.TestCase):
    def test_MERKFlagTokenAndTimeSlot_newtoken(self):
        # Testing generation of a new token
        token1 = main.MERKFlagTokenAndTimeSlot()
        time.sleep(token1[0]+1)
        token2 = main.MERKFlagTokenAndTimeSlot()
        self.assertEqual(token2[3], token1[1])  # add assertion here

    def test_MERKFlagTokenAndTimeSlot_sameToken(self):
        #Testing generation of same token
        token1 = main.MERKFlagTokenAndTimeSlot()
        token2 = main.MERKFlagTokenAndTimeSlot()
        self.assertEqual(token2[1], token1[1])

    def test_MERKFlagTokenAndTimeSlot_tokenSecuence(self):
        #testing long secuence of tokens
        for sec in range(0,3):
            token1 = main.MERKFlagTokenAndTimeSlot()
            time.sleep(token1[0]+1)
            token2 = main.MERKFlagTokenAndTimeSlot()
            self.assertEqual(token2[3], token1[1],)  #the old token2 has to be the same as the new token1

    def test_MERKgenTimeFlag_sameTimeLapse(self):
        tested = 0
        count = 0
        while tested == 0 and count < 10:
            count += 1
            tf1 = main.MERKgenTimeFlag()
            old_now = datetime.now()
            tf2 = main.MERKgenTimeFlag()
            new_now = datetime.now()
            if old_now == new_now:
                tested = 1
                self.assertEqual(tf1, tf2)

    def test_MERKgenTimeFlag_differentTimeLapse(self):
        tested = 0
        count = 0
        while tested == 0 and count < 10:
            tf1 = main.MERKgenTimeFlag()
            old_now = datetime.now()
            time.sleep(1)
            tf2 = main.MERKgenTimeFlag()
            new_now = datetime.now()
            if old_now != new_now:
                tested = 1
                self.assertNotEquals(tf1, tf2)

    def test_forMERKGetPrivateValue(self):
        old_private_value = main.forMERKGetPrivateValue()
        self.assertEqual(main.private_value, old_private_value)

        time_data = datetime.now().strftime("%M/%S").split("/")
        new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
        to_sleep = abs(main.private_time-new_server_time)
        time.sleep(to_sleep+1)
        new_private_value = main.forMERKGetPrivateValue()
        self.assertNotEqual(old_private_value,new_private_value)


if __name__ == '__main__':
    unittest.main()
