package com.hst.socket.service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.context.ApplicationContext;

import java.io.IOException;

@Configurable
public class SQLThread implements Runnable {
    private UService uService;
    private String uid;
    private int userid;

    private static ApplicationContext applicationContext;

    public static void setApplicationContext(ApplicationContext context) {
        applicationContext = context;
    }

    public SQLThread(String uid) {
        this.uid = uid;
        this.uService = applicationContext.getBean(UService.class);
        this.userid = Integer.parseInt(uid);
    }

    private boolean running = true;

    @Override
    public void run() {
        JSONObject userInfo = this.uService.getUser(userid);
        WebSocketService wbs = new WebSocketService();
        while (running) {
            try {
                JSONObject new_userInfo = uService.getUser(userid);
                if (userInfo != new_userInfo) {
                    System.out.println("change");
                    userInfo = new_userInfo;
                    wbs.sendInfo(userInfo.toString(), uid);
                }
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                // 线程被中断，停止轮询
                e.getMessage();
                Thread.currentThread().interrupt();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
    }
    public void stopPolling() {
        running = false;
    }
}
