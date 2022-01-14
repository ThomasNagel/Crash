from z3InteractClasses import z3Runner

def main():
    z3 = z3Runner("code.smt", "out.txt", "default.txt", True)

    N = 520
    for n in range(1, 6):
        smtCode = z3.getTextBlock(0) + "(assert (and\n"

        for i in range(1, 11):
            smtCode = smtCode + f'(ite (= (F {i}) true) (and (= (a {i}) (+ (a {i - 1}) (* 2 (b {i - 1})))) (= (b {i}) (+ (b {i - 1}) {i}))) (and (= (b {i}) (+ (a {i - 1}) (b {i - 1}))) (= (a {i}) (+ (a {i - 1}) {i}))))\n'               

        smtCode = smtCode + f'))\n\n(assert (= (b 10) (+ {N} {n})))\n\n' + z3.getTextBlock(1)

        if not z3.runz3(smtCode):
            print(n)
    

if __name__ == "__main__":
    main()