package com.hst.discount.entity;

import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

@Data
@TableName("coupon")
public class Coupon {
    private Long id;
    private String name;
    private String description;
    private Double discount;
    private String validity;
    private String category;
    private String type;
    private boolean selected;
}