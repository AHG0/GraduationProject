package com.hst.feedback_serve.service.impl;

import com.alibaba.fastjson.JSONObject;
import com.hst.feedback_serve.entity.Feedback;
import com.hst.feedback_serve.mapper.FeedbackMapper;
import com.hst.feedback_serve.service.FeedbackService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Random;

@Service
public class FeedbackServiceImpl implements FeedbackService {
    @Autowired
    private FeedbackMapper feedbackMapper;
    // 文件上传/下载路径（可配置参数）
    @Value("${file.uploadFolder}")
    private String filePath;

    public void addFeedback(int userid, String name, String email, String phone, String module, String filePath, String time) {
        Feedback feedback = new Feedback();
        feedback.setId(getId());
        feedback.setUserid(userid);
        feedback.setName(name);
        feedback.setEmail(email);
        feedback.setPhone(phone);
        feedback.setModule(module);
        feedback.setFile_path(filePath);
        feedback.setSubTime(time);
        feedbackMapper.insert(feedback);
    }

    public byte[] download(String filePath) throws IOException {
            // 关联文件
            File file = new File(filePath);
            byte[] fileBytes = null;
            FileInputStream fileInputStream = null;
            ByteArrayOutputStream bos = null;
            try {
                fileInputStream = new FileInputStream(file);
                bos = new ByteArrayOutputStream();
                byte[] bytes = new byte[1024];
                int len = -1;
                while ((len = fileInputStream.read(bytes)) != -1) {
                    bos.write(bytes, 0, len);
                }
                fileBytes = bos.toByteArray();
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    fileInputStream.close();
                    bos.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return fileBytes;

    }

    public List<JSONObject> getFeedback(){
        return feedbackMapper.selectAll();
    }

    public List<JSONObject> getFeedbackById(int userid){
        return feedbackMapper.selectByUserid(userid);
    }

    public void updateFeedback(Feedback feedback) {
        feedbackMapper.updateFeedback(feedback.getContent(), feedback.getId());
    }

    public String getTime() {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date(System.currentTimeMillis());
        return formatter.format(date);
    }

    Long getId() {
        String id1 = Long.toString(System.currentTimeMillis());
        Random random = new Random();
        int randomSuffix = random.nextInt(1000);
        String id2 = Integer.toString(randomSuffix);
        return Long.parseLong(id1 + id2);
    }
}
