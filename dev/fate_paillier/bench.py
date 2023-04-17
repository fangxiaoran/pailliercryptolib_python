#! /usr/bin/env python3

# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

import numpy as np
from fate_paillier import PaillierKeypair
import fate_paillier
import google_benchmark as benchmark


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(1024)
@benchmark.option.arg(2048)
def BM_KeyGen(state):
    while state:
        _ = PaillierKeypair.generate_keypair(state.range(0))


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(16)
@benchmark.option.arg(1)
def BM_Encrypt(state):
    x = (np.arange(state.range(0)) + 11) * 1234.5678
    while state:
        for i in x:
            _ = pk.encrypt(i)


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(16)
@benchmark.option.arg(1)
def BM_Decrypt(state):
    x = (np.arange(state.range(0)) + 1) * 1234.5678
    ct_x = [pk.encrypt(i) for i in x]
    while state:
        for i in ct_x:
            _ = sk.decrypt(i)


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(16)
@benchmark.option.arg(1)
def BM_Add_CTCT(state):
    x = (np.arange(state.range(0)) + 11) * 5111.2834
    y = (32768 - np.arange(state.range(0))) * 1.3872
    ct_x = [pk.encrypt(i) for i in x]
    ct_y = [pk.encrypt(i) for i in y]
    while state:
        for i, j in zip(ct_x, ct_y):
            _ = i + j


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(16)
@benchmark.option.arg(1)
def BM_Add_CTPT(state):
    x = (np.arange(state.range(0)) + 11) * 5111.2834
    y = (32768 - np.arange(state.range(0))) * 1.3872
    ct_x = [pk.encrypt(i) for i in x]
    ct_x = [i * j for i, j in zip(ct_x, x)]
    while state:
        for i, j in zip(ct_x, y):
            _ = i + j


@benchmark.register
@benchmark.option.unit(benchmark.kMicrosecond)
@benchmark.option.arg(16)
@benchmark.option.arg(1)
def BM_Mul_CTPT(state):
    x = (np.arange(state.range(0)) + 11) * 5111.2834
    y = (32768 - np.arange(state.range(0))) * 1.3872
    ct_x = [pk.encrypt(i) for i in x]
    while state:
        for i, j in zip(ct_x, y):
            _ = i * j


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

    pk = fate_paillier.PaillierPublicKey(N)
    sk = fate_paillier.PaillierPrivateKey(pk, P, Q)

    benchmark.main()
