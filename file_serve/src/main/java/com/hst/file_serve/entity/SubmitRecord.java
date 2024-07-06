package com.hst.file_serve.entity;

import lombok.Data;

@Data
public class SubmitRecord {
    private Integer id;
    private String input;
    private String rsl1;
    private String rsl2;
    private String rsl3;
    private String name;
    private Integer userid;
    private String subTime;
}
