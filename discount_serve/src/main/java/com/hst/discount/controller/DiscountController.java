package com.hst.discount.controller;

import com.hst.discount.entity.Coupon;
import com.hst.discount.service.DiscountService;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class DiscountController {
    @Autowired
    private DiscountService discountService;
    Coupon coupon = new Coupon();

    @GetMapping("/get_coupon")
    public List<Coupon> getAllCoupons() {
        return discountService.getAllCoupons();
    }

    @RequestMapping("/add_coupon")
    public int addCoupon(@RequestParam("name") String name, @RequestParam("description") String description,
                         @RequestParam("discount") Double discount, @RequestParam("validity") String validity,
                         @RequestParam("category") String category, @RequestParam("type") String type) {
        coupon.setId(System.currentTimeMillis());
        coupon.setName(name);
        coupon.setDescription(description);
        coupon.setDiscount(discount);
        coupon.setValidity(validity);
        coupon.setCategory(category);
        coupon.setType(type);
        coupon.setSelected(false);
        return discountService.addCoupon(coupon);
    }

    @PutMapping("/update_coupon/{id}")
    public int updateCoupon(@PathVariable Long id, @RequestBody Coupon coupon) {
        return discountService.updateCoupon(id, coupon);
    }

    @DeleteMapping("/delete_coupon/{id}")
    public String deleteCoupon(@PathVariable Long id) {
        return discountService.deleteCoupon(id);
    }
}