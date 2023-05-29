import numpy as np
import ipcl_python as ipcl
import cProfile
from fate import fate_paillier


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

pk = ipcl.PaillierPublicKey(N, N.bit_length(), True)
sk = ipcl.PaillierPrivateKey(pk, P, Q)

length = 16
x = (np.arange(length) + 11) * 5111.2834
y = (32768 - np.arange(length)) * 1.3872
ct_x = pk.encrypt(x, precision=None)
ct_y = pk.encrypt(y, precision=2**53)

i = 0
with cProfile.Profile() as pr:
    while i < 1000:
        i += 1
        _ = ct_x + ct_x
print(f"Time slots: {ct_x.time_slot_0}, {ct_x.time_slot_1}, {ct_x.time_slot_2}")
print(f"Total: {ct_x.time_slot_0 + ct_x.time_slot_1 + ct_x.time_slot_2}")
pr.print_stats()

pkk = fate_paillier.PaillierPublicKey(N)
skk = fate_paillier.PaillierPrivateKey(pkk, P, Q)

ct_xx = [pkk.encrypt(i, precision=None) for i in x]
ct_yy = [pkk.encrypt(i, precision=2**53) for i in y]

i = 0
with cProfile.Profile() as pr:
    while i < 1000:
        i += 1
        _ = [i + j for i, j in zip(ct_xx, ct_xx)]

pr.print_stats()
