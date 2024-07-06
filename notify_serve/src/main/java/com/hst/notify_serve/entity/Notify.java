package com.hst.notify_serve.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

@Data
public class Notify {
    @TableId("id")
    private Integer id;
    private String title;
    private String content;
    private String time;
}
