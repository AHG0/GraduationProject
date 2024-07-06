package com.hst.feedback_serve.service;

import com.alibaba.fastjson.JSONObject;
import com.hst.feedback_serve.entity.Feedback;

import java.io.IOException;
import java.io.OutputStream;
import java.util.List;

public interface FeedbackService {
    void addFeedback(int userid, String name,String email, String phone, String module, String filePath, String time);
    byte[] download(String filePath) throws IOException;
    List<JSONObject> getFeedback();
    List<JSONObject> getFeedbackById(int userid);
    void updateFeedback(Feedback feedback);
    String getTime();
}
