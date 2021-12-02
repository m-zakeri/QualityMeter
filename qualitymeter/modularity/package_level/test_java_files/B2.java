package B;

import A.*;

class B2 {
    public B1[] makeThree() {
        B1 lst[] = new B1[3];
        for (int i=0; i < 3; i++) {
            lst[i] = new B1(i);
        }
        return lst;
    }

    public int compareTo(B1 b, A1 a) {
        if (b.b > a.getAverage()) return 1;
        return 0;
    }
}
