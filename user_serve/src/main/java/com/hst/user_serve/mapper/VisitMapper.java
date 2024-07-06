package com.hst.user_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.user_serve.entity.UserVisit;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface VisitMapper extends BaseMapper<UserVisit> {
    @Select("select visit_day, sum(visit_count) as visit_count_sum, " +
            "sum(submit_count) as submit_count_sum, " +
            "sum(c_submit_count) as c_submit_count_sum " +
            "from user_visit " +
            "group by visit_day " +
            "order by visit_day")
    List<JSONObject> selectVisitCount();
    @Select("select registration_day, count(registration_day) as day_add_user " +
            "from user " +
            "group by registration_day " +
            "order by registration_day")
    List<JSONObject> dayAddUser();
}
