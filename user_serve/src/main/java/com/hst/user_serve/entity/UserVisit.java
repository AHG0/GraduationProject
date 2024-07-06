package com.hst.user_serve.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

@Data
public class UserVisit {
    @TableId("userid")
    private Integer userid;
    private String visit_day;
    private Integer visit_count;
    private Integer submit_count;
    private Integer c_submit_count;
}
