package com.hst.user_serve.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.hst.user_serve.entity.User;
import com.hst.user_serve.entity.UserVisit;
import com.hst.user_serve.jwt.JwtUtil;
import com.hst.user_serve.mapper.LoginMapper;
import com.hst.user_serve.mapper.VisitMapper;
import com.hst.user_serve.service.LoginService;
import com.hst.user_serve.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Objects;

@Service
public class LoginServiceImpl implements LoginService {
    @Autowired
    private LoginMapper loginMapper;
    @Autowired
    private VisitMapper visitMapper;
    @Autowired
    private UserService userService;
    @Autowired
    User user;
    JwtUtil jwtUtil = new JwtUtil();
    UserVisit userVisit = new UserVisit();

    public JSONObject login(String username, String password){
        List<User> userList = loginMapper.selectList(null);
        for (User user : userList) {
            if (Objects.equals(password, user.getPassword()) && Objects.equals(username, user.getUsername())) {
                loginMapper.updateToken(username, jwtUtil.createToken(user));
                JSONObject json = selectLoginUserInfoByUsername(username);
                int userid = json.getInteger("userid");
                JSONObject userinfo = userService.getUser(userid);
                //判断是否为管理员以及今天是否已经登录过，是则登录次数+=1，否则插入
                if (!user.getPermission()) {
                    if (isLoginToday(userid, getDay()) == 0) {
                        userVisit.setUserid(user.getUserid());
                        userVisit.setVisit_day(getDay());
                        userVisit.setVisit_count(1);
                        userVisit.setSubmit_count(0);
                        userVisit.setC_submit_count(0);
                        visitMapper.insert(userVisit);
                    } else {
                        countAdd(userid, getDay());
                    }
                }
                return userinfo;
            }
        }
        return null;
    }

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
}
