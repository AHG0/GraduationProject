package com.hst.discount.service;

import com.hst.discount.entity.Coupon;

import java.util.List;

public interface DiscountService {
    List<Coupon> getAllCoupons();

    int addCoupon(Coupon coupon);

    int updateCoupon(Long id, Coupon newCoupon);

    String deleteCoupon(Long id);
}
