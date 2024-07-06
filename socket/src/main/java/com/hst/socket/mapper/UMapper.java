package com.hst.socket.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.user_serve.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
@Mapper
public interface UMapper extends BaseMapper<User> {
    @Select("select * from user where userid = #{userid}")
    JSONObject getUser(int userid);
}
