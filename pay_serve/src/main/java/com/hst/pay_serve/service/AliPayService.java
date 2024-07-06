package com.hst.pay_serve.service;

import com.alibaba.fastjson.JSONObject;
import com.alipay.api.AlipayApiException;
import jakarta.servlet.http.HttpServletRequest;

import java.text.ParseException;
import java.util.List;

public interface AliPayService {
    String createOrder(String subject,Integer totalAmount,String description, int userid, String discount, Long discount_id) throws AlipayApiException, ParseException;
    //根据时间生成订单号
    String getOrderNo();
    String payReturn(HttpServletRequest request) throws AlipayApiException;
    void payNotify(HttpServletRequest request) throws AlipayApiException, ParseException;
    List<JSONObject> getUsedCoupons();
    List<Long> couponsUsedByUser(Integer userid);
    int isExistCoupon(Long coupon_id);
    String deleteUsedCoupon(Long id);
    String addMonth() throws ParseException;
    String addQuarter() throws ParseException;
    String addYear() throws ParseException;
    List<JSONObject> selectAllOrder(int userid);
    List<JSONObject> getDayPayCount();
    List<JSONObject> getDayPaySum();
}


