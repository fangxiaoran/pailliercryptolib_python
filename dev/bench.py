import google_benchmark as benchmark
import ipcl_python as ipcl
import numpy as np


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
# @benchmark.option.arg(64)
def BM_Ciphertext_Addition(state):
    while state:
        _ = ct_x + ct_y


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
def BM_Raw_Addition(state):
    while state:
        _ = ct_x._PaillierEncryptedNumber__raw_add(ct_y)


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
# @benchmark.option.arg(64)
def BM_Align_Exponent(state):
    while state:
        _ = ct_x._PaillierEncryptedNumber__align_exponent(
            ct_x.ciphertext(), ct_x.exponent(),
            ct_y.ciphertext(), ct_y.exponent()
        )


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
# @benchmark.option.arg(64)
def BM_Align_Exponent_Same(state):
    while state:
        _ = ct_x._PaillierEncryptedNumber__align_exponent(
            ct_x.ciphertext(), ct_x.exponent(),
            ct_x.ciphertext(), ct_x.exponent()
        )


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
def BM_Pure_Addition(state):
    xx, yy, _ = ct_x._PaillierEncryptedNumber__align_exponent(
        ct_x.ciphertext(), ct_x.exponent(),
        ct_y.ciphertext(), ct_y.exponent()
    )
    while state:
        _ = xx + yy


if __name__ == "__main__":
    # preset values
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
    ct_x = pk.encrypt(x)
    ct_y = pk.encrypt(y)

    benchmark.main()
