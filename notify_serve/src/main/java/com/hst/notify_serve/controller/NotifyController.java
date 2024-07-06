package com.hst.notify_serve.controller;

import com.alibaba.fastjson.JSONObject;
import com.hst.notify_serve.service.NotifyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class NotifyController {
    @Autowired
    private NotifyService notifyService;

    @RequestMapping("/publishNotification")
    public int createNotification(@RequestParam("title") String title, @RequestParam("content") String content) {
        return notifyService.save(title, content);
    }

    @RequestMapping("/selectNotification")
    public List<JSONObject> selectNotification() {
        return notifyService.select();
    }

    @RequestMapping("/update_notify")
    public void update_notify(@RequestParam("id") int id, @RequestParam("title") String title, @RequestParam("content") String content) {
        notifyService.updateNotify(id, title, content);
    }

    @RequestMapping("/delete_notify")
    public void delete_notify(@RequestParam("id") int id) {
        notifyService.deleteNotifyById(id);
    }
}
