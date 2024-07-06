package com.hst.discount.service.impl;

import com.hst.discount.entity.Coupon;
import com.hst.discount.mapper.DiscountMapper;
import com.hst.discount.service.DiscountService;
import org.springframework.stereotype.Service;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@Service
public class DiscountServiceImpl implements DiscountService {
    @Autowired
    private DiscountMapper discountMapper;

    public List<Coupon> getAllCoupons() {
        return discountMapper.selectList(null);
    }

    public int addCoupon(Coupon coupon) {
        return discountMapper.insert(coupon);
    }

    public int updateCoupon(Long id, Coupon newCoupon) {
        Coupon existingCoupon = discountMapper.selectById(id);
        existingCoupon.setName(newCoupon.getName());
        existingCoupon.setDescription(newCoupon.getDescription());
        existingCoupon.setDiscount(newCoupon.getDiscount());
        existingCoupon.setValidity(newCoupon.getValidity());
        existingCoupon.setCategory(newCoupon.getCategory());
        existingCoupon.setType(newCoupon.getType());
        return discountMapper.updateById(existingCoupon);
    }

    public String deleteCoupon(Long id) {
        try{
            Coupon coupon = discountMapper.selectById(id);
            discountMapper.deleteById(coupon);
            return "删除成功";
        }catch (Exception e){
            System.out.println(e.getMessage());
            return "删除失败";
        }
    }
}