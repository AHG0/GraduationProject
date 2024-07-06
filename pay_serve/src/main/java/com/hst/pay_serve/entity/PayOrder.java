package com.hst.pay_serve.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;
import org.springframework.stereotype.Component;

@Data
@Component
public class PayOrder {
    //商户订单号，必填
    @TableId(value = "out_trade_no")
    private String out_trade_no;
    //订单名称，必填
    @TableField(value = "subject")
    private String subject;
    //付款金额，必填
    @TableField(value = "total_amount")
    private Integer total_amount;
    //商品描述，可空
    private String description;
    //订单超时时间
    private String timeout_express;
    //产品编号
    private String product_code;
    //订阅周期（月付：1，季付：2，年付：3）
    private Integer sub_period;
    //订单状态
    private String trade_status;
    //订单支付渠道（支付宝：0，微信：1）
    private String pay_channel;
    //订单创建时间
    private String create_time;
    //付款时间
    private String pay_time;
    //用户id
    private Integer userid;
    //折扣金额
    private String discount;
    private Long discount_id;
}
