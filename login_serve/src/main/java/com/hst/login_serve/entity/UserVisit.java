package com.hst.login_serve.entity;

import lombok.Data;

@Data
public class UserVisit {
    private Integer userid;
    private String visit_day;
    private Integer visit_count;
    private Integer submit_count;
    private Integer c_submit_count;
}
