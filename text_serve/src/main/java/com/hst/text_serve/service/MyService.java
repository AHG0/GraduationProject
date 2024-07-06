package com.hst.text_serve.service;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;


public interface MyService {
    JSONObject getClassify(String inputData);
    JSONObject getEntity(String inputData);
    JSONArray selectE();
    JSONObject selectEData(String input);
    JSONArray selectC();
    JSONObject selectCData(String input);
    void insertClassify();
    void insertEntity(JSONObject object, String input, int userid);
    boolean deleteEntity(String input);
    boolean deleteClassify(String input);
}
