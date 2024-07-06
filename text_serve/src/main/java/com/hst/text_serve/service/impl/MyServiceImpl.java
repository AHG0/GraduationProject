package com.hst.text_serve.service.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.hst.text_serve.entity.Classify;
import com.hst.text_serve.entity.Entity;
import com.hst.text_serve.mapper.ClassifyMapper;
import com.hst.text_serve.mapper.EntityMapper;
import com.hst.text_serve.service.MyService;
import com.hst.text_serve.utils.Utils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class MyServiceImpl implements MyService {
    @Autowired
    private Utils utils;
    @Autowired
    private ClassifyMapper classifyMapper;
    @Autowired
    private EntityMapper entityMapper;

    @Override
    public JSONObject getClassify(String input) {
        return utils.getClassify(input);
    }

    @Override
    public JSONObject getEntity(String input) {
        return utils.getEntity(input);
    }

    public JSONArray selectE() {
        return utils.getInput(entityMapper.selectEInput());
    }

    public JSONObject selectEData(String input) {
        return entityMapper.selectEByInput(input);
    }

    public JSONArray selectC() {
        return utils.getInput(classifyMapper.selectCInput());
    }

    public JSONObject selectCData(String input) {
        return classifyMapper.selectCByInput(input);
    }


    public void insertClassify() {
        try {
            Classify classify = new Classify();
            classify.setId(classifyMapper.findMaxId() + 1);
            classify.setClas(utils.classifyRsl);
            classify.setInput(utils.inputClassify);
            classify.setSimiOne(utils.similarOne);
            classify.setSimiTwo(utils.similarTwo);
            classify.setSimiThree(utils.similarThree);
            classifyMapper.insert(classify);
        } catch (Exception e) {
            System.out.println("insertClassify出错");
        }
    }

    public void insertEntity(JSONObject object, String input, int userid) {
        try {
            Entity entity = new Entity();
            if (entityMapper.findMaxId() == null) {
                entity.setId(1);
            } else {
                entity.setId(Integer.parseInt(entityMapper.findMaxId()) + 1);
            }
            entity.setRsl1(object.getString("rsl1"));
            entity.setRsl2(object.getString("rsl2"));
            entity.setRsl3(object.getString("rsl3"));
            entity.setInput(input);
            entity.setUserid(userid);
            entityMapper.insert(entity);
        } catch (Exception ignored) {
            System.out.println("insertEntity出错");
        }
    }

    public boolean deleteEntity(String input) {
        return entityMapper.deleteEByInput(input);
    }

    public boolean deleteClassify(String input) {
        return classifyMapper.deleteCByInput(input);
    }
}
