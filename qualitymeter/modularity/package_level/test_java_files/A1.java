package A;

class A1 {
    private int x;
    private int y;

    public int getSum() {
        return this.x + this.y;
    }

    public int getAverage() {
        return this.sum() / 2;
    }
}
