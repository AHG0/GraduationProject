package com.hst.discount.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.discount.entity.Coupon;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

@Mapper
public interface DiscountMapper extends BaseMapper<Coupon> {
    @Select("select * from coupon where id=#{id}")
    Coupon selectById(Long id);
}
