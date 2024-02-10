# aoc_2016_07_B_1.py - Day 7: Internet Protocol Version 7 - part 2
# How many IPs in your puzzle input support TLS?
# https://adventofcode.com/2016/day/7


from aoc_2016_07_A_1 import (
    DATA_PATH,
    load_data,
    # test_data_1,
    test_data_2,
    IPv7_Address,
    IPV7_REGEX,
)

from tools import time_it

# other imports

from pprint import pprint


#         aba_list = []
#         for super in address.supers:
#             aba_list.extend(check_aba(super))
#         print(f'{aba_list=}')
#         for hyper in address.hypers:
#             print(f'{hyper=}')
#             for aba in aba_list:
#                 print('\t', aba, check_bab(hyper, aba))
#     print('-' * 100)


class IPv7_Address_SSL(IPv7_Address):
    @property
    def supports_SSL(self) -> bool:
        aba_list = [aba for super in self.supers for aba in check_aba(super)]
        # print(aba_list)
        return any(check_bab(hyper, aba) for hyper in self.hypers for aba in aba_list)


# other constants


def _check_aba(string: str) -> bool:
    return string[0] != string[1] and string[0] == string[-1]


def check_aba(string: str) -> list[str] | None:
    aba_strings = []

    if len(string) < 3:
        return None
    else:
        for i in range(len(string)-2):
            if _check_aba(string[i:i+2+1]):
                aba_strings.append(string[i:i+2+1])
        return aba_strings


def aba_2_bab(string: str) -> str:
    return string[1] + string[0] + string[1]


def check_bab(string: str, aba: str) -> bool:
    return aba_2_bab(aba) in string


test_data_1 = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
""".strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    addresses = []
    for line in data_lines:
        address = IPv7_Address_SSL()
        matches = IPV7_REGEX.findall(line)
        if matches:
            for super, hyper in zip(matches[::2], matches[1::2]):
                address.supers.append(super)
                address.hypers.append(hyper)
            address.supers.append(matches[-1])  # add last (super) field
            # print(address, address.supports_SSL)
            addresses.append(address)

    supported = [address for address in addresses if address.supports_SSL]
    # print(list(str(address) for address in supported))

    print(f'End result: {len(supported)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    main(data_lines)
    # using test_data 1:
    #   End result: 3
    #   Finished 'main' in less than a millisecond
    # using test_data 2:
    #   End result: 2
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 260
    #   Finished 'main' in 37 milliseconds

    # test check_aba
    # for line in data_lines:
    #     matches = IPV7_REGEX.findall(line)
    #     if matches:
    #         for super, hyper in zip(matches[::2], matches[1::2]):
    #             print(super, check_aba(super))
    #             print(hyper, check_aba(hyper))
    #         print(matches[-1], check_aba(matches[-1]))  # add last (super) field

    # test check_bab
    # for line in data_lines:
    #     address = IPv7_Address_SSL()
    #     matches = IPV7_REGEX.findall(line)
    #     if matches:
    #         for super, hyper in zip(matches[::2], matches[1::2]):
    #             address.supers.append(super)
    #             address.hypers.append(hyper)
    #         address.supers.append(matches[-1])  # add last (super) field
    #         print(f'{address=}')
    #
    #         aba_list = []
    #         for super in address.supers:
    #             aba_list.extend(check_aba(super))
    #         print(f'{aba_list=}')
    #         for hyper in address.hypers:
    #             print(f'{hyper=}')
    #             for aba in aba_list:
    #                 print('\t', aba, check_bab(hyper, aba))
    #     print('-' * 100)

