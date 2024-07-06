package com.hst.notify_serve.service;

import com.alibaba.fastjson.JSONObject;

import java.util.List;

public interface NotifyService {
    int save(String title, String content);
    String getTime();
    List<JSONObject> select();
    void updateNotify(int id, String title, String content);
    void deleteNotifyById(int id);
}
