package com.hst.user_serve.service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public interface UserService {
    JSONObject getUserRedis(int userid);
    JSONObject getUser(int userid);
    void updateUserRedis(int userid, int queries_num);
    void updateQueriesNum(int userid, int queries_num);
    List<JSONObject> selectAllUser();
    int selectExist(String name);
    String getDate();
    void expire(int userid);
}
