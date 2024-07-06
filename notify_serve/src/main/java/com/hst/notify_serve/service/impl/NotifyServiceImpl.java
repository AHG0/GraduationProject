package com.hst.notify_serve.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.hst.notify_serve.entity.Notify;
import com.hst.notify_serve.mapper.NotifyMapper;
import com.hst.notify_serve.service.NotifyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Service
public class NotifyServiceImpl implements NotifyService {
    @Autowired
    private NotifyMapper notifyMapper;
    Notify notify = new Notify();
    public int save(String title, String content){
        notify.setId(timeId());
        notify.setTitle(title);
        notify.setContent(content);
        notify.setTime(getTime());
        return notifyMapper.insert(notify);
    }

    public List<JSONObject> select(){
        return notifyMapper.select();
    }

    public void updateNotify(int id, String title, String content){
        notify.setId(id);
        notify.setTitle(title);
        notify.setContent(content);
        notifyMapper.updateById(notify);
    }

    public void deleteNotifyById(int id){
        notifyMapper.deleteById(id);
    }

    public String getTime(){
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return formatter.format(date);
    }

    public int timeId(){
        long timestamp = System.currentTimeMillis();
        return (int)timestamp;
    }
}
