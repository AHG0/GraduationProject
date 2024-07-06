package com.hst.pay_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.pay_serve.entity.UsedCoupons;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface UsedCouponsMapper extends BaseMapper<UsedCoupons> {
    @Select("select * from used_coupons")
    List<JSONObject> getUsedCoupons();
    @Select("select coupon_id from used_coupons where userid=#{userid}")
    List<Long> couponsUsedByUser(Integer userid);
    @Select("select exists (SELECT * from used_coupons where coupon_id=#{coupon_id})")
    int isExistCoupon(Long coupon_id);
    @Delete("delete from used_coupons where id=#{id}")
    void deleteById(Long id);
}
