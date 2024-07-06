package com.hst.file_serve.service;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public interface FileEntityService {
    JSONObject getEntity(String inputData);
    JSONArray selectE();
    JSONArray selectEName();
    List<JSONObject> selectEData(String name, int userid);
    List<JSONObject> selectByUserId(int userid);
    List<JSONObject> selectRecordByUserId(int userid);
    void insertEntity(JSONObject object, String input, String name, int userid);
    boolean deleteEntity(String input);
    String getTime();
    String getDay();
    void subCountAdd(int userid,int file_num, String sub_day);
    void decUserQueriesNum(int userid, int file_num);
}
