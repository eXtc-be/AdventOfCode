# aoc_2016_07_A_1.py - Day 7: Internet Protocol Version 7 - part 1
# How many IPs in your puzzle input support TLS?
# https://adventofcode.com/2016/day/7
from ipaddress import IPv4Address

from tools import time_it

import re
from dataclasses import dataclass, field

from pprint import pprint


DATA_PATH = './input_2016_07'

IPV7_REGEX = re.compile(r'\]?([a-z]+)\[?')


@dataclass
class IPv7_Address:
    supers: list[str] = field(default_factory=list)
    hypers: list[str] = field(default_factory=list)

    @property
    def supports_TLS(self) -> bool:
        if any(check_abba(hyper) for hyper in self.hypers):
            return False
        if any(check_abba(super) for super in self.supers):
            return True
        return False

    def __repr__(self) -> str:
        return (f'{type(self).__name__}('
                f'supers={self.supers}, '
                f'hypers={self.hypers})')

    def __str__(self) -> str:
        result = ''
        for super, hyper in zip(self.supers, self.hypers):
            result += f'{super}[{hyper}]'
        result += f'{self.supers[-1]}'
        return result


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def _check_abba(string: str) -> bool:
    if string[0] == string[1]:
        return False
    if string[0] != string[-1]:
        return False
    if string[1] != string[-2]:
        return False
    return True


def check_abba(string: str) -> bool:
    if len(string) < 4:
        return False
    else:
        for i in range(len(string)-3):
            if _check_abba(string[i:i+3+1]):
                return True
        return False


test_data_1 = '''
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
'''.strip().splitlines()

test_data_2 = '''
wysextplwqpvipxdv[srzvtwbfzqtspxnethm]syqbzgtboxxzpwr[kljvjjkjyojzrstfgrw]obdhcczonzvbfby[svotajtpttohxsh]cooktbyumlpxostt
emzopymywhhxulxuctj[dwwvkzhoigmbmnf]nxgbgfwqvrypqxppyq[qozsihnhpztcrpbdc]rnhnakmrdcowatw[rhvchmzmyfxlolwe]uysecbspabtauvmixa
bqooxxweoytjghrqn[hkwwukixothfyglw]kpasnmikmbzcbfi[vlnyszifsaaicagxtqf]ucdyxasusefuuxlx
rxpusykufgqujfe[rypwoorxdemxffui]cvvcufcqmxoxcphp[witynplrfvquduiot]vcysdcsowcxhphp[gctucefriclxaonpwe]jdprpdvpeumrhokrcjt
iungssgfnnjlgdferc[xfffplonmzjmxkinhl]dehxdielvncdawomqk[teizynepguvtgofr]fjazkxesmlwryphifh[ppjfvfefqhmuqtdp]luopramrehtriilwlou
mqxqhcpalwycdxw[fkwhjscfmgywhtvdb]khadwvhkxygtxqx
ihekzgbwpjxgbau[eqpvqxncntbtsqn]mbtbcujdkbrhxdu
izikobnovmjzngo[ombcpcvshnedtndu]lnnmdkuapgnxpgyxcmg[bgnxdzmiolfvvaizu]tcvnrfufuvhgmlxcm
yhrowrreplrrsbupeor[nchtznfzbzwnogh]rynudxihckzattbz[dshxeaqusdlhydtm]rvqzuffgqtysfzxp
unfjgussbjxzlhopoqg[ppdnqkiuooukdmbqlo]flfiieiitmettblfln
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    addresses = []
    for line in data_lines:
        address = IPv7_Address()
        matches = IPV7_REGEX.findall(line)
        if matches:
            for super, hyper in zip(matches[::2], matches[1::2]):
                address.supers.append(super)
                address.hypers.append(hyper)
            address.supers.append(matches[-1])  # add last (super) field
            # print(address, address.supports_TLS)
            addresses.append(address)

    supported = [address for address in addresses if address.supports_TLS]
    # print(list(str(address) for address in supported))

    print(f'End result: {len(supported)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    main(data_lines)
    # using test_data 1:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 118
    #   Finished 'main' in 44 milliseconds

    # check structure of input data
    # for line in data_lines:
    #     if (
    #             line[0] == '[' or
    #             line[-1] == ']' or
    #             line.count('[') != line.count(']')
    #     ):
    #         print(line[-1])

    # test check_abba
    # for line in data_lines:
    #     matches = IPV7_REGEX.findall(line)
    #     if matches:
    #         for super, hyper in zip(matches[::2], matches[1::2]):
    #             print(super, check_abba(super))
    #             print(hyper, check_abba(hyper))
    #         print(matches[-1], check_abba(matches[-1]))  # add last (super) field

