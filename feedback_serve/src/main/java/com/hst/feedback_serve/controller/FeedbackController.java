package com.hst.feedback_serve.controller;

import com.alibaba.fastjson.JSONObject;
import com.hst.feedback_serve.entity.Feedback;
import com.hst.feedback_serve.service.FeedbackService;
import com.hst.user_serve.jwt.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.util.List;

@CrossOrigin
@RestController
public class FeedbackController {
    @Autowired
    private FeedbackService feedbackService;
    JwtUtil jwtUtil = new JwtUtil();
    @RequestMapping("/submitFeedback")
    public String submitFeedback(@RequestHeader("token") String token, @RequestParam("name") String name,
                                 @RequestParam("email") String email, @RequestParam("phone") String phone,
                                 @RequestParam("module") String module, @RequestParam("files") MultipartFile[] files) {
        // 保存文件到服务器指定目录
        try {
            JSONObject tokenData = jwtUtil.verifyToken(token);
            int userid = tokenData.getInteger("userid");
            String subTime = feedbackService.getTime();
            for (MultipartFile file : files) {
                String filePath = "C:\\Users\\17614\\Desktop\\feedback\\" + file.getOriginalFilename();
                file.transferTo(new File(filePath));
                // 处理保存反馈信息到数据库的逻辑
                feedbackService.addFeedback(userid, name, email, phone, module, filePath, subTime);
            }
            // 返回成功消息给前端
            return "Feedback submitted successfully!";
        } catch (IOException e) {
            e.printStackTrace();
            return "Failed to submit feedback.";
        }
    }

    @RequestMapping("/downloadFile")
    public byte[] downloadFile(@RequestParam("filePath") String filePath) throws IOException {
        // 清空输出流
        return feedbackService.download(filePath);
    }

    @RequestMapping("/getFeedback")
    public List<JSONObject> submitFeedback(){
        return feedbackService.getFeedback();
    }

    @RequestMapping("/getFeedbackById")
    public List<JSONObject> getFeedbackById(@RequestParam("userid") int userid){
        return feedbackService.getFeedbackById(userid);
    }

    @RequestMapping("/updateFeedback")
    public void updateFeedback(@RequestBody Feedback feedback){
        feedbackService.updateFeedback(feedback);
    }
}
