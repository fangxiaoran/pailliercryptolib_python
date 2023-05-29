import numpy as np
from prettytable import PrettyTable, ORGMODE
from performance_assess import Metric
from operator import add, mul


class PaillierAssess(object):
    def __init__(self, method, data_num, test_round):
        if method == "Paillier":
            from fate_paillier import PaillierKeypair, PaillierPublicKey, PaillierPrivateKey
            self.is_ipcl = False
        elif method == "IPCL":
            try:
                from ipcl_python import PaillierKeypair, PaillierPublicKey, PaillierPrivateKey
                self.is_ipcl = True
            except ImportError:
                raise ValueError("IPCL is not supported.")
        else:
            raise ValueError(f"Unsupported Paillier method: {method}.")

        # self.public_key, self.private_key = PaillierKeypair.generate_keypair(2048)

        P = int(
            "17907722236348068892950089903191692955407412936775759886364595"
            "52735277384518331167761570138552647970967958807251538217623805"
            "88199893129274771549316901998509025503556766712439571067562061"
            "82758501008605649830815202920954024506122402034968011655978902"
            "1149844414656481106116277049053335145991958168290159067444243"
        )
        Q = int(
            "15364074494048192090239748141292366255531269713338718185264182"
            "86675686268115568620066283414819003320683895025898634379074026"
            "89773240679814850328978260611055592547225724264355875488478904"
            "93257704058129319548913255512313204302948601763310613641989076"
            "0822812194551465180127077927138009701322446602892596555566791"
        )
        N = P * Q

        if method == "Paillier":
            self.public_key = PaillierPublicKey(N)
            self.private_key = PaillierPrivateKey(self.public_key, P, Q)
        elif method == "IPCL":
            self.public_key = PaillierPublicKey(N, N.bit_length(), True)
            self.private_key = PaillierPrivateKey(self.public_key, P, Q)
        else:
            raise ValueError("Unsupported method.")

        self.method = method
        self.data_num = data_num
        self.test_round = test_round
        self.float_data_x, self.encrypt_float_data_x, self.int_data_x, self.encrypt_int_data_x = self._get_data(name='x')
        self.float_data_y, self.encrypt_float_data_y, self.int_data_y, self.encrypt_int_data_y = self._get_data(name='y')

    def _get_data(self, type_int=True, type_float=True, name=''):
        if self.method in ["Paillier", "IPCL"]:
            key = self.public_key
        else:
            key = None
        encrypt_float_data = []
        encrypt_int_data = []
        float_data = np.random.uniform(-1e9, 1e9, size=self.data_num)
        int_data = np.random.randint(-1000, 1000, size=self.data_num)

        if name == 'x':
            float_data = (np.arange(self.data_num) + 11) * 5111.2834
        elif name == 'y':
            float_data = (32768 - np.arange(self.data_num)) * 1.3872

        if self.is_ipcl:
            if type_float:
                encrypt_float_data = key.encrypt(float_data, precision=2**53)
            if type_int:
                encrypt_int_data = key.encrypt(int_data)
        else:
            if type_float:
                for i in float_data:
                    encrypt_float_data.append(key.encrypt(i, precision=2**53))
            if type_int:
                for i in int_data:
                    encrypt_int_data.append(key.encrypt(i))
        return float_data, encrypt_float_data, int_data, encrypt_int_data

    def output_table(self):
        table = PrettyTable()
        table.set_style(ORGMODE)
        table.field_names = [self.method, "One time consumption", f"{self.data_num} times consumption",
                             "relative acc", "log2 acc", "operations per second", "plaintext consumption per second"]

        metric = Metric(data_num=self.data_num, test_round=self.test_round)

        # table.add_row(metric.encrypt(self.float_data_x, self.public_key.encrypt, is_ipcl=self.is_ipcl))
        # decrypt_data = self.private_key.decrypt(self.encrypt_float_data_x) if self.is_ipcl else [
        #     self.private_key.decrypt(i) for i in self.encrypt_float_data_x]
        # table.add_row(metric.decrypt(self.encrypt_float_data_x, self.float_data_x, decrypt_data,
        #                              self.private_key.decrypt, is_ipcl=self.is_ipcl))

        real_data = list(map(add, self.float_data_x, self.float_data_y))
        if self.is_ipcl:
            encrypt_data = self.encrypt_float_data_x + self.encrypt_float_data_y
        else:
            encrypt_data = list(map(add, self.encrypt_float_data_x, self.encrypt_float_data_y))
        self.binary_op(table, metric, self.encrypt_float_data_x, self.encrypt_float_data_y,
                       self.float_data_x, self.float_data_y, real_data, encrypt_data,
                       add, "float add")

        # real_data = list(map(add, self.int_data_x, self.int_data_y))
        # if self.is_ipcl:
        #     encrypt_data = self.encrypt_int_data_x + self.encrypt_int_data_y
        # else:
        #     encrypt_data = list(map(add, self.encrypt_int_data_x, self.encrypt_int_data_y))
        # self.binary_op(table, metric, self.encrypt_int_data_x, self.encrypt_int_data_y,
        #                self.int_data_x, self.int_data_y, real_data, encrypt_data,
        #                add, "int add")

        real_data = list(map(mul, self.float_data_x, self.float_data_y))
        if self.is_ipcl:
            encrypt_data = self.encrypt_float_data_x * self.float_data_y
        else:
            encrypt_data = list(map(mul, self.encrypt_float_data_x, self.float_data_y))
        self.binary_op(table, metric, self.encrypt_float_data_x, self.float_data_y,
                       self.float_data_x, self.float_data_y, real_data, encrypt_data,
                       mul, "float mul")

        # real_data = list(map(mul, self.int_data_x, self.int_data_y))
        # if self.is_ipcl:
        #     encrypt_data = self.encrypt_int_data_x * self.int_data_y
        # else:
        #     encrypt_data = list(map(mul, self.encrypt_int_data_x, self.int_data_y))
        # self.binary_op(table, metric, self.encrypt_int_data_x, self.int_data_y,
        #                self.int_data_x, self.int_data_y, real_data, encrypt_data,
        #                mul, "int mul")

        return table.get_string(title=f"{self.method} Computational performance")

    def binary_op(self, table, metric, encrypt_data_x, encrypt_data_y, raw_data_x, raw_data_y,
                  real_data, encrypt_data, op, op_name):
        decrypt_data = self.private_key.decrypt(encrypt_data) if self.is_ipcl else [
            self.private_key.decrypt(i) for i in encrypt_data]
        table.add_row(metric.binary_op(encrypt_data_x, encrypt_data_y,
                                       raw_data_x, raw_data_y,
                                       real_data, decrypt_data,
                                       op, op_name, is_ipcl=self.is_ipcl))
