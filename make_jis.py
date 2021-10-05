
def make_checkdigit(num: int) -> int :
    n = [int(x) for x in str(num)]
    s1 = sum(n[1::2]) * 3
    s2 = sum(n[::2])
    s3 = int(str(s1 + s2)[-1])
    s4 = 10 - s3
    if s4==10: s4 = 0
    return s4


if __name__ == '__main__':
    for i in range(25, 50):
        num = int('4030' + f'{i}'.zfill(8))
        c = make_checkdigit(num)
        print(f'{num}{c}')