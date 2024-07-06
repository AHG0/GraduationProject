package com.hst.socket.service;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;

@Component
public interface UService {
    JSONObject getUser(int userid);
}
