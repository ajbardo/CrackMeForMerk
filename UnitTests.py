import time, unittest, main, warnings
from datetime import datetime


class TestCase1(unittest.TestCase):
    def test_MERKFlagTokenAndTimeSlot_newtoken(self):
        # Testing generation of a new token
        token1 = main.MERKFlagTokenAndTimeSlot()
        time.sleep(token1[0] + 1)
        token2 = main.MERKFlagTokenAndTimeSlot()
        self.assertEqual(token2[3], token1[1])  # add assertion here

    def test_MERKFlagTokenAndTimeSlot_sameToken(self):
        # Testing generation of same token
        token1 = main.MERKFlagTokenAndTimeSlot()
        token2 = main.MERKFlagTokenAndTimeSlot()
        self.assertEqual(token2[1], token1[1])

    def test_MERKFlagTokenAndTimeSlot_tokenSecuence(self):
        # testing long secuence of tokens
        for sec in range(0, 3):
            token1 = main.MERKFlagTokenAndTimeSlot()
            time.sleep(token1[0] + 1)
            token2 = main.MERKFlagTokenAndTimeSlot()
            self.assertEqual(token2[3], token1[1], )  # the old token2 has to be the same as the new token1

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

    def test_forMERKGetClientPrivateValue(self):
        old_private_value = main.forMERKGetClientPrivateValue()
        self.assertEqual(main.client_private_value, old_private_value)
        old_private_value2 = main.forMERKGetClientPrivateValue()
        self.assertEqual(old_private_value2, old_private_value)

        time_data = datetime.now().strftime("%M/%S").split("/")
        new_client_time = (int(time_data[0]) * 100) + int(time_data[1])
        to_sleep = abs(main.client_private_time - new_client_time)
        time.sleep(to_sleep + 1)
        new_private_value = main.forMERKGetClientPrivateValue()
        self.assertNotEqual(old_private_value, new_private_value)

    def test_forMERKGetServerPrivateValue(self):
        old_private_value = main.forMERKGetServerPrivateValue()
        self.assertEqual(main.server_private_value, old_private_value)
        old_private_value2 = main.forMERKGetServerPrivateValue()
        self.assertEqual(old_private_value2, old_private_value)

        time_data = datetime.now().strftime("%M/%S").split("/")
        new_server_time = (int(time_data[0]) * 100) + int(time_data[1])
        to_sleep = abs(main.server_private_time - new_server_time)
        time.sleep(to_sleep + 1)
        new_private_value = main.forMERKGetServerPrivateValue()
        self.assertNotEqual(old_private_value, new_private_value)

    def test_MERKcifValue(self):
        expected = [101, 99, 104, 111, 32, 106, 101, 106, 101]
        for token in range(0, 10):
            command_data = main.MERKcifValue("echo jeje", token).split(",")
            for pos in range(0, len(command_data)):
                self.assertEqual(expected[pos] + token, int(command_data[pos]), token)

    def test_MERKcifResultValue(self):
        data = "this is a random string:)"
        for token in range(0, 10):
            cif_value = main.MERKcifValue(data, token)
            result_value = main.MERKgetValue(cif_value.split(","), token)
            self.assertEqual(data, result_value)

    def test_forMerkStateMachineClient_DH1(self):
        result = main.forMerkStateMachineClient("DH_1:" + str(main.common_value + 4444))
        self.assertEqual(result, "DH_2:" + str(main.client_private_value + 4444))

    def test_forMerkStateMachineClient_DH2(self):
        result = main.forMerkStateMachineClient(
            "DH_2:" + str(1 + main.client_private_value) + "," + str(2222 + main.client_private_value)).split("/")[0]
        self.assertEqual(result, "PVT_1:2323,2321,2326,2333,2254,2328,2323,2328,2323")

    def test_forMerkStateMachineClient_PVT_1(self):
        test_string = "test"
        result = main.forMerkStateMachineClient("PVT_1:" + main.MERKcifValue(test_string, 2222))
        self.assertEqual(result, main.state_machine_end_mark + test_string)

    def test_forMerkStateMachineServer_DH_1(self):
        priv_value = main.forMERKGetServerPrivateValue()
        token_vals = main.MERKFlagTokenAndTimeSlot()
        result = main.forMerkStateMachineServer("DH_1/" + str(main.MERKgenTimeFlag()[0]), priv_value, token_vals)
        self.assertEqual(result, "DH_1:" + str(main.forMERKGetServerPrivateValue() + main.common_value) + "/" + str(
            main.MERKgenTimeFlag()[0]))

    def test_forMerkStateMachineServer_DH_2(self):
        client_value = 1111
        priv_value = main.forMERKGetServerPrivateValue()
        token_vals = main.MERKFlagTokenAndTimeSlot()
        result = main.forMerkStateMachineServer(
            "DH_2:" + str(client_value + main.forMERKGetServerPrivateValue()) + "/" + str(
                main.MERKgenTimeFlag()[0]),priv_value,token_vals).split(
            "/")[0]
        self.assertEqual(result, "DH_2:" + str(client_value + main.MERKFlagTokenAndTimeSlot()[0]) + "," + str(
            client_value + main.MERKFlagTokenAndTimeSlot()[1]))

    def test_forMerkStateMachineServer_PVT_1(self):

        warnings.simplefilter("ignore")
        command = "echo jeje"
        expected_result = "jeje\n"
        main.MERKFlagTokenAndTimeSlot()
        time.sleep(5)
        main.MERKFlagTokenAndTimeSlot()
        command_data = main.MERKcifValue(command, main.new_token)
        priv_value = main.forMERKGetServerPrivateValue()
        token_vals = main.MERKFlagTokenAndTimeSlot()
        result = main.forMerkStateMachineServer(
            "PVT_1:" + command_data + "/" + str(main.MERKgenTimeFlag()[0]),
            priv_value,
            token_vals
        ).split("/")[0]
        self.assertEqual(expected_result, main.MERKgetValue(result.split("PVT_1:")[1].split(","), main.new_token))

    def test_MERKClient(self):
        data = "127.0.0.1:4450"
        result = main.MERKClient(data, self.aux_sender, self.aux_forMerkStateMachineClient)
        self.assertEqual("DH_1", result.split("/")[0])

    def aux_sender(self, data, obj, port):
        data = (data + "/" + str(main.MERKgenTimeFlag()[0])).encode()
        return data

    def aux_forMerkStateMachineClient(self, response):
        return "forMerkStateMachineClientEnds"

    def test_integration(self):
        test_data = "ip:localhost", "port:5000", "cicles:5", "delay:10"
        default_result = ("127.0.0.1", 4450, 1, 10)

        for count in range(0, len(test_data)):
            count = bin(count)
            data_to_try = []
            expected_result = []
            if count[2] == "1":
                data_to_try.append(test_data[0])
                expected_result.append(test_data[0].split(":")[1])
            else:
                expected_result.append(default_result[0])
            if len(count) > 3:
                if int(count[3]) == 1:
                    data_to_try.append(test_data[1])
                    expected_result.append(test_data[1].split(":")[1])
                else:
                    expected_result.append(default_result[1])
            else:
                expected_result.append(default_result[1])

            if len(count) > 4:
                if int(count[4]) == 1:
                    data_to_try.append(test_data[2])
                    expected_result.append(test_data[2].split(":")[1])
                else:
                    expected_result.append(default_result[2])
            else:
                expected_result.append(default_result[2])

            if len(count) > 5:
                if int(count[5]) == 1:
                    data_to_try.append(test_data[3])
                    expected_result.append(test_data[3].split(":")[1])
                else:
                    expected_result.append(default_result[3])
            else:
                expected_result.append(default_result[3])

            result = main.main(data_to_try)
            for aux in expected_result:
                self.assertIn(str(aux), result, (result, data_to_try))


if __name__ == '__main__':
    initial = time()
    unittest.main()
    final = time()
    print("Testing time:",final-initial)
