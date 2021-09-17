import time
import unittest
import main


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
            self.assertEqual(token2[3], token1[1],(token1,token2))  #the old token2 has to be the same as the new token1

if __name__ == '__main__':
    unittest.main()
