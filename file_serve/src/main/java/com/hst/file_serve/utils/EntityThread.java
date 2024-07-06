package com.hst.file_serve.utils;

import com.alibaba.fastjson.JSONObject;
import com.hst.file_serve.service.FileEntityService;
import com.hst.file_serve.service.impl.FileEntityServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.List;

//public class EntityThread extends Thread{
//    private List<String> input;
//    public JSONObject entityResult;
//
//    EntityThread(List<String> input) {
//        this.input = input;
//    }
//    EntityUtils eu = new EntityUtils();
//
//    public void startThread() {
//        for (String inp : this.input) {
//            Thread thread = new Thread(new Runnable() {
//                @Override
//                public void run() {
//                    entityResult = eu.getEntity(inp);
//                }
//            });
//            thread.start(); // 启动线程
//            try {
//                thread.join();
//            } catch (InterruptedException e) {
//                e.printStackTrace();
//            }
//        }
//    }
//}

public class EntityThread extends Thread {
    List<String> input;

    FileEntityUtils feu = new FileEntityUtils();
    List<JSONObject> entityResults = new ArrayList<>();
    public EntityThread(List<String> input) {
        this.input = input;
    }

    public void startThread() {
        for (String inp : this.input) {
            Thread thread = new Thread(() -> {
                // 这里是每个线程要执行的操作
                System.out.println("调用run");
                System.out.println("inp---->"+ inp);
                entityResults.add(feu.getEntity(inp));
            });
            thread.start(); // 启动线程
            try {
                thread.join(); // 等待线程结束
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public List<JSONObject> getEntityResults() {
        return entityResults;
    }
}
