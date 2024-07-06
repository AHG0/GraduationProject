package com.hst.login_serve.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.hst.login_serve.mapper.LoginMapper;
import com.hst.login_serve.mapper.VisitMapper;
import com.hst.login_serve.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@Service
public class LoginServiceImpl implements LoginService {
    @Autowired
    private LoginMapper loginMapper;
    @Autowired
    private VisitMapper visitMapper;

    public JSONObject selectLoginUserInfoByUsername(String username) {
        return loginMapper.selectLoginUser(username);
    }

    public String getDay() {
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        return formatter.format(date);
    }

    public int isLoginToday(int userid, String day) {
        return loginMapper.isLoginToday(userid, day);
    }

    public void countAdd(int userid, String day) {
        loginMapper.countAdd(userid, day);
    }

    public List<JSONObject> selectVisitCount() {
        return visitMapper.selectVisitCount();
    }

    public List<JSONObject> dayAddUser(){
        return visitMapper.dayAddUser();
    }

    public String getDate() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        Date date = new Date(System.currentTimeMillis());
        return formatter.format(date);
    }
}
