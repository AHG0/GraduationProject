package com.hst.pay_serve.service.impl;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;
import com.alipay.api.AlipayApiException;
import com.alipay.api.AlipayClient;
import com.alipay.api.DefaultAlipayClient;
import com.alipay.api.internal.util.AlipaySignature;
import com.alipay.api.request.AlipayTradePagePayRequest;
import com.hst.pay_serve.config.AliPayConfig;
import com.hst.pay_serve.entity.PayOrder;
import com.hst.pay_serve.entity.UsedCoupons;
import com.hst.pay_serve.mapper.OrderMapper;
import com.hst.pay_serve.mapper.UsedCouponsMapper;
import com.hst.pay_serve.service.AliPayService;
import com.hst.user_serve.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
public class AliPayServiceImpl implements AliPayService {
    @Autowired
    private AliPayConfig aliPayConfig;
    @Autowired
    private OrderMapper orderMapper;
    @Autowired
    private UsedCouponsMapper usedCouponsMapper;
    @Autowired
    private PayOrder payOrder;
    private UserService userService;
    private String pay_time;
    private int user_id;
    private int user_type;
    private int queries_num;
    private int sub_period;

    @Override
    public String createOrder(String subject, Integer totalAmount, String description, int userid, String discount, Long discount_id) throws AlipayApiException {
        this.user_id = userid;
        if (subject.contains("普通会员")) {
            this.user_type = 0;
            this.queries_num = 10;
        } else if (subject.contains("中级会员")) {
            this.user_type = 1;
            this.queries_num = 100;
        } else {
            this.user_type = 2;
            this.queries_num = 1000;
        }
        if (subject.contains("月付")) {
            this.sub_period = 1;
        } else if (subject.contains("季付")) {
            this.sub_period = 2;
        } else {
            this.sub_period = 3;
        }
        payOrder.setOut_trade_no(getOrderNo());
        payOrder.setSubject(subject);
        payOrder.setTotal_amount(totalAmount);
        payOrder.setDescription(description);
        payOrder.setTimeout_express(aliPayConfig.getTimeout_express());
        payOrder.setProduct_code(aliPayConfig.getProduct_code());
        payOrder.setSub_period(this.sub_period);
        payOrder.setTrade_status("未付款");
        payOrder.setPay_channel("0");
        payOrder.setCreate_time(getTime());
        payOrder.setPay_time("（未付款）");
        payOrder.setUserid(userid);
        payOrder.setDiscount(discount);
        payOrder.setDiscount_id(discount_id);
        System.out.println(payOrder);
        orderMapper.insert(payOrder);
        // 将用户使用优惠券信息保存到数据库
        if (!Objects.equals(payOrder.getDiscount(), "0")) {
            UsedCoupons usedCoupons = new UsedCoupons();
            usedCoupons.setUserid(payOrder.getUserid());
            usedCoupons.setCouponId(payOrder.getDiscount_id());
            usedCouponsMapper.insert(usedCoupons);
        }
        // 支付宝网关
        String serverUrl = aliPayConfig.getGatewayUrl();
        // APPID
        String appId = aliPayConfig.getAppId();
        // 商户私钥, 即PKCS8格式RSA2私钥
        String privateKey = aliPayConfig.getPrivateKey();
        // 格式化为 json 格式
        String format = "json";
        // 字符编码格式
        String charset = aliPayConfig.getCharset();
        // 支付宝公钥, 即对应APPID下的支付宝公钥
        String alipayPublicKey = aliPayConfig.getPublicKey();
        // 签名方式
        String signType = aliPayConfig.getSignType();
        // 页面跳转同步通知页面路径
        String returnUrl = aliPayConfig.getReturnUrl();
        // 服务器异步通知页面路径
        String notifyUrl = aliPayConfig.getNotifyUrl();
        // 1、获得初始化的AlipayClient
        AlipayClient alipayClient = new DefaultAlipayClient(
                serverUrl, appId, privateKey, format, charset, alipayPublicKey, signType);
        // 2、设置请求参数
        AlipayTradePagePayRequest alipayRequest = new AlipayTradePagePayRequest();
        // 页面跳转同步通知页面路径
        alipayRequest.setReturnUrl(returnUrl);
        // 服务器异步通知页面路径
        alipayRequest.setNotifyUrl(notifyUrl);
        // 封装参数(以json格式封装)
        alipayRequest.setBizContent(JSON.toJSONString(payOrder));
        // 3、请求支付宝进行付款，并获取支付结果
        return alipayClient.pageExecute(alipayRequest).getBody();
    }

    public String getTime() {
        Date date = new Date();
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        return formatter.format(date);
    }

    public String getOrderNo() {
        //年、月、日、时、分、秒、毫秒
        DateTimeFormatter df = DateTimeFormatter.ofPattern("yyyyMMddHHmmssSSS");
        LocalDateTime localDateTime = Instant.ofEpochMilli(System.currentTimeMillis()).atZone(ZoneOffset.ofHours(8)).toLocalDateTime();
        return df.format(localDateTime);
    }

