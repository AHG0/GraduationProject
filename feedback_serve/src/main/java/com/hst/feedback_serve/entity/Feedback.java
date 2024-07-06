package com.hst.feedback_serve.entity;

import lombok.Data;

@Data
public class Feedback {
    private Long id;
    private Integer userid;
    private String name;
    private String email;
    private String phone;
    private String module;
    private String file_path;
    private String subTime;
    private String content;
}
