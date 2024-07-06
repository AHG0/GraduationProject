package com.hst.file_serve.utils;

import com.alibaba.fastjson.JSONObject;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class EntityThreadPool {
    private final List<String> input;
    public JSONObject entityResult;

    EntityThreadPool(List<String> input) {
        this.input = input;
    }

    //public void ThreadPool() {
    //    EntityUtils eu = new EntityUtils();
    //    ExecutorService cachedThreadPool = Executors.newCachedThreadPool();
    //
    //    for (String inp : this.input) {
    //        cachedThreadPool.execute(new Runnable() {
    //            @Override
    //            public void run() {
    //                entityResult = eu.getEntity(inp);
    //                System.out.println(entityResult);
    //            }
    //        });
    //    }
    //    cachedThreadPool.shutdown();
    public void ThreadPool() {
        FileEntityUtils eu = new FileEntityUtils();
        int numThreads = 3; // 设置线程数量
        ExecutorService threadPool = Executors.newFixedThreadPool(numThreads);

        for (String inp : this.input) {
            threadPool.execute(new Runnable() {
                @Override
                public void run() {
                    entityResult = eu.getEntity(inp);
                }
            });
        }
        threadPool.shutdown(); // 关闭线程池
    }
}