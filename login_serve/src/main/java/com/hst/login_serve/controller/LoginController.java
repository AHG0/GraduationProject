package com.hst.login_serve.controller;

import com.alibaba.fastjson.JSONObject;
import com.hst.login_serve.entity.User;
import com.hst.login_serve.entity.UserVisit;
import com.hst.login_serve.jwt.JwtUtil;
import com.hst.login_serve.mapper.LoginMapper;
import com.hst.login_serve.mapper.VisitMapper;
import com.hst.login_serve.service.impl.LoginServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Objects;

@RestController
public class LoginController {
    @Autowired
    private LoginMapper loginMapper;
    @Autowired
    private VisitMapper visitMapper;
    @Autowired
    private LoginServiceImpl loginService;
    @Autowired
    User user;
    JwtUtil jwtUtil = new JwtUtil();
    UserVisit userVisit = new UserVisit();

    //根据id查找用户
    @GetMapping("/login/{id}")
    public User findById(@PathVariable int id) {
        return loginMapper.selectById(id);
    }

    //查找所有用户
    @GetMapping("/select_all")
    public List<User> findAll() {
        return loginMapper.selectList(null);
    }


    //登录功能
    @GetMapping("/userLogin")
    public JSONObject findById(@RequestParam("username") String username, @RequestParam("password") String password) {
        List<User> userList = loginMapper.selectList(null);
        for (User user : userList) {
            if (Objects.equals(password, user.getPassword()) && Objects.equals(username, user.getUsername())) {
                loginMapper.updateToken(username, jwtUtil.createToken(user));
                JSONObject json = loginService.selectLoginUserInfoByUsername(username);
                int userid = json.getInteger("userid");
                //判断是否为管理员以及今天是否已经登录过，是则登录次数+=1，否则插入
                if (!user.getPermission()) {
                    if (loginService.isLoginToday(userid, loginService.getDay()) == 0) {
                        userVisit.setUserid(user.getUserid());
                        userVisit.setVisit_day(loginService.getDay());
                        userVisit.setVisit_count(1);
                        userVisit.setSubmit_count(0);
                        userVisit.setC_submit_count(0);
                        visitMapper.insert(userVisit);
                    } else {
                        loginService.countAdd(userid, loginService.getDay());
                    }
                }
                return json;
            }
        }
        return null;
    }

    @RequestMapping("/selectVisitCount")
    public List<JSONObject> selectVisitCount() {
        return loginService.selectVisitCount();
    }

    @RequestMapping("/selectDayAddUser")
    public List<JSONObject> selectDayAddUser() {
        return loginService.dayAddUser();
    }

    //用户注册功能
    @GetMapping("/add_login")
    public boolean add(@RequestParam("username") String username, @RequestParam("password") String password,
                       @RequestParam("mail") String mail, @RequestParam("phone") String phone) {
        List<User> list = loginMapper.selectList(null);
        for (User i : list) {
            if (Objects.equals(username, i.getUsername())) {
                return false;
            }
        }
        int maxId = loginMapper.findMaxId();
        user.setUserid(maxId + 1);
        user.setUsername(username);
        user.setPassword(password);
        user.setPermission(false);
        user.setMail(mail);
        user.setPhone(phone);
        user.setUsertype(0);
        user.setQueries_num(10);
        user.setRegistration_day(loginService.getDay());
        loginMapper.insert(user);
        return true;
    }
    //管理员注册用户功能

    //更改功能
    @GetMapping("/update_login")
    public boolean update(@RequestParam("id") int id, @RequestParam("name") String username, @RequestParam("password") String password, @RequestParam("permission") boolean perm) {
        try {
            user.setUserid(id);
            user.setUsername(username);
            user.setPassword(password);
            user.setPermission(perm);
            loginMapper.updateById(user);
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    //删除功能
    @GetMapping("/delete_login/{id}")
    public void delete(@PathVariable("id") int id) {
        loginMapper.deleteById(id);
    }
}