    public String payReturn(HttpServletRequest request) throws AlipayApiException {
        System.out.println("=========支付宝同步回调========");
        Map<String, String> params = new HashMap<>();
        Map<String, String[]> requestParams = request.getParameterMap();

        for (String name : requestParams.keySet()) {
            params.put(name, request.getParameter(name));
            //System.out.println(name + " = " + request.getParameter(name));
        }
        boolean checkSignature = AlipaySignature.rsaCheckV1(params, aliPayConfig.getALiPublicKey(), "UTF-8", aliPayConfig.getSignType());        // 支付宝验签
        if (checkSignature) {
            // 验签通过
            System.out.println("=========同步回调验签成功========");
            System.out.println("支付宝交易凭证号: " + params.get("trade_no"));
            System.out.println("商户订单号: " + params.get("out_trade_no"));
            System.out.println("交易金额: " + params.get("total_amount"));
            System.out.println("买家付款时间: " + params.get("timestamp"));
            System.out.println("买家付款金额: " + params.get("total_amount"));

            return "支付成功";
        } else {
            System.out.println("=========同步回调验签失败========");
            return "支付失败";
        }
    }

    public void payNotify(HttpServletRequest request) throws AlipayApiException, ParseException {
        System.out.println("=========支付宝异步回调========");
        for (String name : request.getParameterMap().keySet()) {
            System.out.println(name + " = " + request.getParameter(name));
        }
        if (request.getParameter("trade_status").equals("TRADE_SUCCESS")) {
            //获取支付宝POST过来反馈信息
            Map<String, String> params = new HashMap<>();
            Map<String, String[]> requestParams = request.getParameterMap();
            for (String name : requestParams.keySet()) {
                String[] values = requestParams.get(name);
                String valueStr = "";
                for (int i = 0; i < values.length; i++) {
                    valueStr = (i == values.length - 1) ? valueStr + values[i] : valueStr + values[i] + ",";
                }
                //乱码解决，这段代码在出现乱码时使用。
                //valueStr = new String(valueStr.getBytes("ISO-8859-1"), "utf-8");
                params.put(name, valueStr);
            }
            boolean signVerified = AlipaySignature.rsaCheckV1(params, aliPayConfig.getALiPublicKey(), "utf-8", "RSA2");
            if (signVerified) {//验证成功
                System.out.println("=========异步回调验签成功========");
                System.out.println(this.user_type);
                // 更新订单状态为已支付
                this.pay_time = params.get("gmt_payment");
                if (this.sub_period == 1) {
                    orderMapper.updateOrder(params.get("gmt_payment"), params.get("trade_status"), params.get("out_trade_no"), this.user_id);
                    orderMapper.updateUser(this.user_type, this.queries_num, addMonth(), this.user_id);
                } else if (this.sub_period == 2) {
                    orderMapper.updateOrder(params.get("gmt_payment"), params.get("trade_status"), params.get("out_trade_no"), this.user_id);
                    orderMapper.updateUser(this.user_type, this.queries_num, addQuarter(), this.user_id);
                } else {
                    orderMapper.updateOrder(params.get("gmt_payment"), params.get("trade_status"), params.get("out_trade_no"), this.user_id);
                    orderMapper.updateUser(this.user_type, this.queries_num, addYear(), this.user_id);
                }
                // 将用户使用优惠券信息保存到数据库
                if (!Objects.equals(payOrder.getDiscount(), "0")) {
                    UsedCoupons usedCoupons = new UsedCoupons();
                    usedCoupons.setUserid(payOrder.getUserid());
                    usedCoupons.setCouponId(payOrder.getDiscount_id());
                    usedCouponsMapper.insert(usedCoupons);
                }
                System.out.println("success");
            } else {//验证失败
                System.out.println("=========异步回调验签失败========");
                System.out.println("fail");
            }
        }
    }

    public List<JSONObject> getUsedCoupons(){
        return usedCouponsMapper.getUsedCoupons();
    }

    public List<Long> couponsUsedByUser(Integer userid){
        return usedCouponsMapper.couponsUsedByUser(userid);
    }

    public int isExistCoupon(Long coupon_id){
        return usedCouponsMapper.isExistCoupon(coupon_id);
    }

    public String deleteUsedCoupon(Long id){
        usedCouponsMapper.deleteById(id);
        return "删除成功";
    }

    public String addMonth() throws ParseException {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        Calendar c = Calendar.getInstance();
        c.setTime(formatter.parse(this.pay_time));
        c.add(Calendar.DATE, 30);  // number of days to add
        return formatter.format(c.getTime());
    }

    public String addQuarter() throws ParseException {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        Calendar c = Calendar.getInstance();
        c.setTime(formatter.parse(this.pay_time));
        c.add(Calendar.DATE, 90);  // number of days to add
        return formatter.format(c.getTime());
    }

    public String addYear() throws ParseException {
        SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd");
        Calendar c = Calendar.getInstance();
        c.setTime(formatter.parse(this.pay_time));
        c.add(Calendar.DATE, 360);  // number of days to add
        return formatter.format(c.getTime());
    }

    public List<JSONObject> selectAllOrder(int userid) {
        List<JSONObject> list = orderMapper.selectById(userid);
        System.out.println(list);
        return list;
    }

    public List<JSONObject> getDayPayCount() {
        return orderMapper.getDayPayCount();
    }

    public List<JSONObject> getDayPaySum() {
        return orderMapper.getDayPaySum();
    }
}