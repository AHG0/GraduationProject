package com.hst.pay_serve.controller;

import com.alibaba.fastjson.JSONObject;
import com.alipay.api.AlipayApiException;
import com.hst.pay_serve.entity.PayOrder;
import com.hst.pay_serve.service.AliPayService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.text.ParseException;
import java.util.List;

@RestController
public class AliPayController {
    @Autowired
    private AliPayService aliPayService;

    @RequestMapping(value = "/AliPay")
    public String createOrder(@RequestParam("total_amount") Integer totalAmount, @RequestParam("subject") String subject,
                              @RequestParam("description") String description, @RequestParam("userid") int userid,
                              @RequestParam("discount") String discount, @RequestParam("discount_id") Long discount_id) throws AlipayApiException, ParseException {
        return aliPayService.createOrder(subject, totalAmount, description, userid, discount, discount_id);
    }

    @RequestMapping("/return")  // 同步调用，返回给用户，注意这里必须是GET接口
    public String payReturn(HttpServletRequest request) throws Exception {
        return aliPayService.payReturn(request);
    }

    @PostMapping("/notify")  // 注意这里必须是POST接口
    @ResponseBody
    public void payNotify(HttpServletRequest request) throws AlipayApiException, ParseException {
        aliPayService.payNotify(request);
    }

    @RequestMapping("/selectAllOrder")
    public List<JSONObject> selectAllOrder(@RequestParam("userid") int userid){
        return aliPayService.selectAllOrder(userid);
    }

    @RequestMapping("/getUsedCoupons")
    public List<JSONObject> getUsedCoupons(){
        return aliPayService.getUsedCoupons();
    }

    @RequestMapping("/couponsUsedByUser/{userid}")
    public List<Long> couponsUsedByUser(@PathVariable Integer userid){
        return aliPayService.couponsUsedByUser(userid);
    }

        @RequestMapping("/is_exist_coupon/{coupon_id}")
    public int isExistCoupon(@PathVariable Long coupon_id){
        return aliPayService.isExistCoupon(coupon_id);
    }

    @DeleteMapping("/delete_coupon/{id}")
    public String deleteCoupon(@PathVariable Long id) {
        return aliPayService.deleteUsedCoupon(id);
    }

    @RequestMapping("/getDayPayCount")
    public List<JSONObject> getDayPayCount(){
        return aliPayService.getDayPayCount();
    }

    @RequestMapping("/getDayPaySum")
    public List<JSONObject> getDayPaySum(){
        return aliPayService.getDayPaySum();
    }
}