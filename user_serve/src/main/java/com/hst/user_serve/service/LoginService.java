package com.hst.user_serve.service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public interface LoginService {
    JSONObject login(String username, String password);
    JSONObject selectLoginUserInfoByUsername(String username);
    String getDay();
    int isLoginToday(int userid, String day);
    void countAdd(int userid, String day);
    List<JSONObject> selectVisitCount();
    List<JSONObject> dayAddUser();
}
