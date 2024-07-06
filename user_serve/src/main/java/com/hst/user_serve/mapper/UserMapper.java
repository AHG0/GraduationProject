package com.hst.user_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.user_serve.entity.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;

import java.util.List;

@Mapper
public interface UserMapper extends BaseMapper<User> {
    @Select("select MAX(userid) from user")
    int findMaxId();

    @Select("select exists (SELECT * from  user where username=#{name})")
    int selectExist(String name);

    @Select("select * from user")
    List<JSONObject> selectAllUser();

    @Select("select * from user where userid = #{userid}")
    JSONObject selectById(int userid);

    @Select("select * from user where username like concat('%', #{name}, '%')")
    List<JSONObject> fuzzyQueries(String name);

    @Update("UPDATE user " +
            "SET username = #{name} " +
            "WHERE userid=#{userid};")
    void updateName(int userid, String name);

    @Update("UPDATE user " +
            "SET phone = #{phone} " +
            "WHERE userid=#{userid};")
    void updatePhone(int userid, String phone);

    @Update("UPDATE user " +
            "SET password = #{password} " +
            "WHERE userid=#{userid};")
    void updatePassword(int userid, String password);

    @Update("UPDATE user " +
            "SET mail = #{mail} " +
            "WHERE userid = #{userid};")
    void updateMail(int userid, String mail);

    @Update("UPDATE user " +
            "SET queries_num = #{num} " +
            "WHERE userid = #{userid};")
    void updateQueriesNum(int userid, int num);

    @Update("UPDATE user " +
            "SET usertype = 0, expire_date = 'null' " +
            "WHERE userid=#{userid};")
    void expire(int userid);
}
