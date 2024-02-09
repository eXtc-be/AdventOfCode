# aoc_2016_04_A_1.py - Day 4: Security Through Obscurity - part 1
# What is the sum of the sector IDs of the real rooms?
# https://adventofcode.com/2016/day/4


from tools import time_it

from typing import NamedTuple
import re
from collections import Counter

from pprint import pprint


DATA_PATH = './input_2016_04'

ROOM = re.compile(r'([a-z-]+)-(\d+)\[([a-z]+)\]')


class Room(NamedTuple):
    name: str
    sector: int
    checksum: str

    def _calc_checksum(self) -> str:
        checksum = ''
        counts = Counter(self.name.replace('-', '')).most_common()  # count the number of occurrences
        # print('counts =', counts)

        freqs = Counter([count[1] for count in counts]).most_common()  # count the number of occurrences of the occurrences
        # print('freqs =', freqs)

        uniques = [freq[0] for freq in freqs if freq[1] == 1]
        # print('uniques =', uniques)

        ties = [freq[0] for freq in freqs if freq[1] > 1]
        # print('ties =', ties)

        # all_counts = sorted(uniques + ties, reverse=True)
        # print('all_counts =', all_counts)

        for count in sorted(uniques + ties, reverse=True):
            if count in uniques:
                checksum += [c[0] for c in counts if c[1] == count][0]
            elif count in ties:
                checksum += ''.join(sorted([c[0] for c in counts if c[1] == count]))

        # print('full checksum =', checksum)

        return checksum[:5]

    def validate(self) -> bool:
        return self.checksum == self._calc_checksum()

    def decrypt(self) -> str:
        result = ''

        for c in self.name:
            if c == '-':
                result += ' '
            else:
                result += chr((ord(c) - ord('a') + self.sector) % 26 + ord('a'))

        return result


def load_data(path: str) -> list[str]:
    with open(path) as f:
        return f.read().splitlines()


def get_rooms(datalines: list[str]) -> list[Room]:
    rooms = []
    for line in datalines:
        match = ROOM.match(line)
        if match:
            rooms.append(
                Room(
                    match.groups()[0],
                    int(match.groups()[1]),
                    match.groups()[2]
                )
            )
    return rooms


test_data_1 = '''
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
'''.strip().splitlines()

test_data_2 = '''
fubrjhqlf-edvnhw-dftxlvlwlrq-803[wjvzd]
kzgwomvqk-rmttgjmiv-lmxizbumvb-902[zmnji]
dkqjcbctfqwu-dwppa-fgukip-596[syiua]
xjinphzm-bmvyz-ytz-gjbdnodxn-135[nzbdj]
uwtojhynqj-hfsid-xytwflj-177[ztsqu]
udpsdjlqj-fkrfrodwh-ilqdqflqj-491[uscwt]
kdijqrbu-fbqijys-whqii-sedjqydcudj-790[dijqb]
udpsdjlqj-hjj-uhdftxlvlwlrq-439[jldhq]
bnmrtldq-fqzcd-bqxnfdmhb-bgnbnkzsd-zmzkxrhr-105[bdnzm]
lejkrscv-wlqqp-sleep-ivrthlzjzkzfe-789[elzjk]
zlilocri-ciltbo-obxznrfpfqflk-419[spmzt]
tyepcyletzylw-nsznzwlep-qtylyntyr-821[shmzu]
ynssr-vtgwr-lmhktzx-865[kyqlr]
crwwv-pzxsbkdbo-erkq-pxibp-991[bpkrw]
uiovmbqk-ziuxioqvo-zijjqb-bmkpvwtwog-616[sizek]
qfmcusbwq-foppwh-cdsfohwcbg-194[cfwbh]
nvrgfezqvu-irsszk-drerxvdvek-477[tvzgs]
otzkxtgzoutgr-hatte-jkbkruvsktz-748[yutkm]
ksodcbwnsr-qcbgiasf-ufors-pibbm-rsdzcmasbh-298[sbcra]
dmbttjgjfe-qmbtujd-hsbtt-bobmztjt-259[mkyef]
lnkfaypeha-bhksan-wymqeoepekj-836[lcygv]
zekvierkzferc-treup-ljvi-kvjkzex-789[ekrvz]
ajyqqgdgcb-djmucp-mncpyrgmlq-626[cyuom]
sbnqbhjoh-fhh-bdrvjtjujpo-857[bmhse]
surmhfwloh-iorzhu-vklsslqj-829[hlsor]
ymszqfuo-nmewqf-iadwetab-690[unsbc]
gpewwmjmih-tpewxmg-kveww-xvemrmrk-464[mrtux]
rzvkjiduzy-nxvqzibzm-cpio-mzxzdqdib-395[lnkyz]
qzoggwtwsr-suu-kcfygvcd-766[gcsuw]
molgbzqfib-bdd-rpbo-qbpqfkd-679[tljei]
'''.strip().splitlines()


@time_it
def main(data_lines: list[str]) -> None:
    rooms = get_rooms(data_lines)
    # pprint(rooms)

    real_rooms = []
    for room in rooms:
        status = 'Not real'
        if room.validate():
            real_rooms.append(room)
            status = 'Real'
        # print(room.name, room.checksum, status)
        # print('-' * 100)

    # real_rooms = [room for room in rooms if room.validate()]

    print(f'End result: {sum(room.sector for room in real_rooms)}')
    # print(f'End result: {sum(room.sector for room in rooms)}')


if __name__ == "__main__":
    data_lines = load_data(DATA_PATH)
    # data_lines = test_data_1
    # data_lines = test_data_2
    # print(data_lines)

    main(data_lines)
    # using test_data:
    #   End result: 1514
    #   Finished 'main' in less than a millisecond
    # using input data:
    #   End result: 151272 - too low
    #   Finished 'main' in 28 milliseconds
    # using input data:
    #   End result: 173787
    #   Finished 'main' in 25 milliseconds
