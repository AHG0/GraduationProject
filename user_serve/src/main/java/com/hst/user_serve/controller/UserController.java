package com.hst.user_serve.controller;


import com.alibaba.fastjson.JSONObject;
import com.hst.user_serve.entity.User;
import com.hst.user_serve.jwt.JwtUtil;
import com.hst.user_serve.mapper.UserMapper;
import com.hst.user_serve.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Objects;

@RestController
@RequestMapping
public class UserController {
    @Autowired
    private UserMapper userMapper;
    @Autowired
    private UserService userService;
    JwtUtil jwtUtil;
    User user = new User();

    @GetMapping("/admin/select_user_by_admin/{name}")
    public List<JSONObject> findByName(@PathVariable String name) {
        return userMapper.fuzzyQueries(name);
    }

    @GetMapping("/admin/select_all_user")
    public List<JSONObject> select() {
        return userService.selectAllUser();
    }

    @RequestMapping("/select_by_userid")
    public JSONObject select(@RequestParam("userid") int userid) {
        return userService.getUser(userid);
    }

    @RequestMapping("/update_by_userid")
    public void update(@RequestHeader("token") String token) {
        JSONObject json = jwtUtil.verifyToken(token);
        userService.updateQueriesNum(json.getInteger("userid"), json.getInteger("queries_num"));
    }

    @RequestMapping("/update_queries_num")
    public void update_queries_num(@RequestParam("userid") int userid, @RequestParam("queries_num") int queries_num) {
        userService.updateQueriesNum(userid, queries_num);
        System.out.println("————————————更新成功————————————");
    }

    @RequestMapping("/add_user")
    public int add(@RequestParam("username") String username, @RequestParam("password") String password,
                   @RequestParam("phone") String phone, @RequestParam("mail") String mail) {
        if (userService.selectExist(username) == 1) {
            return 0;
        } else {
            try {
                user.setUserid(userMapper.findMaxId() + 1);
                user.setUsername(username);
                user.setUsertype(0);
                user.setPhone(phone);
                user.setMail(mail);
                user.setPassword(password);
                user.setQueries_num(10);
                user.setPermission(false);
                user.setExpire_date("null");
                user.setRegistration_day(userService.getDate());
                userMapper.insert(user);
                return 1;
            } catch (Exception e) {
                return 2;
            }
        }
    }

    @RequestMapping("/admin/add_user_by_admin")
    public int addByAdmin(@RequestParam("username") String username, @RequestParam("password") String password,
                          @RequestParam("phone") String phone, @RequestParam("mail") String mail,
                          @RequestParam("usertype") int usertype, @RequestParam("queries_num") int queries_num,
                          @RequestParam("usertype") boolean permission, @RequestParam("expire_date") String expire_date) {
        if (userService.selectExist(username) == 1) {
            return 0;
        } else {
            try {
                user.setUserid(userMapper.findMaxId() + 1);
                user.setUsername(username);
                user.setUsertype(usertype);
                user.setPhone(phone);
                user.setMail(mail);
                user.setPassword(password);
                user.setQueries_num(queries_num);
                user.setPermission(permission);
                user.setExpire_date(expire_date);
                user.setRegistration_day(userService.getDate());
                userMapper.insert(user);
                return 1;
            } catch (Exception e) {
                return 2;
            }
        }
    }

    @GetMapping("/update_user")
    public void update(@RequestParam("userid") int userid, @RequestParam("key") String key,
                       @RequestParam("value") String value) {
        if (Objects.equals(key, "用户名")) {
            userMapper.updateName(userid, value);
        }
        if (Objects.equals(key, "手机号码")) {
            userMapper.updatePhone(userid, value);
        }
        if (Objects.equals(key, "密码")) {
            userMapper.updatePassword(userid, value);
        }
        if (Objects.equals(key, "电子邮箱")) {
            userMapper.updateMail(userid, value);
        }
    }

    @GetMapping("/admin/update_user_by_admin")
    public void updateByAdmin(@RequestParam("userid") int userid, @RequestParam("username") String username,
                              @RequestParam("usertype") int usertype, @RequestParam("phone") String phone,
                              @RequestParam("mail") String mail, @RequestParam("password") String password,
                              @RequestParam("queries_num") int queries_num, @RequestParam("permission") boolean permission,
                              @RequestParam("expire_date") String expire_date) {
        user.setUserid(userid);
        user.setUsername(username);
        user.setUsertype(usertype);
        user.setPhone(phone);
        user.setMail(mail);
        user.setPassword(password);
        user.setQueries_num(queries_num);
        user.setPermission(permission);
        user.setExpire_date(expire_date);
        userMapper.updateById(user);
    }

    @GetMapping("/admin/delete_user/{delete_id}")
    public void delete(@PathVariable int delete_id) {
        user.setUserid(delete_id);
        userMapper.deleteById(delete_id);
    }
}
