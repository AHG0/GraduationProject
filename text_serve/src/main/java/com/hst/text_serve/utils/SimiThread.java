package com.hst.text_serve.utils;

class SimiThread extends Thread {
    private final String input;
    public String SimiResult;

    SimiThread(String input) {
        this.input = input;
    }

    @Override
    public void run() {
        // 编写程序，这段程序运行在分支线程中（分支栈）。
        Utils u = new Utils();
        SimiResult = u.PythonSimilar(this.input);
    }
}
