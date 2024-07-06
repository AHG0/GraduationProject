package com.hst.text_serve.mapper;

import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.hst.text_serve.entity.Entity;
import org.apache.ibatis.annotations.Delete;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

import java.util.List;

@Mapper
public interface EntityMapper extends BaseMapper<Entity> {

    @Select("select input from entity")
    List<String> selectEInput();

    @Select("select MAX(id) from entity")
    String findMaxId();

    @Select("select * from entity where input=#{input}")
    JSONObject selectEByInput(@Param("input") String input);

    @Delete("delete from entity where input=#{input}")
    boolean deleteEByInput(@Param("input") String input);
}
