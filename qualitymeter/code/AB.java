class A{
    public int f;
    private double x=10.5;
    private double x2=10.5;
    public void method1(){
        int i=2;
        f = i * f;
    }
}
class AB{
    public void method1(){
        return true;
    }
    public void method2(){
        c = method1();
        method1();
    }
}
class B{
    public int b_var;
    public AB abObject = new AB();
    public void method1(){
        b_var = abObject.method1();
    }
}

class C{
    public int A;
    public A aObject = new A();
    public B bObject = new B();
    public AB abObject = new AB();
    public void method1(){
        int name = aObject.method1();
    }
    public void method2(){
        int name = bObject.method1();
    }
}

/*class A{
    public void m(){
        return true;
    }
    public void n(){
       b= m();
    }
}
class C{
    public A a = new A();
    string name = a.m();
}*/
