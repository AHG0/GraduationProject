package com.hst.socket.service.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.hst.socket.mapper.UMapper;
import com.hst.socket.service.UService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UServiceImpl implements UService {
    @Autowired
    private UMapper uMapper;

    public JSONObject getUser(int userid){
        return uMapper.getUser(userid);
    }
}
