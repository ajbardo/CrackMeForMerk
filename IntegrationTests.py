import time, unittest, main, warnings
from datetime import datetime
from unittest.mock import Mock

class IntegrationTestCase(unittest.TestCase):
    def test_integration(self):
        test_data = "ip:localhost", "port:5000", "cycles:5", "delay:10"
        default_result = ("127.0.0.1", 4450, 1, 10)

        for count in range(0, len(test_data)**2):
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
    unittest.main()