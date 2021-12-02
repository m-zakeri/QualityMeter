package A;

class A2 {
    private A1 obj;

    public A2(A1 obj) {
        this.obj = obj;
    }
    
    public int getAverage() {
        return this.obj.getAverage();
    }

    public int compare(A1 a1) {
        if (this.obj.getSum() > a1.getSum()) return 1;
        return 0;
    }
}