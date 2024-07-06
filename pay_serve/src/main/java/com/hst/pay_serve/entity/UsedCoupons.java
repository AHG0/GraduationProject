package com.hst.pay_serve.entity;

import lombok.Data;

import java.sql.Timestamp;

@Data
public class UsedCoupons {
    private Long id;
    private Integer userid;
    private Long couponId;
    private Data useTime;
}
