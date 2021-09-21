import time,unittest,main,warnings
from datetime import datetime
from multiprocessing import Process,Manager

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
                self.assertNotEqual(tf1, tf2)

    def test_forMERKGetPrivateValue(self):
        old_private_value = main.forMERKGetPrivateValue()
        self.assertEqual(main.private_value, old_private_value)

        time_data = datetime.now().strftime("%M/%S").split("/")
        new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
        to_sleep = abs(main.private_time-new_server_time)
        time.sleep(to_sleep+1)
        new_private_value = main.forMERKGetPrivateValue()
        self.assertNotEqual(old_private_value,new_private_value)

    def test_MERKcifValue(self):
        expected = [101, 99, 104, 111, 32, 106, 101, 106, 101]
        for token in range(0,10):
            command_data = main.MERKcifValue("echo jeje",token).split(",")
            for pos in range(0,len(command_data)):
                self.assertEqual(expected[pos]+token, int(command_data[pos]),token)


    def test_MERKcifResultValue(self):
        data = "this is a random string:)"
        for token in range(0,10):
            cif_value = main.MERKcifValue(data, token)
            result_value = main.MERKgetValue(cif_value.split(","),token)
            self.assertEqual(data,result_value)

    def test_forMerkStateMachineClient_DH1(self):
        result = main.forMerkStateMachineClient("DH_1:"+str(main.common_value+4444))
        self.assertEqual(result,"DH_2:"+str(main.private_value+4444))

    def test_forMerkStateMachineClient_DH2(self):
        result = main.forMerkStateMachineClient("DH_2:" + str(1+main.private_value)+","+str(2222+main.private_value)).split("/")[0]
        self.assertEqual(result, "PVT_1:2323,2321,2326,2333,2254,2328,2323,2328,2323")

    def test_forMerkStateMachineClient_PVT_1(self):
        test_string = "test"
        result = main.forMerkStateMachineClient("PVT_1:"+main.MERKcifValue(test_string,2222))
        self.assertEqual(result,main.state_machine_end_mark+test_string)

    def test_forMerkStateMachineServer_DH_1(self):
        result = main.forMerkStateMachineServer("DH_1/"+str(main.MERKgenTimeFlag()[0]))
        self.assertEqual(result, "DH_1:"+str(main.forMERKGetPrivateValue()+main.common_value)+"/"+str(main.MERKgenTimeFlag()[0]))

    def test_forMerkStateMachineServer_DH_2(self):
        client_value = 1111
        result = main.forMerkStateMachineServer("DH_2:"+str(client_value+main.forMERKGetPrivateValue())+"/"+str(main.MERKgenTimeFlag()[0])).split("/")[0]
        self.assertEqual(result, "DH_2:"+str(client_value+main.MERKFlagTokenAndTimeSlot()[0])+","+str(client_value+main.MERKFlagTokenAndTimeSlot()[1]))


    def test_forMerkStateMachineServer_PVT_1(self):
        #warnings.simplefilter("ignore")
        command = "echo jeje"
        expected_result = "jeje\n"
        main.MERKFlagTokenAndTimeSlot()
        time.sleep(5)
        main.MERKFlagTokenAndTimeSlot()
        command_data = main.MERKcifValue(command, main.new_token)
        result = main.forMerkStateMachineServer("PVT_1:"+command_data+"/"+ str(main.MERKgenTimeFlag()[0])).split("/")[0]
        self.assertEqual(expected_result,main.MERKgetValue(result.split("PVT_1:")[1].split(","),main.new_token))

if __name__ == '__main__':

    unittest.main()
