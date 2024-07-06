package com.hst.login_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.login_serve.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

@Mapper
public interface LoginMapper extends BaseMapper<User> {
    @Select("select MAX(userid) from user")
    int findMaxId();

    @Select("select * from user where username = #{username}")
    JSONObject selectLoginUser(String username);

    @Select("select exists (SELECT * from user_visit where userid=#{userid} and visit_day=#{visit_day})")
    int isLoginToday(int userid, String visit_day);

    @Update("update user set token=#{token} where username=#{username}")
    void updateToken(String username, String token);

    @Update("update user_visit set visit_count=visit_count+1 where userid=#{userid} and visit_day=#{day}")
    void countAdd(int userid, String day);
}
