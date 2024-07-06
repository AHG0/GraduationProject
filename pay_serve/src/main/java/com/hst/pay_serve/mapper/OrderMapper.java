package com.hst.pay_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.pay_serve.entity.PayOrder;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface OrderMapper extends BaseMapper<PayOrder> {
    @Update("UPDATE pay_order " +
            "SET pay_time=#{pay_time}, trade_status=#{trade_status} " +
            "WHERE out_trade_no=#{out_trade_no} and userid=#{userid}")
    void updateOrder(String pay_time, String trade_status, String out_trade_no, int userid);

    @Update("UPDATE user SET usertype=#{usertype}, queries_num=#{queries_num}, expire_date=#{expire_date} " +
            "WHERE userid=#{userid}")
    void updateUser(int usertype,int queries_num, String expire_date, int userid);

    @Select("select * from pay_order where userid=#{userid}")
    List<JSONObject> selectById(int userid);

    @Select("select DATE_FORMAT(pay_time, '%Y-%m-%d') as pay_day, count(DATE_FORMAT(pay_time, '%Y-%m-%d')) as pay_day_count " +
            "from pay_order " +
            "group by DATE_FORMAT(pay_time, '%Y-%m-%d') " +
            "order by DATE_FORMAT(pay_time, '%Y-%m-%d')")
    List<JSONObject> getDayPayCount();
    @Select("select DATE_FORMAT(pay_time, '%Y-%m-%d') as pay_day, sum(total_amount) as pay_day_sum " +
            "from pay_order " +
            "group by DATE_FORMAT(pay_time, '%Y-%m-%d') " +
            "order by DATE_FORMAT(pay_time, '%Y-%m-%d')")
    List<JSONObject> getDayPaySum();
}
