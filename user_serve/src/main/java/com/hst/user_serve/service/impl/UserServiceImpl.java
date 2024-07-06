package com.hst.user_serve.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.hst.user_serve.mapper.UserMapper;
import com.hst.user_serve.service.UserService;
import com.hst.user_serve.utils.RedisUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Objects;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    UserMapper userMapper;
    @Autowired
    private RedisUtil redisUtil;
    private JSONObject userInfoMySql;

    public JSONObject getUserRedis(int userid) {
        String key = String.format("userid%d", userid);
        JSONObject users = JSONObject.parseObject(JSON.toJSONString(redisUtil.get(key)));
        if (CollectionUtils.isEmpty(users)) {
            this.userInfoMySql = userMapper.selectById(userid);
            System.out.println(this.userInfoMySql);
            redisUtil.set(key, this.userInfoMySql);
            return this.userInfoMySql;
        }
        return users;
    }

    public JSONObject getUser(int userid) {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        try {
            Date now_date = sdf.parse(getDate());
            String expire_date = userMapper.selectById(userid).get("expire_date").toString();
            if (Objects.equals(expire_date, "null") || now_date.before(sdf.parse(expire_date))) {
                //表示now_date小于expire_date
                System.out.println(userMapper.selectById(userid).get("expire_date"));
                JSONObject userInfo = userMapper.selectById(userid);
                // 表示会员没有过期
                userInfo.put("isExpire", 0);
                return userMapper.selectById(userid);
            } else {
                expire(userid);
                JSONObject userInfo = userMapper.selectById(userid);
                // 表示会员过期
                userInfo.put("isExpire", 1);
                return userInfo;
            }
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }

    }

    public void updateUserRedis(int userid, int value) {
        String key = String.format("userid%d", userid);
        JSONObject userInfo = JSONObject.parseObject(JSON.toJSONString(redisUtil.get(key)));
        redisUtil.updateRedisValue(userInfo, key, value);
    }

    public void updateQueriesNum(int userid, int value) {
        userMapper.updateQueriesNum(userid, value);
    }

    public List<JSONObject> selectAllUser() {
        return userMapper.selectAllUser();
    }

    public int selectExist(String name) {
        return userMapper.selectExist(name);
    }

    public String getDate() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        Date date = new Date(System.currentTimeMillis());
        return formatter.format(date);
    }

    public void expire(int userid) {
        userMapper.expire(userid);
    }
}
