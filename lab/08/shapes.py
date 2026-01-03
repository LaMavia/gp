from functools import cache
from sys import argv

@cache
def shapes_of_n(n: int):
    assert n > 0
    match n:
        case 1: return ["()"]
        case 2: return ["(,)"]
        case n:
            m = n // 2
            out = []
            for i_ in range(m):
                i = i_ + 1
                j = n - i
                if i == j:
                    out.extend(
                        f'({left_tree},{right_tree})' 
                        for li, left_tree in enumerate(shapes_of_n(i)) 
                        for ri, right_tree in enumerate(shapes_of_n(j)) 
                        if li <= ri
                    )
                else:
                    out.extend(
                        f'({left_tree},{right_tree})' 
                        for left_tree in shapes_of_n(i) 
                        for right_tree in shapes_of_n(j)
                    )
            return out

def main():
    n = int(argv[1])
    with open("./out.nwk", "w") as f:
        f.write("(")
        cnt = 0
        for i, t in enumerate(shapes_of_n(n)):
            if i > 0:
                f.write(",")

            f.write(t)
            cnt += 1

        f.write(");")
        print(f"#trees({n}) = {cnt}")

if __name__ == "__main__":
    main()
